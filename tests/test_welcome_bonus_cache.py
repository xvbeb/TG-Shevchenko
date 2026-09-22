from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.config import Settings
from app.database import Base
from app.models import Book, BookChunk, ReadingProgress, User
from app.services.ai import WelcomeBonusGeneration
import app.services.welcome_bonus as welcome_bonus_service


def test_welcome_bonus_is_reused_from_cache(monkeypatch) -> None:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    settings = Settings(
        _env_file=None,
        ai_provider="gemini",
        ai_model="test-model",
        gemini_api_key="test-key",
        welcome_bonus_prompt_version="test-v1",
    )
    calls = 0

    def fake_generate(*args, **kwargs):
        nonlocal calls
        calls += 1
        payload = {
            "type": "quick",
            "title": "Що було раніше",
            "recap": "Короткий тестовий переказ.",
            "key_points": [],
            "continue_hint": "Можна продовжувати.",
        }
        return WelcomeBonusGeneration(payload=payload, raw_text="{}", parsed_json=True)

    monkeypatch.setattr(welcome_bonus_service, "get_settings", lambda: settings)
    monkeypatch.setattr(welcome_bonus_service, "generate_welcome_bonus", fake_generate)

    with Session(engine) as db:
        user = User(telegram_id="cache-user")
        db.add(user)
        db.flush()
        book = Book(user_id=user.id, title="Cache Book", source_type="txt", total_words=20, total_chunks=2)
        db.add(book)
        db.flush()
        db.add_all(
            [
                BookChunk(book_id=book.id, chunk_index=0, text="Previous context.", word_count=2),
                BookChunk(book_id=book.id, chunk_index=1, text="Current context.", word_count=2),
                ReadingProgress(user_id=user.id, book_id=book.id, current_chunk_index=1),
            ]
        )
        db.commit()

        first = welcome_bonus_service.create_welcome_bonus(db, user, book.id, "quick")
        second = welcome_bonus_service.create_welcome_bonus(db, user, book.id, "quick")

        assert first.id == second.id
        assert calls == 1
        assert second.payload["recap"] == "Короткий тестовий переказ."

