from __future__ import annotations

from typing import Literal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import BookChunk, User, WelcomeBonus
from app.services.books import get_book_progress, get_user_book
from app.utils.text import first_sentence

RecapDepth = Literal["quick", "story", "deep"]


def create_welcome_bonus(db: Session, user: User, book_id: int, depth: RecapDepth = "story") -> WelcomeBonus:
    book = get_user_book(db, user, book_id)
    progress = get_book_progress(db, user, book.id)
    current_index = progress.current_chunk_index
    paragraph_count = _paragraph_count_for_depth(depth)
    from_index = max(0, current_index - paragraph_count)
    to_index = max(0, current_index - 1)

    chunks = list(
        db.scalars(
            select(BookChunk)
            .where(BookChunk.book_id == book.id, BookChunk.chunk_index >= from_index, BookChunk.chunk_index <= to_index)
            .order_by(BookChunk.chunk_index)
        )
    )
    text = _build_rule_based_recap(chunks, current_index, depth)
    recap = WelcomeBonus(
        user_id=user.id,
        book_id=book.id,
        from_chunk_index=from_index,
        to_chunk_index=to_index,
        current_chunk_index=current_index,
        text=text,
        generated_by=f"rule_based_v1_{depth}",
    )
    db.add(recap)
    db.commit()
    db.refresh(recap)
    return recap


def _paragraph_count_for_depth(depth: RecapDepth) -> int:
    return {"quick": 5, "story": 10, "deep": 15}[depth]


def _build_rule_based_recap(chunks: list[BookChunk], current_index: int, depth: RecapDepth) -> str:
    if not chunks:
        return "Это начало книги. Можно просто прочитать первый небольшой фрагмент и остановиться без давления."

    highlights = [first_sentence(chunk.text) for chunk in chunks if chunk.text.strip()]
    if not highlights:
        return f"Вы остановились перед фрагментом {current_index + 1}. Продолжим спокойно, по одному абзацу."

    if depth == "quick":
        return "Коротко: " + " ".join(highlights[-2:])

    if depth == "story":
        return (
            "Что происходило: "
            + _join_event_sentences(highlights[-5:])
            + " Сейчас можно продолжить с того места, где внимание уже почти зацепилось."
        )

    return (
        "Подробный пересказ: "
        + _join_event_sentences(highlights[-8:])
        + " Если читать дальше тяжело, достаточно взять следующий абзац как отдельную маленькую сцену."
    )


def _join_event_sentences(sentences: list[str]) -> str:
    cleaned = [sentence.strip() for sentence in sentences if sentence.strip()]
    if not cleaned:
        return ""
    return " ".join(cleaned)
