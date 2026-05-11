from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class WelcomeBonusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    from_chunk_index: int
    to_chunk_index: int
    current_chunk_index: int
    bonus_type: str
    text: str
    payload: dict[str, Any]
    generated_by: str
    model: str
    prompt_version: str
    created_at: datetime
