from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class AdminStats(BaseModel):
    total_users: int
    total_books: int
    total_welcome_bonuses: int
    active_progress_rows: int


class AdminUserRow(BaseModel):
    id: int
    telegram_id: str
    username: Optional[str] = None
    display_name: Optional[str] = None
    books_added: int
    welcome_bonuses_used: int
    created_at: datetime


class AdminProgressRow(BaseModel):
    user_id: int
    telegram_id: str
    username: Optional[str] = None
    display_name: Optional[str] = None
    book_id: int
    book_title: str
    book_author: Optional[str] = None
    current_chunk_index: int
    current_page: int
    total_chunks: int
    progress_percent: float
    last_opened_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AdminBookRow(BaseModel):
    id: int
    title: str
    author: Optional[str] = None
    original_filename: Optional[str] = None
    source_type: str
    total_words: int
    total_chunks: int
    uploaded_at: datetime
    owner_user_id: int
    owner_telegram_id: str
    owner_username: Optional[str] = None
    owner_display_name: Optional[str] = None


class AdminSummary(BaseModel):
    stats: AdminStats
    users: list[AdminUserRow]
    progress: list[AdminProgressRow]
    books: list[AdminBookRow]


class AdminMessageRequest(BaseModel):
    audience: Literal["user", "all"]
    text: str = Field(min_length=1, max_length=2000)
    user_id: Optional[int] = None


class AdminMessageResult(BaseModel):
    user_id: int
    telegram_id: str
    ok: bool
    error: Optional[str] = None


class AdminMessageResponse(BaseModel):
    sent: int
    failed: int
    results: list[AdminMessageResult]


class AdminRechunkResponse(BaseModel):
    book_id: int
    old_total_chunks: int
    new_total_chunks: int
    total_words: int
    progress_rows_updated: int
