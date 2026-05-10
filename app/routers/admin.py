from __future__ import annotations

from collections import Counter
from pathlib import Path

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import Book, ReadingProgress, User, WelcomeBonus
from app.routers.dependencies import get_current_user
from app.schemas.admin import (
    AdminBookRow,
    AdminMessageRequest,
    AdminMessageResponse,
    AdminMessageResult,
    AdminProgressRow,
    AdminRechunkResponse,
    AdminStats,
    AdminSummary,
    AdminUserRow,
)
from app.services.books import is_uncat, rechunk_book

router = APIRouter(prefix="/admin", tags=["admin"])


def require_uncat_admin(current_user: User = Depends(get_current_user)) -> User:
    if not is_uncat(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin dashboard is only available to Uncat")
    return current_user


@router.get("/", include_in_schema=False)
def admin_dashboard() -> FileResponse:
    return FileResponse(Path("app/static/admin.html"))


@router.get("/admin.css", include_in_schema=False)
def admin_styles() -> FileResponse:
    return FileResponse(Path("app/static/admin.css"), media_type="text/css")


@router.get("/admin.js", include_in_schema=False)
def admin_script() -> FileResponse:
    return FileResponse(Path("app/static/admin.js"), media_type="application/javascript")


@router.get("/api/summary", response_model=AdminSummary)
def admin_summary(
    db: Session = Depends(get_db),
    _: User = Depends(require_uncat_admin),
) -> AdminSummary:
    users = list(db.scalars(select(User).order_by(desc(User.created_at))))
    books = list(db.scalars(select(Book).order_by(desc(Book.uploaded_at))))
    progress_rows = list(
        db.execute(
            select(ReadingProgress, User, Book)
            .join(User, ReadingProgress.user_id == User.id)
            .join(Book, ReadingProgress.book_id == Book.id)
            .order_by(desc(ReadingProgress.updated_at))
        ).all()
    )

    book_counts = Counter(book.user_id for book in books)
    bonus_counts = dict(db.execute(select(WelcomeBonus.user_id, func.count()).group_by(WelcomeBonus.user_id)).all())
    total_welcome_bonuses = sum(int(count) for count in bonus_counts.values())

    return AdminSummary(
        stats=AdminStats(
            total_users=len(users),
            total_books=len(books),
            total_welcome_bonuses=total_welcome_bonuses,
            active_progress_rows=len(progress_rows),
        ),
        users=[
            AdminUserRow(
                id=user.id,
                telegram_id=user.telegram_id,
                username=user.username,
                display_name=user.display_name,
                books_added=book_counts.get(user.id, 0),
                welcome_bonuses_used=int(bonus_counts.get(user.id, 0)),
                created_at=user.created_at,
            )
            for user in users
        ],
        progress=[
            AdminProgressRow(
                user_id=user.id,
                telegram_id=user.telegram_id,
                username=user.username,
                display_name=user.display_name,
                book_id=book.id,
                book_title=book.title,
                book_author=book.author,
                current_chunk_index=progress.current_chunk_index,
                current_page=progress.current_chunk_index + 1,
                total_chunks=book.total_chunks,
                progress_percent=_progress_percent(progress.current_chunk_index, book.total_chunks),
                last_opened_at=progress.last_opened_at,
                updated_at=progress.updated_at,
            )
            for progress, user, book in progress_rows
        ],
        books=[
            AdminBookRow(
                id=book.id,
                title=book.title,
                author=book.author,
                original_filename=book.original_filename,
                source_type=book.source_type,
                total_words=book.total_words,
                total_chunks=book.total_chunks,
                uploaded_at=book.uploaded_at,
                owner_user_id=book.user.id,
                owner_telegram_id=book.user.telegram_id,
                owner_username=book.user.username,
                owner_display_name=book.user.display_name,
            )
            for book in books
        ],
    )


@router.post("/api/messages", response_model=AdminMessageResponse)
async def send_admin_message(
    payload: AdminMessageRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_uncat_admin),
) -> AdminMessageResponse:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="TELEGRAM_BOT_TOKEN is not configured")

    recipients = _message_recipients(db, payload)
    if not recipients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No recipients found")

    results: list[AdminMessageResult] = []
    async with httpx.AsyncClient(timeout=12) as client:
        for user in recipients:
            results.append(await _send_telegram_message(client, settings.telegram_bot_token, user, payload.text.strip()))

    sent = sum(1 for result in results if result.ok)
    return AdminMessageResponse(sent=sent, failed=len(results) - sent, results=results)


@router.post("/api/books/{book_id}/rechunk", response_model=AdminRechunkResponse)
def rechunk_admin_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_uncat_admin),
) -> AdminRechunkResponse:
    return AdminRechunkResponse(**rechunk_book(db, current_user, book_id))


def _message_recipients(db: Session, payload: AdminMessageRequest) -> list[User]:
    if payload.audience == "all":
        return list(db.scalars(select(User).order_by(User.id)))
    if not payload.user_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="user_id is required for a user message")
    user = db.scalar(select(User).where(User.id == payload.user_id))
    return [user] if user else []


async def _send_telegram_message(
    client: httpx.AsyncClient,
    bot_token: str,
    user: User,
    text: str,
) -> AdminMessageResult:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        response = await client.post(
            url,
            json={
                "chat_id": user.telegram_id,
                "text": text,
                "disable_web_page_preview": True,
            },
        )
        data = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        return AdminMessageResult(user_id=user.id, telegram_id=user.telegram_id, ok=False, error=str(exc))

    if response.is_success and data.get("ok"):
        return AdminMessageResult(user_id=user.id, telegram_id=user.telegram_id, ok=True)

    description = data.get("description") if isinstance(data, dict) else response.text
    return AdminMessageResult(
        user_id=user.id,
        telegram_id=user.telegram_id,
        ok=False,
        error=description or f"Telegram API returned HTTP {response.status_code}",
    )


def _progress_percent(current_chunk_index: int, total_chunks: int) -> float:
    if total_chunks <= 0:
        return 0
    return round(((current_chunk_index + 1) / total_chunks) * 100, 1)
