# ТГШ — читання без перевантаження 📚

**ТГШ** — Telegram Mini App для читання книжок короткими фрагментами з AI-нагадуванням контексту, збереженням прогресу та фокусом на комфортному поверненні до читання.

Ідея проєкту проста: замість необхідності щоразу згадувати, де ти зупинився і що відбувалося раніше, застосунок зберігає прогрес та може коротко відновити контекст перед продовженням читання.

## ✨ Можливості

* 📖 читання книжок невеликими фрагментами;
* 📚 підтримка `TXT`, `EPUB`, `FB2` та `.fb2.zip`;
* 🤖 AI-нагадування контексту перед продовженням читання;
* 💾 автоматичне збереження прогресу;
* ⏱ відстеження сесій читання;
* 🔥 система прогресу та streaks;
* 🎯 Focus Mode для зменшення візуального навантаження;
* 📱 повноцінний інтерфейс всередині Telegram Mini Apps;
* 🔐 авторизація через Telegram Mini App `initData`;
* ⚡ кешування AI-відповідей для зменшення затримок та кількості API-запитів.

## 🤖 AI Welcome Bonus

Одна з головних функцій ТГШ — **Welcome Bonus**.

Коли користувач повертається до книжки після перерви, застосунок може сформувати коротке нагадування про вже прочитаний контекст.

Доступні декілька режимів:

* **Quick** — коротке загальне нагадування;
* **Fiction** — останні події, поточна ситуація та важливі персонажі;
* **Non-fiction** — ключові ідеї, аргументи та поняття;
* **Characters** — хто є хто серед персонажів останнього контексту.

AI отримує лише попередні фрагменти відносно поточної позиції користувача.

**Майбутні частини книжки не передаються**, тому recap не повинен містити спойлерів із тексту, який користувач ще не прочитав.

### Кешування

Згенеровані результати зберігаються в PostgreSQL.

Кеш враховує:

* користувача;
* книжку;
* поточний фрагмент;
* тип recap;
* AI-модель;
* версію prompt.

Тому повторне відкриття тієї самої позиції не потребує нового AI-запиту.

Якщо AI-провайдер недоступний або API-ключ не налаштований, застосунок повертає fallback-відповідь замість падіння endpoint.

## 🏗 Архітектура

Проєкт складається з декількох основних частин:

```text
Telegram
   │
   ├── aiogram bot
   │
   ▼
Telegram Mini App
   │
   ▼
FastAPI
   │
   ├── Authentication
   ├── Books
   ├── Reading progress
   ├── Reading sessions
   └── AI Welcome Bonus
          │
          ▼
      AI Provider
          │
          ▼
        Gemini

FastAPI
   │
   ▼
PostgreSQL
```

Backend побудований так, щоб бізнес-логіка не залежала безпосередньо від конкретного AI-провайдера.

AI-рівень винесений в окрему абстракцію, тому Gemini можна замінити або доповнити іншим провайдером без переписування основної логіки читання.

## 🛠 Технології

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* PostgreSQL

### Telegram

* aiogram
* Telegram Bot API
* Telegram Mini Apps
* Telegram `initData` authentication

### AI

* Gemini API
* provider abstraction
* prompt versioning
* response caching
* fallback handling

### Frontend

* HTML
* CSS
* JavaScript
* Telegram Mini Apps API

### Infrastructure

* Railway
* PostgreSQL
* ngrok для локального тестування Mini App

## 📂 Структура проєкту

```text
TG-Shevchenko/
│
├── app/
│   ├── models/       # SQLAlchemy models
│   ├── routers/      # FastAPI endpoints
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # business logic, AI, auth, parsing
│   ├── static/       # Telegram Mini App frontend
│   └── main.py       # FastAPI application
│
├── tests/            # automated tests
├── bot.py            # aiogram bot
├── requirements.txt
├── railway.toml
└── .env.example
```

## 📚 Робота з книжками

Підтримуються:

```text
.txt
.epub
.fb2
.fb2.zip
```

Після імпорту текст розбивається на фрагменти, які використовуються reader-інтерфейсом та системою AI recap.

Позиція користувача зберігається в базі даних, тому читання можна продовжити з того самого місця після повторного відкриття застосунку.

## 🔐 Telegram Authentication

У production-запитах використовується `Telegram.WebApp.initData`.

Backend перевіряє підпис Telegram за допомогою токена бота перед тим, як довіряти даним користувача.

Для локальної розробки передбачений окремий development-режим:

```env
ALLOW_DEV_AUTH=true
ENVIRONMENT=local
```

Development authentication дозволена лише в локальному environment.

## 🌐 API

Основні endpoints:

```text
POST /books/upload
GET  /books
GET  /books/{book_id}
GET  /books/{book_id}/read
POST /books/{book_id}/progress

GET  /books/{book_id}/welcome-bonus

POST /sessions/start
POST /sessions/end

GET  /health
```

Інтерактивна документація FastAPI доступна локально:

```text
http://127.0.0.1:8000/docs
```

## 🚀 Локальний запуск

### 1. Клонування

```bash
git clone https://github.com/xvbeb/TG-Shevchenko.git
cd TG-Shevchenko
```

### 2. Virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment

```bash
cp .env.example .env
```

Основні змінні:

```env
TELEGRAM_BOT_TOKEN=
TELEGRAM_WEBAPP_URL=

DATABASE_URL=

AI_PROVIDER=gemini
AI_MODEL=gemini-2.5-flash
GEMINI_API_KEY=

ALLOW_DEV_AUTH=false
```

API-ключі та токени не повинні зберігатися в Git.

### 5. FastAPI

```bash
uvicorn app.main:app --reload
```

Після запуску:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/docs
```

### 6. Telegram bot

В іншому терміналі:

```bash
source .venv/bin/activate
python bot.py
```

## 📱 Локальне тестування Telegram Mini App

Telegram Mini Apps потребують HTTPS.

Для локальної розробки можна використати ngrok:

```bash
ngrok http 8000
```

Після цього HTTPS URL потрібно вказати в:

```env
TELEGRAM_WEBAPP_URL=https://your-domain.ngrok-free.app
```

і перезапустити bot та FastAPI.

## 🧪 Tests

Автоматичні тести запускаються через:

```bash
pytest -q
```

Тести перевіряють, зокрема:

* Telegram Mini App signature verification;
* обмеження development authentication;
* парсинг AI JSON-відповідей;
* конфігурацію admin IDs;
* повторне використання Welcome Bonus cache.

Live-запити до Gemini не є частиною звичайного test suite, щоб тести залишалися детермінованими та не витрачали API quota.

## 🚂 Deployment

Проєкт підготовлений для deployment на Railway.

FastAPI запускається командою:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Конфігурація знаходиться в:

```text
railway.toml
```

Для production використовуються environment variables Railway та PostgreSQL database service.

Health check:

```text
GET /health
```

Очікувана відповідь:

```json
{
  "status": "ok"
}
```

## 💡 Навіщо я створив ТГШ

Великі полотна тексту та необхідність згадувати контекст після перерви можуть створювати зайвий бар'єр перед тим, як просто продовжити читання.

ТГШ — експеримент із тим, як зробити цей процес простішим: розбити книжку на комфортні фрагменти, запам'ятати позицію користувача та за потреби швидко нагадати вже прочитане.

Мета проєкту — не скоротити книжку до AI-summary, а навпаки — **допомогти повернутися до самого читання**.
