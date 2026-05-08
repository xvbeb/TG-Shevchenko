from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()

engine = create_engine(settings.sqlalchemy_database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    # MVP convenience for local/Railway prototypes. Replace with Alembic before production.
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _ensure_prototype_columns()


def _ensure_prototype_columns() -> None:
    inspector = inspect(engine)
    if "books" not in inspector.get_table_names():
        return

    book_columns = {column["name"] for column in inspector.get_columns("books")}
    if "cover_image_data_url" not in book_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE books ADD COLUMN cover_image_data_url TEXT"))
