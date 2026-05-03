from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ReadingProgress, ReadingSession, User
from app.schemas.session import SessionEnd, SessionStart
from app.services.books import clamp_chunk_index, get_book_progress, get_user_book


def start_session(db: Session, user: User, payload: SessionStart) -> ReadingSession:
    book = get_user_book(db, user, payload.book_id)
    progress = get_book_progress(db, user, book.id)
    start_chunk_index = clamp_chunk_index(book, payload.start_chunk_index if payload.start_chunk_index is not None else progress.current_chunk_index)

    session = ReadingSession(
        user_id=user.id,
        book_id=book.id,
        planned_minutes=payload.planned_minutes,
        start_chunk_index=start_chunk_index,
    )
    progress.last_opened_at = datetime.now(timezone.utc)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def end_session(db: Session, user: User, payload: SessionEnd) -> ReadingSession:
    session = db.scalar(select(ReadingSession).where(ReadingSession.id == payload.session_id, ReadingSession.user_id == user.id))
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    if session.ended_at:
        return session

    book = get_user_book(db, user, session.book_id)
    end_chunk_index = clamp_chunk_index(book, payload.end_chunk_index)
    session.end_chunk_index = end_chunk_index
    session.chunks_read = payload.chunks_read
    session.words_read = payload.words_read
    session.ended_at = datetime.now(timezone.utc)

    progress = db.scalar(
        select(ReadingProgress).where(ReadingProgress.user_id == user.id, ReadingProgress.book_id == session.book_id)
    )
    if progress:
        progress.current_chunk_index = end_chunk_index
        progress.chunks_read += payload.chunks_read
        progress.words_read += payload.words_read
        progress.last_opened_at = session.ended_at

    db.commit()
    db.refresh(session)
    return session
