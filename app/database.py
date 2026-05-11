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
    table_names = set(inspector.get_table_names())
    if "books" not in table_names:
        return

    book_columns = {column["name"] for column in inspector.get_columns("books")}
    if "cover_image_data_url" not in book_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE books ADD COLUMN cover_image_data_url TEXT"))

    if "welcome_bonuses" not in table_names:
        return

    bonus_columns = {column["name"] for column in inspector.get_columns("welcome_bonuses")}
    expected_cache_columns = ["user_id", "book_id", "current_chunk_index", "bonus_type", "model", "prompt_version"]
    existing_cache_constraint = next(
        (
            constraint
            for constraint in inspector.get_unique_constraints("welcome_bonuses")
            if constraint.get("name") == "uq_welcome_bonus_cache"
        ),
        None,
    )

    with engine.begin() as connection:
        if "bonus_type" not in bonus_columns:
            connection.execute(
                text("ALTER TABLE welcome_bonuses ADD COLUMN bonus_type VARCHAR(32) DEFAULT 'quick' NOT NULL")
            )
        if "payload" not in bonus_columns:
            connection.execute(text("ALTER TABLE welcome_bonuses ADD COLUMN payload JSON DEFAULT '{}' NOT NULL"))
        if "model" not in bonus_columns:
            connection.execute(
                text("ALTER TABLE welcome_bonuses ADD COLUMN model VARCHAR(128) DEFAULT 'rule_based' NOT NULL")
            )
        if "prompt_version" not in bonus_columns:
            connection.execute(
                text(
                    "ALTER TABLE welcome_bonuses ADD COLUMN prompt_version VARCHAR(64) DEFAULT 'rule_based_v1' NOT NULL"
                )
            )
        if engine.dialect.name == "postgresql":
            if existing_cache_constraint is None or existing_cache_constraint.get("column_names") != expected_cache_columns:
                connection.execute(text("ALTER TABLE welcome_bonuses DROP CONSTRAINT IF EXISTS uq_welcome_bonus_cache"))
                connection.execute(
                    text(
                        """
                        DELETE FROM welcome_bonuses old
                        USING welcome_bonuses newer
                        WHERE old.id < newer.id
                          AND old.user_id = newer.user_id
                          AND old.book_id = newer.book_id
                          AND old.current_chunk_index = newer.current_chunk_index
                          AND old.bonus_type = newer.bonus_type
                          AND old.model = newer.model
                          AND old.prompt_version = newer.prompt_version
                        """
                    )
                )
                connection.execute(
                    text(
                        "ALTER TABLE welcome_bonuses ADD CONSTRAINT uq_welcome_bonus_cache "
                        "UNIQUE (user_id, book_id, current_chunk_index, bonus_type, model, prompt_version)"
                    )
                )
