from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ReadingProgress, User
from app.schemas.progress import ProgressUpdate
from app.services.books import clamp_chunk_index, get_user_book


def update_progress(db: Session, user: User, book_id: int, payload: ProgressUpdate) -> ReadingProgress:
    book = get_user_book(db, user, book_id)
    progress = db.scalar(select(ReadingProgress).where(ReadingProgress.user_id == user.id, ReadingProgress.book_id == book_id))
    if not progress:
        progress = ReadingProgress(user_id=user.id, book_id=book_id)
        db.add(progress)

    progress.current_chunk_index = clamp_chunk_index(book, payload.current_chunk_index)
    progress.chunks_read += payload.chunks_read
    progress.words_read += payload.words_read
    progress.last_opened_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(progress)
    return progress


def touch_last_opened(db: Session, progress: ReadingProgress) -> ReadingProgress:
    progress.last_opened_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(progress)
    return progress
