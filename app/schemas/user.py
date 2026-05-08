from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: str
    username: Optional[str] = None
    display_name: Optional[str] = None
    preferences: dict[str, Any] = {}
    gentle_streak_days: int
    created_at: datetime


class UserPreferencesUpdate(BaseModel):
    language: Literal["ru", "uk"]
