from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Literal, Protocol

import httpx

from app.config import Settings, get_settings

WelcomeBonusType = Literal["quick", "fiction", "nonfiction", "characters"]


class AIProviderError(RuntimeError):
    pass


@dataclass(frozen=True)
class WelcomeBonusRequest:
    book_title: str
    current_chunk_index: int
    bonus_type: WelcomeBonusType = "quick"
    previous_chunks_text: str = ""
    ui_language: str = "uk"
    book_type: str | None = None
    summary_so_far: str | None = None


@dataclass(frozen=True)
class WelcomeBonusGeneration:
    payload: dict[str, Any]
    raw_text: str
    parsed_json: bool


class AIProvider(Protocol):
    def generate_welcome_bonus(self, request: WelcomeBonusRequest) -> WelcomeBonusGeneration:
        pass


def generate_welcome_bonus(
    request: WelcomeBonusRequest,
    settings: Settings | None = None,
) -> WelcomeBonusGeneration:
    active_settings = settings or get_settings()
    provider = _get_provider(active_settings)
    return provider.generate_welcome_bonus(request)


def _get_provider(settings: Settings) -> AIProvider:
    provider_name = settings.ai_provider.strip().lower()
    if provider_name == "gemini":
        return GeminiProvider(settings.gemini_api_key, settings.ai_model)
    raise AIProviderError(f"Unsupported AI_PROVIDER: {settings.ai_provider}")


class GeminiProvider:
    def __init__(self, api_key: str | None, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def generate_welcome_bonus(self, request: WelcomeBonusRequest) -> WelcomeBonusGeneration:
        if not self.api_key:
            raise AIProviderError("GEMINI_API_KEY is not configured")

        prompt = build_welcome_bonus_prompt(request)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.25,
                "topP": 0.9,
                # Gemini 2.5 counts internal thinking against maxOutputTokens. Recaps
                # are a formatting task, so disable thinking to avoid truncated JSON.
                "thinkingConfig": {"thinkingBudget": 0},
                "maxOutputTokens": 1600,
                "responseMimeType": "application/json",
            },
        }
        headers = {"x-goog-api-key": self.api_key}

        try:
            with httpx.Client(timeout=20.0) as client:
                response = client.post(url, headers=headers, json=payload)
        except httpx.HTTPError as exc:
            raise AIProviderError("Gemini request failed") from exc

        if response.status_code >= 400:
            raise AIProviderError(f"Gemini request failed with HTTP {response.status_code}")

        raw_text = _extract_gemini_text(response)
        parsed = parse_json_payload(raw_text)
        if parsed is None:
            return WelcomeBonusGeneration(
                payload=raw_text_payload(request.bonus_type, raw_text),
                raw_text=raw_text,
                parsed_json=False,
            )

        normalized = normalize_bonus_payload(parsed, request.bonus_type)
        return WelcomeBonusGeneration(payload=normalized, raw_text=raw_text, parsed_json=True)


def _extract_gemini_text(response: httpx.Response) -> str:
    try:
        data = response.json()
        parts = data["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise AIProviderError("Gemini response did not include text") from exc

    text = "\n".join(str(part.get("text", "")).strip() for part in parts if part.get("text")).strip()
    if not text:
        raise AIProviderError("Gemini returned empty text")
    return text


def parse_json_payload(raw_text: str) -> dict[str, Any] | None:
    candidates = [raw_text.strip()]
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, flags=re.DOTALL)
    if fenced:
        candidates.append(fenced.group(1).strip())
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidates.append(raw_text[start : end + 1])

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


def build_welcome_bonus_prompt(request: WelcomeBonusRequest) -> str:
    schema = _schema_for_bonus_type(request.bonus_type)
    focus = _focus_for_bonus_type(request.bonus_type)
    language_name = "українська" if request.ui_language == "uk" else request.ui_language
    book_type = request.book_type or "невідомий"
    summary = request.summary_so_far or "Немає."

    return f"""Ти генеруєш Welcome Bonus для Telegram Mini App читалки.

Завдання: допомогти користувачу м'яко повернутися до книжки після паузи. Не замінюй читання.

Тип Welcome Bonus: {request.bonus_type}
Фокус цього типу: {focus}

Суворі правила:
- Використовуй тільки наданий нижче текст.
- Не вигадуй події, імена, мотиви, стосунки або пояснення.
- Не розкривай і не передбачай нічого після поточної позиції читання.
- Не продовжуй історію.
- Не цитуй великі частини книжки.
- Не підсумовуй всю книжку.
- Не додавай зовнішні знання.
- Якщо тексту недостатньо, чесно напиши, що можна пригадати тільки недавній контекст.
- Тон: спокійний, теплий, корисний.
- Мова відповіді: {language_name}; якщо є сумнів, відповідай українською.
- Поверни тільки валідний JSON. Без Markdown, без пояснень, без тексту поза JSON.

Книжка:
- title: {request.book_title}
- book_type: {book_type}
- current_chunk_index: {request.current_chunk_index}
- bonus_type: {request.bonus_type}
- summary_so_far: {summary}

JSON schema:
{schema}

Попередні фрагменти перед поточною позицією:
{request.previous_chunks_text}
"""


