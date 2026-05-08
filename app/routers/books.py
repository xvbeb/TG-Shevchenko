from __future__ import annotations

from typing import Optional
from typing import Literal

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.routers.dependencies import get_current_user
from app.schemas.book import BookDetail, BookRead, BookSearchResponse, ReadRangeResponse, ReadResponse
from app.schemas.progress import ProgressUpdate, ReadingProgressRead
from app.schemas.welcome_bonus import WelcomeBonusRead
from app.services.books import (
    clamp_chunk_index,
    create_book_from_upload,
    get_book_progress,
    get_chunk,
    get_chunks_range,
    get_user_book,
    list_user_books,
    search_book_chunks,
)
from app.services.progress import touch_last_opened, update_progress
from app.services.welcome_bonus import create_welcome_bonus

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/upload", response_model=BookRead, status_code=201)
async def upload_book(
    file: UploadFile = File(...),
    title: Optional[str] = Form(default=None),
    author: Optional[str] = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content = await file.read()
    return create_book_from_upload(db, current_user, file, content, title, author)


@router.get("", response_model=list[BookRead])
def get_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_user_books(db, current_user)


@router.get("/{book_id}", response_model=BookDetail)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = get_user_book(db, current_user, book_id)
    progress = get_book_progress(db, current_user, book_id)
    return BookDetail(
        **BookRead.model_validate(book).model_dump(),
        current_chunk_index=progress.current_chunk_index,
        last_opened_at=progress.last_opened_at,
    )


@router.get("/{book_id}/read", response_model=ReadResponse)
def read_book(
    book_id: int,
    chunk_index: Optional[int] = Query(default=None, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = get_user_book(db, current_user, book_id)
    progress = get_book_progress(db, current_user, book_id)
    selected_index = clamp_chunk_index(book, chunk_index if chunk_index is not None else progress.current_chunk_index)
    chunk = get_chunk(db, book.id, selected_index)
    touch_last_opened(db, progress)
    return ReadResponse(
        book=BookRead.model_validate(book),
        chunk=chunk,
        current_chunk_index=selected_index,
        total_chunks=book.total_chunks,
        has_previous=selected_index > 0,
        has_next=selected_index < max(0, book.total_chunks - 1),
    )


@router.get("/{book_id}/read-range", response_model=ReadRangeResponse)
def read_book_range(
    book_id: int,
    start_chunk_index: int = Query(default=0, ge=0),
    limit: int = Query(default=24, ge=1, le=80),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = get_user_book(db, current_user, book_id)
    selected_index = clamp_chunk_index(book, start_chunk_index)
    chunks = get_chunks_range(db, book.id, selected_index, limit)
    end_index = chunks[-1].chunk_index if chunks else selected_index
    return ReadRangeResponse(
        book=BookRead.model_validate(book),
        chunks=chunks,
        start_chunk_index=selected_index,
        end_chunk_index=end_index,
        total_chunks=book.total_chunks,
        has_previous=selected_index > 0,
        has_next=end_index < max(0, book.total_chunks - 1),
    )


@router.post("/{book_id}/progress", response_model=ReadingProgressRead)
def save_progress(
    book_id: int,
    payload: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_progress(db, current_user, book_id, payload)


@router.get("/{book_id}/welcome-bonus", response_model=WelcomeBonusRead)
def welcome_bonus(
    book_id: int,
    depth: Literal["quick", "story", "deep"] = Query(default="story"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_welcome_bonus(db, current_user, book_id, depth)


@router.get("/{book_id}/search", response_model=BookSearchResponse)
def search_book(
    book_id: int,
    q: str = Query(min_length=1, max_length=160),
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {"query": q, "results": search_book_chunks(db, current_user, book_id, q, limit)}
