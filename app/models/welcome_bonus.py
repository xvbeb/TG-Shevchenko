from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class WelcomeBonus(Base):
    __tablename__ = "welcome_bonuses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), index=True)
    from_chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    to_chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    current_chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    generated_by: Mapped[str] = mapped_column(String(64), default="rule_based")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    book = relationship("Book")
