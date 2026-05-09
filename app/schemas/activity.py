from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class StreakStatus(BaseModel):
    streak_days: int
    completed_today: bool
    just_completed_today: bool = False
    today: date
