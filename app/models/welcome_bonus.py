from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class WelcomeBonus(Base):
    __tablename__ = "welcome_bonuses"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "book_id",
            "current_chunk_index",
            "bonus_type",
            "model",
            "prompt_version",
            name="uq_welcome_bonus_cache",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), index=True)
    from_chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    to_chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    current_chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    bonus_type: Mapped[str] = mapped_column(String(32), default="quick", index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    generated_by: Mapped[str] = mapped_column(String(64), default="rule_based")
    model: Mapped[str] = mapped_column(String(128), default="rule_based", index=True)
    prompt_version: Mapped[str] = mapped_column(String(64), default="rule_based_v1", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    book = relationship("Book")
