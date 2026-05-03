from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ReadingSession(Base):
    __tablename__ = "reading_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), index=True)
    planned_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    start_chunk_index: Mapped[int] = mapped_column(Integer, default=0)
    end_chunk_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    chunks_read: Mapped[int] = mapped_column(Integer, default=0)
    words_read: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="sessions")
    book = relationship("Book", back_populates="sessions")
