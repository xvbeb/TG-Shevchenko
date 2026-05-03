from __future__ import annotations

from typing import Optional

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Book, BookChunk, ReadingProgress, User
from app.services.book_parser import parse_book_upload
from app.utils.text import count_words


settings = get_settings()


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


def list_user_books(db: Session, user: User) -> list[Book]:
    return list(db.scalars(select(Book).where(Book.user_id == user.id).order_by(Book.uploaded_at.desc())))


def get_user_book(db: Session, user: User, book_id: int) -> Book:
    book = db.scalar(select(Book).where(Book.id == book_id, Book.user_id == user.id))
    if not book:
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


def clamp_chunk_index(book: Book, chunk_index: int) -> int:
    if book.total_chunks <= 0:
        return 0
    return max(0, min(chunk_index, book.total_chunks - 1))
