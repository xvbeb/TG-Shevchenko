from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.models import BookChunk, User, WelcomeBonus
from app.services.ai import (
    AIProviderError,
    WelcomeBonusRequest,
    WelcomeBonusType,
    display_text_from_payload,
    fallback_bonus_payload,
    generate_welcome_bonus,
    looks_like_json_fragment,
    parse_json_payload,
)
from app.services.books import get_book_progress, get_user_book


def create_welcome_bonus(
    db: Session,
    user: User,
    book_id: int,
    bonus_type: WelcomeBonusType = "quick",
) -> WelcomeBonus:
    settings = get_settings()
    book = get_user_book(db, user, book_id)
    progress = get_book_progress(db, user, book.id)
    current_index = progress.current_chunk_index
    language = _ui_language(user)
    model = settings.ai_model
    fallback_model = _fallback_model_name(model)
    prompt_version = settings.welcome_bonus_prompt_version

    cached = _get_cached_bonus(db, user.id, book.id, current_index, bonus_type, model, prompt_version)
    if not cached and not _ai_is_configured(settings):
        cached = _get_cached_bonus(db, user.id, book.id, current_index, bonus_type, fallback_model, prompt_version)
    cached = _usable_cached_bonus(db, cached)
    if cached:
        return cached

    context_count = _context_count_for_type(bonus_type, settings.welcome_bonus_context_chunks)
    from_index = max(0, current_index - context_count)
    to_index = max(0, current_index - 1)
    chunks = list(
        db.scalars(
            select(BookChunk)
            .where(BookChunk.book_id == book.id, BookChunk.chunk_index >= from_index, BookChunk.chunk_index <= to_index)
            .order_by(BookChunk.chunk_index)
        )
    )
    context_chunks = _limit_context(chunks, settings.welcome_bonus_max_context_chars)
    previous_chunks_text = _format_context_chunks(context_chunks)
    from_index = context_chunks[0][0].chunk_index if context_chunks else current_index
    to_index = context_chunks[-1][0].chunk_index if context_chunks else max(0, current_index - 1)

    cache_model = model
    generated_by = f"{settings.ai_provider}_{prompt_version}_{bonus_type}_{language}"
    try:
        if context_chunks:
            generation = generate_welcome_bonus(
                WelcomeBonusRequest(
                    book_title=book.title,
                    book_type=_book_type_hint(bonus_type),
                    current_chunk_index=current_index,
                    bonus_type=bonus_type,
                    previous_chunks_text=previous_chunks_text,
                    ui_language=language,
                ),
                settings=settings,
            )
            payload = generation.payload
            if not generation.parsed_json:
                if looks_like_json_fragment(generation.raw_text):
                    raise AIProviderError("Gemini returned incomplete JSON")
                generated_by = f"gemini_raw_fallback_{prompt_version}_{bonus_type}_{language}"
        else:
            payload = fallback_bonus_payload("")
            cache_model = fallback_model
            generated_by = f"fallback_no_context_{prompt_version}_{bonus_type}_{language}"
    except AIProviderError:
        cached_fallback = _get_cached_bonus(db, user.id, book.id, current_index, bonus_type, fallback_model, prompt_version)
        cached_fallback = _usable_cached_bonus(db, cached_fallback)
        if cached_fallback:
            return cached_fallback
        payload = fallback_bonus_payload(_preview_text(previous_chunks_text))
        cache_model = fallback_model
        generated_by = f"fallback_provider_{prompt_version}_{bonus_type}_{language}"

    recap = WelcomeBonus(
        user_id=user.id,
        book_id=book.id,
        from_chunk_index=from_index,
        to_chunk_index=to_index,
        current_chunk_index=current_index,
        bonus_type=bonus_type,
        text=display_text_from_payload(payload),
        payload=payload,
        generated_by=generated_by[:64],
        model=cache_model,
        prompt_version=prompt_version,
    )
    db.add(recap)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        cached = _get_cached_bonus(db, user.id, book.id, current_index, bonus_type, cache_model, prompt_version)
        cached = _usable_cached_bonus(db, cached)
        if cached:
            return cached
        raise
    db.refresh(recap)
    return recap


