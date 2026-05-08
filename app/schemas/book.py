from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: Optional[str] = None
    source_type: str
    original_filename: Optional[str] = None
    cover_image_data_url: Optional[str] = None
    total_words: int
    total_chunks: int
    uploaded_at: datetime


class BookDetail(BookRead):
    current_chunk_index: int = 0
    last_opened_at: Optional[datetime] = None


class BookChunkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chunk_index: int
    text: str
    word_count: int


class ReadResponse(BaseModel):
    book: BookRead
    chunk: Optional[BookChunkRead]
    current_chunk_index: int
    total_chunks: int
    has_previous: bool
    has_next: bool


class ReadRangeResponse(BaseModel):
    book: BookRead
    chunks: list[BookChunkRead]
    start_chunk_index: int
    end_chunk_index: int
    total_chunks: int
    has_previous: bool
    has_next: bool


class BookSearchResult(BaseModel):
    chunk_index: int
    page_number: int
    word_count: int
    snippet: str


class BookSearchResponse(BaseModel):
    query: str
    results: list[BookSearchResult]
