from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ReadingActivity, User
from app.schemas.activity import StreakStatus


def get_streak_status(db: Session, user: User, just_completed_today: bool = False) -> StreakStatus:
    today = _today()
    completed_today = _activity_exists(db, user, today)
    return StreakStatus(
        streak_days=_calculate_streak(db, user, today),
        completed_today=completed_today,
        just_completed_today=just_completed_today,
        today=today,
    )


def record_reading_activity(db: Session, user: User) -> StreakStatus:
    today = _today()
    activity = db.scalar(
        select(ReadingActivity).where(ReadingActivity.user_id == user.id, ReadingActivity.activity_date == today)
    )
    just_completed_today = activity is None
    if activity:
        activity.reads_count += 1
    else:
        db.add(ReadingActivity(user_id=user.id, activity_date=today, reads_count=1))

    db.flush()
    user.gentle_streak_days = _calculate_streak(db, user, today)
    db.commit()
    db.refresh(user)
    return get_streak_status(db, user, just_completed_today=just_completed_today)


def _calculate_streak(db: Session, user: User, today: date) -> int:
    activity_dates = set(
        db.scalars(
            select(ReadingActivity.activity_date)
            .where(ReadingActivity.user_id == user.id, ReadingActivity.activity_date <= today)
            .order_by(ReadingActivity.activity_date.desc())
        )
    )
    streak = 0
    cursor = today
    while cursor in activity_dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def _activity_exists(db: Session, user: User, day: date) -> bool:
    return (
        db.scalar(select(ReadingActivity.id).where(ReadingActivity.user_id == user.id, ReadingActivity.activity_date == day))
        is not None
    )


def _today() -> date:
    return datetime.now(timezone.utc).date()
