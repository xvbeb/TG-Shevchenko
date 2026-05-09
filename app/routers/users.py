from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.routers.dependencies import get_current_user
from app.schemas.activity import StreakStatus
from app.schemas.user import UserPreferencesUpdate, UserRead
from app.services.activity import get_streak_status
from app.services.users import update_user_language

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/me/streak", response_model=StreakStatus)
def get_my_streak(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_streak_status(db, current_user)


@router.patch("/me/preferences", response_model=UserRead)
def update_preferences(
    payload: UserPreferencesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_user_language(db, current_user, payload.language)
