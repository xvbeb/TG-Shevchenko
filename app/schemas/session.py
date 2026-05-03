from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SessionStart(BaseModel):
    book_id: int
    planned_minutes: Optional[int] = Field(default=None, ge=1, le=60)
    start_chunk_index: Optional[int] = Field(default=None, ge=0)


class SessionEnd(BaseModel):
    session_id: int
    end_chunk_index: int = Field(ge=0)
    chunks_read: int = Field(default=0, ge=0)
    words_read: int = Field(default=0, ge=0)


class ReadingSessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    planned_minutes: Optional[int] = None
    start_chunk_index: int
    end_chunk_index: Optional[int] = None
    chunks_read: int
    words_read: int
    started_at: datetime
    ended_at: Optional[datetime] = None
