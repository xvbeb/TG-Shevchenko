# ADHD Reader Mini App MVP

Backend + temporary Telegram Mini App UI for an ADHD-friendly reading app. The first goal is simple: open a book, read one small chunk, save progress, and return later with a short recap.

## Stack

- FastAPI for API and static Mini App files.
- SQLAlchemy + PostgreSQL for data.
- `aiogram` for the Telegram bot entrypoint.
- Plain HTML/CSS/JS for the temporary Mini App design.
- TXT, EPUB, FB2, and `.fb2.zip` imports.

## Project Structure

- `app/main.py` creates the FastAPI app, API routes, and static Mini App.
- `bot.py` runs the Telegram bot and sends the WebApp button.
- `app/static/` contains the temporary Mini App UI.
- `app/models/` contains SQLAlchemy tables.
- `app/schemas/` contains Pydantic request/response DTOs.
- `app/routers/` contains HTTP endpoints.
- `app/services/` contains parsing, auth, progress, sessions, and recap logic.

## Environment

Copy and edit config:

```bash
cp .env.example .env
```

Required for Telegram:

```env
TELEGRAM_BOT_TOKEN="123456:ABC..."
TELEGRAM_WEBAPP_URL="https://your-public-mini-app-domain"
ALLOW_DEV_AUTH=true
```

For local API testing without Telegram, `ALLOW_DEV_AUTH=true` lets the temporary frontend use a dev user. Real Telegram Mini App requests use `Telegram.WebApp.initData` and are verified with `TELEGRAM_BOT_TOKEN`.

For Railway PostgreSQL from your local machine, use:

```env
DATABASE_PUBLIC_URL="postgresql://postgres:password@host.proxy.rlwy.net:12345/railway"
DB_AUTO_CREATE=true
```

`DATABASE_URL` is for services running inside Railway. `DATABASE_PUBLIC_URL` is for your laptop through Railway TCP proxy.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Locally

Run API and Mini App:

```bash
uvicorn app.main:app --reload
```

Open locally:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/docs
```

Run Telegram bot in a second terminal:

```bash
source .venv/bin/activate
python bot.py
```

In Telegram, send `/start` to the bot and tap `Открыть reader`.

## Temporary Railway Deployment

This deploys only the FastAPI web service: API + static Telegram Mini App page. The `aiogram` bot can still run locally, or later as a separate Railway worker service.

Railway uses [config as code](https://docs.railway.com/config-as-code/reference) from `railway.toml`. The current start command is:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Deploy steps:

1. Push this project to GitHub.
2. In Railway, create a new project from the GitHub repo.
3. Add a PostgreSQL service in the same Railway project.
4. In the FastAPI service variables, set:

```env
DATABASE_URL="${{Postgres.DATABASE_URL}}"
DB_AUTO_CREATE=true
TELEGRAM_BOT_TOKEN="123456:ABC..."
TELEGRAM_WEBAPP_URL="https://your-service.up.railway.app"
ALLOW_DEV_AUTH=false
ENVIRONMENT=railway
```

5. Deploy the FastAPI service.
6. Open:

```text
https://your-service.up.railway.app/health
```

Expected response:

```json
{"status":"ok"}
```

7. Open the Mini App page:

```text
https://your-service.up.railway.app/
```

8. Use that same public HTTPS URL in Telegram:

```env
TELEGRAM_WEBAPP_URL="https://your-service.up.railway.app"
```

Then restart `bot.py` locally, or set the Mini App URL in BotFather/Menu Button.

Notes:

- `app.main:app` is the correct import path.
- Static frontend files are served by FastAPI from `app/static`.
- CORS middleware is not needed for this temporary deploy because the frontend and API share the same Railway origin.
- Keep `DB_AUTO_CREATE=true` only for this temporary prototype. Replace it with Alembic migrations before real users.

## Ngrok Local Testing

Telegram Mini Apps need an HTTPS URL. Point ngrok to the local FastAPI server:

```text
ngrok http 8000
```

Then set:

```env
TELEGRAM_WEBAPP_URL="https://your-ngrok-domain.ngrok-free.app"
```

Restart both:

```bash
uvicorn app.main:app --reload
python bot.py
```

## API Routes

- `POST /books/upload`
- `GET /books`
- `GET /books/{book_id}`
- `GET /books/{book_id}/read`
- `POST /books/{book_id}/progress`
- `GET /books/{book_id}/welcome-bonus`
- `POST /sessions/start`
- `POST /sessions/end`
- `GET /health`

## MVP Notes

The frontend is intentionally temporary and dependency-free. Once the reading flow feels right inside Telegram, it can be replaced with React/Vite or another frontend without changing the API shape too much.

The current “AI-помощник” is a rule-based placeholder with three recap depths:

- `quick`: a short orientation.
- `story`: a more event-like recap.
- `deep`: a fuller recap from more previous chunks.

The API shape is ready for replacing this service with a real AI summarizer later.
