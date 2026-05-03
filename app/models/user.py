from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    telegram_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    display_name: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    preferences: Mapped[dict] = mapped_column(JSON, default=dict)
    gentle_streak_days: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    books = relationship("Book", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("ReadingProgress", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("ReadingSession", back_populates="user", cascade="all, delete-orphan")
