from __future__ import annotations

import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

import pytest
from fastapi import HTTPException

from app.config import Settings
from app.routers.dependencies import dev_auth_is_allowed
from app.services.telegram_auth import extract_init_data_from_authorization, verify_telegram_init_data


BOT_TOKEN = "123456:test-token"


def _signed_init_data(*, user_id: int = 42, auth_date: int | None = None) -> str:
    pairs = {
        "auth_date": str(auth_date or int(time.time())),
        "query_id": "test-query",
        "user": json.dumps(
            {"id": user_id, "first_name": "Test", "last_name": "Reader", "username": "reader"},
            separators=(",", ":"),
        ),
    }
    data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(pairs.items()))
    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    pairs["hash"] = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return urlencode(pairs)


def test_valid_telegram_init_data_is_accepted() -> None:
    user = verify_telegram_init_data(_signed_init_data(), BOT_TOKEN)

    assert user.telegram_id == "42"
    assert user.username == "reader"
    assert user.display_name == "Test Reader"


def test_tampered_telegram_init_data_is_rejected() -> None:
    init_data = _signed_init_data().replace("test-query", "tampered-query")

    with pytest.raises(HTTPException) as exc_info:
        verify_telegram_init_data(init_data, BOT_TOKEN)

    assert exc_info.value.status_code == 401


def test_bearer_init_data_extraction() -> None:
    assert extract_init_data_from_authorization("Bearer signed-data") == "signed-data"
    assert extract_init_data_from_authorization("Basic signed-data") is None


def test_admin_ids_are_read_from_comma_separated_env_value() -> None:
    settings = Settings(_env_file=None, admin_telegram_ids="42, 77")

    assert settings.is_admin_telegram_id("42") is True
    assert settings.is_admin_telegram_id(77) is True
    assert settings.is_admin_telegram_id("999") is False


@pytest.mark.parametrize(
    ("environment", "enabled", "expected"),
    [("local", True, True), ("railway", True, False), ("production", True, False), ("local", False, False)],
)
def test_dev_auth_is_local_only(environment: str, enabled: bool, expected: bool) -> None:
    settings = Settings(_env_file=None, environment=environment, allow_dev_auth=enabled)

    assert dev_auth_is_allowed(settings) is expected
