from __future__ import annotations

from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import User
from app.services.telegram_auth import extract_init_data_from_authorization, verify_telegram_init_data
from app.services.users import get_or_create_telegram_user


def get_current_user(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
    telegram_id: Optional[str] = Header(default=None, alias="X-Telegram-User-Id"),
    username: Optional[str] = Header(default=None, alias="X-Telegram-Username"),
    display_name: Optional[str] = Header(default=None, alias="X-Telegram-Display-Name"),
) -> User:
    settings = get_settings()
    init_data = extract_init_data_from_authorization(authorization)
    if init_data:
        if not settings.telegram_bot_token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="TELEGRAM_BOT_TOKEN is not configured",
            )
        telegram_user = verify_telegram_init_data(init_data, settings.telegram_bot_token)
        return get_or_create_telegram_user(
            db,
            telegram_id=telegram_user.telegram_id,
            username=telegram_user.username,
            display_name=telegram_user.display_name,
        )

    if not settings.allow_dev_auth or not telegram_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Telegram Mini App initData",
        )
    return get_or_create_telegram_user(db, telegram_id=telegram_id, username=username, display_name=display_name)
