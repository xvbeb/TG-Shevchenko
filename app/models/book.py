from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    author: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    source_type: Mapped[str] = mapped_column(String(16), nullable=False)
    original_filename: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    total_words: Mapped[int] = mapped_column(Integer, default=0)
    total_chunks: Mapped[int] = mapped_column(Integer, default=0)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="books")
    chunks = relationship("BookChunk", back_populates="book", cascade="all, delete-orphan", order_by="BookChunk.chunk_index")
    progress = relationship("ReadingProgress", back_populates="book", cascade="all, delete-orphan")
    sessions = relationship("ReadingSession", back_populates="book", cascade="all, delete-orphan")


class BookChunk(Base):
    __tablename__ = "book_chunks"
    __table_args__ = (UniqueConstraint("book_id", "chunk_index", name="uq_book_chunk_index"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, default=0)

    book = relationship("Book", back_populates="chunks")
