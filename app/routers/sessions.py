from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.routers.dependencies import get_current_user
from app.schemas.session import ReadingSessionRead, SessionEnd, SessionStart
from app.services.sessions import end_session, start_session

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/start", response_model=ReadingSessionRead, status_code=201)
def start_reading_session(
    payload: SessionStart,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return start_session(db, current_user, payload)


@router.post("/end", response_model=ReadingSessionRead)
def end_reading_session(
    payload: SessionEnd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return end_session(db, current_user, payload)
