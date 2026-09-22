from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_LOCAL_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/adhd_reader"


class Settings(BaseSettings):
    app_name: str = "TGSH"
    environment: str = "local"
    database_url: Optional[str] = None
    database_public_url: Optional[str] = None
    db_auto_create: bool = True
    telegram_bot_token: Optional[str] = None
    telegram_webapp_url: str = "https://reader.localhost"
    allow_dev_auth: bool = False
    admin_telegram_ids: str = ""
    max_upload_mb: int = 20
    default_chunk_words: int = 220
    ai_provider: str = "gemini"
    ai_model: str = "gemini-2.5-flash"
    gemini_api_key: Optional[str] = None
    welcome_bonus_prompt_version: str = "v1"
    welcome_bonus_context_chunks: int = 10
    welcome_bonus_max_context_chars: int = 12000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def sqlalchemy_database_url(self) -> str:
        # Railway exposes DATABASE_PUBLIC_URL for local/external connections.
        # SQLAlchemy needs the +psycopg driver marker because this project uses psycopg v3.
        value = self.database_public_url or self.database_url or DEFAULT_LOCAL_DATABASE_URL
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value

    @property
    def admin_telegram_id_set(self) -> set[str]:
        return {value.strip() for value in self.admin_telegram_ids.split(",") if value.strip()}

    def is_admin_telegram_id(self, telegram_id: str | int | None) -> bool:
        return telegram_id is not None and str(telegram_id) in self.admin_telegram_id_set


@lru_cache
def get_settings() -> Settings:
    return Settings()
