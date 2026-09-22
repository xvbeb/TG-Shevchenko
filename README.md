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
ADMIN_TELEGRAM_IDS="123456789"
ALLOW_DEV_AUTH=true
```

For local API testing without Telegram, `ALLOW_DEV_AUTH=true` lets the temporary frontend use a dev user. It only works when `ENVIRONMENT=local`; all other environments reject development headers even if the flag is accidentally enabled. The default is `false`. Real Telegram Mini App requests use `Telegram.WebApp.initData` and are verified with `TELEGRAM_BOT_TOKEN`.

`ADMIN_TELEGRAM_IDS` is a comma-separated list of Telegram user IDs allowed to use admin features. Keep real IDs in `.env` or Railway variables, never in source code.

For Railway PostgreSQL from your local machine, use:

```env
DATABASE_PUBLIC_URL="postgresql://postgres:password@host.proxy.rlwy.net:12345/railway"
DB_AUTO_CREATE=true
```

`DATABASE_URL` is for services running inside Railway. `DATABASE_PUBLIC_URL` is for your laptop through Railway TCP proxy.

Welcome Bonus recaps use a provider-switchable AI service. For MVP testing the default provider is Gemini:

```env
AI_PROVIDER=gemini
AI_MODEL=gemini-2.5-flash
GEMINI_API_KEY="your-google-ai-studio-key"
WELCOME_BONUS_PROMPT_VERSION=v1
WELCOME_BONUS_CONTEXT_CHUNKS=10
WELCOME_BONUS_MAX_CONTEXT_CHARS=12000
```

To get a Gemini API key:

1. Open [Google AI Studio](https://aistudio.google.com/).
2. Sign in with a Google account.
3. Open the API key section and create a key.
4. Add the key to `.env` locally or to Railway variables as `GEMINI_API_KEY`.

Keep API keys out of Git. `.env.example` intentionally leaves `GEMINI_API_KEY` empty.

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
ADMIN_TELEGRAM_IDS="123456789"
ALLOW_DEV_AUTH=false
ENVIRONMENT=railway
AI_PROVIDER=gemini
AI_MODEL=gemini-2.5-flash
GEMINI_API_KEY="your-google-ai-studio-key"
WELCOME_BONUS_PROMPT_VERSION=v1
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

## Testing Telegram Fullscreen UX

1. Run FastAPI locally or deploy it to Railway.
2. Expose it through HTTPS:

```bash
ngrok http 8000
```

3. Set the public URL:

```env
TELEGRAM_WEBAPP_URL="https://your-domain.ngrok-free.app"
```

4. Restart the bot:

```bash
python bot.py
```

5. In Telegram, send `/start`, open the Mini App, and check:

- the app expands after opening;
- the top area stays fixed;
- the bottom navigation stays visible;
- only the current screen scrolls;
- Home, Library, Reader, Progress, and Settings switch without page reloads;
- Telegram dark/light theme colors are reflected where Telegram exposes theme params.

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

## Tests

Run the local automated suite:

```bash
pytest -q
```

The suite covers Telegram Mini App signature verification, local-only development authentication, AI JSON parsing, admin ID configuration, and Welcome Bonus cache reuse. Live Gemini access is intentionally checked separately so routine tests remain deterministic and do not spend API quota.

## MVP Notes

The frontend is intentionally temporary and dependency-free. Once the reading flow feels right inside Telegram, it can be replaced with React/Vite or another frontend without changing the API shape too much.

Welcome Bonus now uses the AI service abstraction in `app/services/ai.py`. The current MVP provider is Gemini, and the business logic calls `generate_welcome_bonus(...)` so another provider can be added later without rewriting the recap endpoint.

The endpoint is:

```text
GET /books/{book_id}/welcome-bonus?type=quick
```

Supported `type` values:

- `quick`: short general reminder.
- `fiction`: recent events, active situation, and characters when present.
- `nonfiction`: key ideas, arguments, concepts, and what to remember before continuing.
- `characters`: who is who in the recent context.

The service sends only the book title, optional book type, current chunk index, selected bonus type, UI language, and previous chunks within `WELCOME_BONUS_MAX_CONTEXT_CHARS`. It never sends the whole book or future chunks. Results are cached in `welcome_bonuses` by user, book, current chunk index, bonus type, model, and prompt version.

Gemini is asked to return valid JSON only. If it returns invalid JSON, the app tries to extract JSON; if that still fails, the raw text is stored as a safe recap. If the AI provider fails or the key is missing, the endpoint returns a fallback payload instead of crashing the app.

Manual test examples:

```bash
curl -s -H "X-Telegram-User-Id: dev-user-1" "http://127.0.0.1:8000/books/1/welcome-bonus?type=quick"
curl -s -H "X-Telegram-User-Id: dev-user-1" "http://127.0.0.1:8000/books/1/welcome-bonus?type=fiction"
curl -s -H "X-Telegram-User-Id: dev-user-1" "http://127.0.0.1:8000/books/1/welcome-bonus?type=nonfiction"
curl -s -H "X-Telegram-User-Id: dev-user-1" "http://127.0.0.1:8000/books/1/welcome-bonus?type=characters"
```

To test fallback behavior, temporarily unset `GEMINI_API_KEY` and repeat one of the requests. The response should include `payload.type = "fallback"` and `model` should start with `fallback:`.

AI provider note: do not send private user books to a free AI tier unless the user understands the provider's data handling policies.
