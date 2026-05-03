from __future__ import annotations

import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import parse_qsl

from fastapi import HTTPException, status


@dataclass
class TelegramWebAppUser:
    telegram_id: str
    username: Optional[str] = None
    display_name: Optional[str] = None


def verify_telegram_init_data(init_data: str, bot_token: str, max_age_seconds: int = 86400) -> TelegramWebAppUser:
    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = pairs.pop("hash", None)
    if not received_hash:
        raise _unauthorized("Telegram initData hash is missing")

    auth_date = _read_auth_date(pairs)
    if max_age_seconds and time.time() - auth_date > max_age_seconds:
        raise _unauthorized("Telegram initData is too old")

    data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(pairs.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise _unauthorized("Telegram initData signature is invalid")

    return _read_user(pairs)


def extract_init_data_from_authorization(authorization: Optional[str]) -> Optional[str]:
    if not authorization:
        return None
    scheme, _, value = authorization.partition(" ")
    if scheme.lower() != "bearer" or not value:
        return None
    return value


def _read_auth_date(pairs: dict[str, str]) -> int:
    try:
        return int(pairs["auth_date"])
    except (KeyError, ValueError) as exc:
        raise _unauthorized("Telegram initData auth_date is invalid") from exc


def _read_user(pairs: dict[str, str]) -> TelegramWebAppUser:
    try:
        payload: dict[str, Any] = json.loads(pairs["user"])
    except (KeyError, json.JSONDecodeError) as exc:
        raise _unauthorized("Telegram initData user payload is invalid") from exc

    telegram_id = payload.get("id")
    if telegram_id is None:
        raise _unauthorized("Telegram user id is missing")

    first_name = payload.get("first_name") or ""
    last_name = payload.get("last_name") or ""
    display_name = " ".join(part for part in [first_name, last_name] if part).strip() or None

    return TelegramWebAppUser(
        telegram_id=str(telegram_id),
        username=payload.get("username"),
        display_name=display_name,
    )


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
