from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


def get_or_create_telegram_user(
    db: Session,
    telegram_id: str,
    username: Optional[str] = None,
    display_name: Optional[str] = None,
) -> User:
    user = db.scalar(select(User).where(User.telegram_id == telegram_id))
    if user:
        changed = False
        if username and user.username != username:
            user.username = username
            changed = True
        if display_name and user.display_name != display_name:
            user.display_name = display_name
            changed = True
        if changed:
            db.commit()
            db.refresh(user)
        return user

    user = User(telegram_id=telegram_id, username=username, display_name=display_name, preferences={})
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
