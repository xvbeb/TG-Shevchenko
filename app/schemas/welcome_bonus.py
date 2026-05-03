from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WelcomeBonusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    from_chunk_index: int
    to_chunk_index: int
    current_chunk_index: int
    text: str
    generated_by: str
    created_at: datetime
