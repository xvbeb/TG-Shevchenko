from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import init_db
from app.routers import admin, books, sessions, users


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.db_auto_create:
        init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(admin.router)
app.include_router(books.router)
app.include_router(sessions.router)
app.include_router(users.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.mount("/", StaticFiles(directory="app/static", html=True), name="mini_app")
