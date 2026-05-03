from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProgressUpdate(BaseModel):
    current_chunk_index: int = Field(ge=0)
    chunks_read: int = Field(default=0, ge=0)
    words_read: int = Field(default=0, ge=0)


class ReadingProgressRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    current_chunk_index: int
    chunks_read: int
    words_read: int
    last_opened_at: Optional[datetime] = None
    updated_at: datetime