def normalize_bonus_payload(payload: dict[str, Any], bonus_type: WelcomeBonusType) -> dict[str, Any]:
    normalized = dict(payload)
    normalized["type"] = bonus_type
    normalized.setdefault("title", _default_title(bonus_type))
    normalized.setdefault("continue_hint", "Можна спокійно продовжувати читання.")

    if bonus_type == "quick":
        normalized.setdefault("recap", "")
        normalized.setdefault("key_points", [])
    elif bonus_type == "fiction":
        normalized.setdefault("recap", "")
        normalized.setdefault("events", [])
        normalized.setdefault("characters", [])
    elif bonus_type == "nonfiction":
        normalized.setdefault("main_idea", "")
        normalized.setdefault("key_points", [])
    elif bonus_type == "characters":
        normalized.setdefault("recap", "")
        normalized.setdefault("characters", [])
    return normalized


def raw_text_payload(bonus_type: WelcomeBonusType, raw_text: str) -> dict[str, Any]:
    recap = raw_text.strip()
    if looks_like_json_fragment(recap):
        recap = "Не вдалося розібрати AI-нагадування. Можна спокійно повернутися до попереднього контексту."
    return {
        "type": bonus_type,
        "title": _default_title(bonus_type),
        "recap": recap or "Не вдалося розібрати AI-нагадування.",
        "continue_hint": "Можна спокійно продовжувати читання.",
    }


def fallback_bonus_payload(previous_text_preview: str) -> dict[str, Any]:
    return {
        "type": "fallback",
        "title": "Коротке нагадування",
        "recap": (
            "Не вдалося згенерувати AI-нагадування. Ось кілька попередніх фрагментів, "
            "щоб швидко згадати контекст."
        ),
        "previous_text_preview": previous_text_preview,
        "continue_hint": "Можна спокійно продовжувати читання.",
    }


def display_text_from_payload(payload: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ("recap", "main_idea"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())
    for key in ("key_points", "events"):
        value = payload.get(key)
        if isinstance(value, list):
            parts.extend(str(item).strip() for item in value[:4] if str(item).strip())
    hint = payload.get("continue_hint")
    if isinstance(hint, str) and hint.strip():
        parts.append(hint.strip())
    preview = payload.get("previous_text_preview")
    if not parts and isinstance(preview, str):
        parts.append(preview.strip())
    return "\n\n".join(parts).strip() or "Можна спокійно продовжувати читання."


def looks_like_json_fragment(text: str) -> bool:
    stripped = text.strip()
    if not stripped.startswith("{"):
        return False
    return parse_json_payload(stripped) is None


def _default_title(bonus_type: str) -> str:
    return {
        "quick": "Що було раніше",
        "fiction": "Що сталося раніше",
        "nonfiction": "Що важливо пам'ятати",
        "characters": "Хто є хто",
    }.get(bonus_type, "Коротке нагадування")


def _focus_for_bonus_type(bonus_type: WelcomeBonusType) -> str:
    return {
        "quick": "загальне коротке нагадування у 3-5 реченнях",
        "fiction": "недавні події, активна ситуація, персонажі і емоційний стан історії, якщо це видно з тексту",
        "nonfiction": "ключові ідеї, аргументи, поняття і те, що варто пам'ятати перед продовженням",
        "characters": "імена персонажів, хто вони і чому важливі зараз, тільки якщо це прямо видно з тексту",
    }[bonus_type]


def _schema_for_bonus_type(bonus_type: WelcomeBonusType) -> str:
    schemas = {
        "quick": {
            "type": "quick",
            "title": "Що було раніше",
            "recap": "3-5 коротких речень.",
            "key_points": ["point 1", "point 2"],
            "continue_hint": "Одне м'яке речення, що допомагає продовжити.",
        },
        "fiction": {
            "type": "fiction",
            "title": "Що сталося раніше",
            "recap": "3-5 речень переказу недавніх подій.",
            "events": ["recent event 1", "recent event 2", "recent event 3"],
            "characters": [{"name": "Character name", "context": "Why this character matters right now"}],
            "continue_hint": "Одне м'яке речення для повернення в історію.",
        },
        "nonfiction": {
            "type": "nonfiction",
            "title": "Що важливо пам'ятати",
            "main_idea": "Один короткий абзац з головною ідеєю.",
            "key_points": ["key idea 1", "key idea 2", "key idea 3"],
            "continue_hint": "Одне речення про те, від чого продовжується наступний розділ.",
        },
        "characters": {
            "type": "characters",
            "title": "Хто є хто",
            "recap": "Одне коротке речення про поточний контекст персонажів.",
            "characters": [
                {
                    "name": "Character name",
                    "description": "Who this person is based only on the provided text.",
                    "current_context": "Why they matter right now.",
                }
            ],
            "continue_hint": "Одне м'яке речення для повернення до читання.",
        },
    }
    return json.dumps(schemas[bonus_type], ensure_ascii=False, indent=2)