def _usable_cached_bonus(db: Session, bonus: WelcomeBonus | None) -> WelcomeBonus | None:
    if bonus is None:
        return None
    if _cached_bonus_has_broken_json(bonus):
        db.delete(bonus)
        db.commit()
        return None
    return _normalize_cached_bonus(db, bonus)


def _cached_bonus_has_broken_json(bonus: WelcomeBonus) -> bool:
    payload = bonus.payload or {}
    recap = payload.get("recap") if isinstance(payload, dict) else None
    return looks_like_json_fragment(bonus.text or "") or (
        isinstance(recap, str) and looks_like_json_fragment(recap)
    )


def _normalize_cached_bonus(db: Session, bonus: WelcomeBonus) -> WelcomeBonus:
    if bonus.payload:
        return bonus

    parsed = parse_json_payload(bonus.text)
    if parsed is not None:
        bonus.payload = parsed
        bonus.text = display_text_from_payload(parsed)
    else:
        bonus.payload = {
            "type": bonus.bonus_type or "quick",
            "title": "Що було раніше",
            "recap": bonus.text,
            "continue_hint": "Можна спокійно продовжувати читання.",
        }
    db.commit()
    db.refresh(bonus)
    return bonus


def _get_cached_bonus(
    db: Session,
    user_id: int,
    book_id: int,
    current_index: int,
    bonus_type: str,
    model: str,
    prompt_version: str,
) -> WelcomeBonus | None:
    return db.scalar(
        select(WelcomeBonus)
        .where(
            WelcomeBonus.user_id == user_id,
            WelcomeBonus.book_id == book_id,
            WelcomeBonus.current_chunk_index == current_index,
            WelcomeBonus.bonus_type == bonus_type,
            WelcomeBonus.model == model,
            WelcomeBonus.prompt_version == prompt_version,
        )
        .order_by(WelcomeBonus.created_at.desc(), WelcomeBonus.id.desc())
    )


def _ai_is_configured(settings: Settings) -> bool:
    if settings.ai_provider.strip().lower() == "gemini":
        return bool(settings.gemini_api_key)
    return False


def _fallback_model_name(model: str) -> str:
    return f"fallback:{model}"[:128]


def _context_count_for_type(bonus_type: WelcomeBonusType, default_count: int) -> int:
    default_count = min(max(default_count, 8), 12)
    return {
        "quick": 8,
        "fiction": default_count,
        "nonfiction": default_count,
        "characters": 12,
    }[bonus_type]


def _book_type_hint(bonus_type: WelcomeBonusType) -> str | None:
    if bonus_type in {"fiction", "nonfiction"}:
        return bonus_type
    return None


def _ui_language(user: User) -> str:
    language = (user.preferences or {}).get("language") or "uk"
    return "uk" if language not in {"uk", "en"} else language


def _limit_context(chunks: list[BookChunk], max_chars: int) -> list[tuple[BookChunk, str]]:
    if max_chars <= 0:
        return [(chunk, chunk.text.strip()) for chunk in chunks if chunk.text.strip()]

    selected: list[tuple[BookChunk, str]] = []
    total_chars = 0
    for chunk in reversed(chunks):
        text = chunk.text.strip()
        if not text:
            continue
        label_budget = 32
        next_total = total_chars + len(text) + label_budget
        if selected and next_total > max_chars:
            break
        if not selected and next_total > max_chars:
            text = text[-max(0, max_chars - label_budget) :]
            next_total = len(text) + label_budget
        selected.append((chunk, text))
        total_chars = next_total
        if total_chars >= max_chars:
            break
    return list(reversed(selected))


def _format_context_chunks(chunks: list[tuple[BookChunk, str]]) -> str:
    return "\n\n".join(f"[chunk_index={chunk.chunk_index}]\n{text}" for chunk, text in chunks if text.strip())


def _preview_text(text: str, max_chars: int = 1200) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[-max_chars:].strip()
