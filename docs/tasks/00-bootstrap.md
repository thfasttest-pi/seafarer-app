# 00 — Bootstrap Project

Чеклист первоначальной настройки проекта.

---

## 1. Backend Bootstrap

- [ ] Создать `backend/` и структуру:
  - [ ] `app/__init__.py`
  - [ ] `app/main.py` (FastAPI app)
  - [ ] `app/core/` — settings, db, security, errors
  - [ ] `app/models/` — base.py, user, job, company
  - [ ] `app/schemas/` — DTOs
  - [ ] `app/services/` — placeholder
  - [ ] `app/api/` — routers
  - [ ] `app/bot/` — Aiogram handlers
- [ ] `requirements.txt` с зависимостями
- [ ] `pyproject.toml` или `setup.py` (опционально)
- [ ] Alembic: `alembic init`
- [ ] Health check endpoint: `GET /health`
- [ ] Глобальная зависимость initData (заглушка до полной реализации)

---

## 2. Frontend Bootstrap

- [ ] Создать Next.js 14 (App Router): `npx create-next-app@14`
- [ ] Установить: Tailwind, @twa-dev/sdk, SWR или TanStack Query
- [ ] Структура:
  - [ ] `src/lib/tma.ts` — WebApp wrapper
  - [ ] `src/lib/api.ts` — API client + initData header
  - [ ] `src/hooks/` — useJobs, useApply и т.д.
  - [ ] `src/components/` — layout, job card, search form
- [ ] Страница `/` с минимальным UI
- [ ] Конфигурация для TMA (viewport, theme)

---

## 3. Database

- [ ] PostgreSQL running locally или Docker
- [ ] Базовые модели: User, Company, Job
- [ ] Alembic: первая миграция
- [ ] `alembic upgrade head` успешно

---

## 4. Infra & Config

- [x] `.gitignore` — Python, Node, .env, linters, Docker
- [x] `.editorconfig` — единый стиль кода
- [x] `docker-compose.yml` — PostgreSQL 15
- [x] `Makefile` — make db-up, migrate, api, bot, frontend
- [ ] `.env` из `.env.example` (локально, не коммитить)
- [ ] README: команды `make api`, `make migrate`, etc.

---

## 5. Verification

- [ ] `uvicorn app.main:app --reload` — API отвечает
- [ ] `GET /health` → 200
- [ ] `npm run dev` — frontend стартует
- [ ] /docs (Swagger) доступен при ENABLE_DOCS=true

---

**Следующий шаг:** [01-api-auth.md](01-api-auth.md) — полная реализация initData validation
