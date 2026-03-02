# Development Guide

Руководство по настройке окружения и разработке.

---

## Требования

- **Python** 3.11+
- **Node.js** 18+
- **PostgreSQL** 15+
- **pnpm** или **npm**

---

## 1. Клонирование и окружение

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt

# Frontend
cd frontend
npm install   # или pnpm install
```

---

## 2. База данных

### Вариант A: Docker Compose (рекомендуется)

```bash
make db-up
# или: docker compose up -d postgres
```

### Вариант B: Локальный PostgreSQL

```bash
createdb seafarer
```

### Вариант C: Один контейнер Docker

```bash
docker run -d \
  --name seafarer-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=seafarer \
  -p 5432:5432 \
  postgres:15-alpine
```

### Миграции

```bash
cd backend
python -m alembic upgrade head
```

---

## 3. Переменные окружения

```bash
cp .env.example .env
# Отредактировать .env: BOT_TOKEN, DATABASE_URL, SECRET_KEY
```

---

## 4. Запуск

### Backend (API)

```bash
make api
# или: cd backend && uvicorn app.main:app --reload
```

API: http://localhost:8000  
Swagger: http://localhost:8000/docs

### Backend (Telegram Bot)

```bash
make bot
# или: cd backend && python -m app.bot.run
```

### Frontend

```bash
make frontend
# или: cd frontend && npm run dev
```

Frontend: http://localhost:3000

---

## 5. Тестирование TMA локально

1. Использовать [@webappbot](https://t.me/webappbot) или свой бот.
2. Указать `WEBAPP_URL` на ngrok или Cloudflare Tunnel, если нужен HTTPS.
3. В `ALLOWED_ORIGINS` добавить URL Mini App.

---

## 6. Частые проблемы

### `ModuleNotFoundError: No module named 'app'`

- Запускать из корня `backend/`
- Либо: `PYTHONPATH=backend uvicorn app.main:app`

### `connection refused` к PostgreSQL

- Проверить, что PostgreSQL запущен
- Проверить `DATABASE_URL` в `.env`

### initData validation fails

- Убедиться, что `BOT_TOKEN` совпадает с ботом, из которого открыт WebApp
- Проверить заголовок `X-Tg-Init-Data`

### CORS errors

- Добавить origin в `ALLOWED_ORIGINS`
- При локальной разработке: `http://localhost:3000`
