from __future__ import annotations

import base64
import re
from typing import Optional

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Book, BookChunk, ReadingProgress, User
from app.services.book_parser import parse_book_upload
from app.utils.text import count_words


settings = get_settings()
UNCAT_TELEGRAM_ID = "6896703626"
PUBLIC_BOOK_TITLES = {"заповіт"}


def create_book_from_upload(
    db: Session,
    user: User,
    file: UploadFile,
    content: bytes,
    title: Optional[str] = None,
    author: Optional[str] = None,
) -> Book:
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File is too large")

    try:
        parsed = parse_book_upload(file.filename or "book.txt", content, title, author)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if not parsed.chunks:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not extract readable text")

    book = Book(
        user_id=user.id,
        title=parsed.title,
        author=parsed.author,
        source_type=parsed.source_type,
        original_filename=file.filename,
        cover_image_data_url=parsed.cover_image_data_url,
        total_words=parsed.total_words,
        total_chunks=len(parsed.chunks),
    )
    db.add(book)
    db.flush()

    db.add_all(
        BookChunk(book_id=book.id, chunk_index=index, text=chunk, word_count=count_words(chunk))
        for index, chunk in enumerate(parsed.chunks)
    )
    db.add(ReadingProgress(user_id=user.id, book_id=book.id, current_chunk_index=0))
    db.commit()
    db.refresh(book)
    return book


def update_book_metadata(
    db: Session,
    user: User,
    book_id: int,
    title: Optional[str] = None,
    author: Optional[str] = None,
    remove_cover: bool = False,
    cover_content: Optional[bytes] = None,
    cover_content_type: Optional[str] = None,
) -> Book:
    book = db.scalar(select(Book).where(Book.id == book_id))
    if not book or not can_user_read_book(user, book):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if not can_user_edit_book(user, book):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot edit this book")

    clean_title = title.strip() if title is not None else None
    if clean_title:
        book.title = clean_title
    if author is not None:
        book.author = author.strip() or None
    if remove_cover:
        book.cover_image_data_url = None
    if cover_content:
        book.cover_image_data_url = _cover_data_url(cover_content, cover_content_type)

    db.commit()
    db.refresh(book)
    return book


def list_user_books(db: Session, user: User) -> list[Book]:
    if is_uncat(user):
        return list(db.scalars(select(Book).order_by(Book.uploaded_at.desc())))

    own_books = list(db.scalars(select(Book).where(Book.user_id == user.id).order_by(Book.uploaded_at.desc())))
    own_ids = {book.id for book in own_books}
    public_books = [
        book
        for book in db.scalars(select(Book).where(Book.user_id != user.id).order_by(Book.uploaded_at.desc()))
        if book.id not in own_ids and is_public_book(book)
    ]
    return sorted([*own_books, *public_books], key=lambda book: book.uploaded_at, reverse=True)


def get_user_book(db: Session, user: User, book_id: int) -> Book:
    book = db.scalar(select(Book).where(Book.id == book_id))
    if not book or not can_user_read_book(user, book):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


def get_book_progress(db: Session, user: User, book_id: int) -> ReadingProgress:
    progress = db.scalar(select(ReadingProgress).where(ReadingProgress.user_id == user.id, ReadingProgress.book_id == book_id))
    if progress:
        return progress
    progress = ReadingProgress(user_id=user.id, book_id=book_id, current_chunk_index=0)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def get_chunk(db: Session, book_id: int, chunk_index: int) -> Optional[BookChunk]:
    return db.scalar(select(BookChunk).where(BookChunk.book_id == book_id, BookChunk.chunk_index == chunk_index))


def get_chunks_range(db: Session, book_id: int, start_index: int, limit: int) -> list[BookChunk]:
    return list(
        db.scalars(
            select(BookChunk)
            .where(BookChunk.book_id == book_id, BookChunk.chunk_index >= start_index)
            .order_by(BookChunk.chunk_index)
            .limit(limit)
        )
    )


def clamp_chunk_index(book: Book, chunk_index: int) -> int:
    if book.total_chunks <= 0:
        return 0
    return max(0, min(chunk_index, book.total_chunks - 1))


def search_book_chunks(db: Session, user: User, book_id: int, query: str, limit: int = 20) -> list[dict[str, object]]:
    book = get_user_book(db, user, book_id)
    clean_query = query.strip()
    if not clean_query:
        return []

    chunks = list(
        db.scalars(select(BookChunk).where(BookChunk.book_id == book.id).order_by(BookChunk.chunk_index))
    )
    numeric_match = re.fullmatch(r"\d+", clean_query)
    if numeric_match:
        chunk_index = int(clean_query) - 1
        if 0 <= chunk_index < len(chunks):
            chunk = chunks[chunk_index]
            return [_search_result(chunk, chunk.text[:220])]
        return []

    terms = [term.casefold() for term in clean_query.split() if term.strip()]
    results: list[dict[str, object]] = []
    for chunk in chunks:
        haystack = chunk.text.casefold()
        if not all(term in haystack for term in terms):
            continue
        results.append(_search_result(chunk, _build_snippet(chunk.text, terms)))
        if len(results) >= limit:
            break
    return results


def can_user_read_book(user: User, book: Book) -> bool:
    return is_uncat(user) or book.user_id == user.id or is_public_book(book)


def can_user_edit_book(user: User, book: Book) -> bool:
    return is_uncat(user) or book.user_id == user.id


def is_uncat(user: User) -> bool:
    return str(user.telegram_id) == UNCAT_TELEGRAM_ID


def is_public_book(book: Book) -> bool:
    return book.title.strip().casefold() in PUBLIC_BOOK_TITLES


def _search_result(chunk: BookChunk, snippet: str) -> dict[str, object]:
    return {
        "chunk_index": chunk.chunk_index,
        "page_number": chunk.chunk_index + 1,
        "word_count": chunk.word_count,
        "snippet": snippet,
    }


def _build_snippet(text: str, terms: list[str]) -> str:
    folded = text.casefold()
    first_match = min((folded.find(term) for term in terms if folded.find(term) >= 0), default=0)
    start = max(0, first_match - 80)
    end = min(len(text), first_match + 180)
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(text) else ""
    return prefix + text[start:end].strip() + suffix


def _cover_data_url(content: bytes, content_type: Optional[str]) -> str:
    if len(content) > 1_500_000:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Cover image is too large")
    mime = (content_type or "image/jpeg").split(";")[0].strip().lower()
    if mime not in {"image/jpeg", "image/png", "image/webp", "image/gif"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cover must be JPEG, PNG, WebP or GIF")
    return f"data:{mime};base64,{base64.b64encode(content).decode('ascii')}"
