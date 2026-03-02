# SEAFARER APP — Architecture

Полная архитектурная спецификация системы.

---

## 1. System Overview

**Seafarer App** — Fullstack Telegram Mini App для поиска вакансий моряками. Состоит из:

| Component | Tech | Назначение |
|-----------|------|------------|
| **Telegram Bot** | Aiogram 3.x | Точка входа, запуск Mini App, команды |
| **Web App (TMA)** | Next.js 14 | UI в WebView — поиск, отклики |
| **API** | FastAPI | REST API для TMA, валидация initData |
| **Database** | PostgreSQL | User, Job, Company, Application |
| **Shared** | Models, Schemas, Services | Общая логика для Bot и API |

```
┌─────────────────────────────────────────────────────────────────┐
│                     TELEGRAM CLIENT                               │
│  ┌─────────────┐                    ┌─────────────────────────┐  │
│  │   Bot Chat  │ ── /start ───────> │  Mini App (WebView)     │  │
│  │   Commands  │                    │  Next.js + TWA SDK      │  │
│  └─────────────┘                    └───────────┬─────────────┘  │
│         │                                        │                │
└─────────┼────────────────────────────────────────┼────────────────┘
          │                                        │
          │ Aiogram                                │ X-Tg-Init-Data
          ▼                                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (Python)                             │
│  ┌─────────────┐                    ┌─────────────────────────┐  │
│  │   Bot       │                    │   FastAPI API           │  │
│  │   Handlers  │                    │   initData → RBAC →     │  │
│  └──────┬──────┘                    │   Service → DB          │  │
│         │                           └───────────┬─────────────┘  │
│         │                                       │                │
│         └───────────────────┬───────────────────┘                │
│                             │                                     │
│                    ┌────────▼────────┐                            │
│                    │  Services       │  (business logic)           │
│                    │  Models/Schemas │  (shared)                   │
│                    └────────┬────────┘                            │
│                             │                                     │
└─────────────────────────────┼─────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    └─────────────────┘
```

---

## 2. Main Flow (TMA → initData → API → DB)

```
Telegram Mini App (WebView)
        ↓
WebApp.initData (signed payload from Telegram)
        ↓  (заголовок X-Tg-Init-Data)
FastAPI dependency: validate initData (HMAC-SHA256)
        ↓
Resolve/upsert User in DB by telegram_user_id
        ↓
Attach current_user to request
        ↓
Rate limit check (by user_id)
        ↓
Router → Service layer (business logic)
        ↓
SQLAlchemy AsyncSession
        ↓
PostgreSQL
        ↓
Response: Pydantic schema (response_model)
```

---

## 3. initData Validation (HMAC)

**Критично:** Каждый защищённый endpoint требует валидный initData.

| Шаг | Действие |
|-----|----------|
| 1 | Клиент отправляет `X-Tg-Init-Data` (строка из `WebApp.initData`) |
| 2 | Бэкенд парсит key=value пары, строит data-check-string |
| 3 | Вычисляет HMAC-SHA256(data_check_string, BOT_TOKEN) |
| 4 | Сравнивает с hash из initData |
| 5 | Проверяет auth_date (не старше N минут) |
| 6 | Извлекает user_id → ищет/создаёт User в DB |
| 7 | Прикрепляет `current_user` к request.state |

**Запрещено:**
- Логировать raw initData
- Возвращать initData в ответах
- Использовать endpoints без этой зависимости (кроме /health)

---

## 4. Request Pipeline (порядок обработки)

```
Request
  → CORS middleware
  → Rate limit (by user_id, после получения user из initData)
  → initData validation (dependency)
  → RBAC check (per-endpoint dependency)
  → Router handler
  → Service call
  → DB query
  → Response (Pydantic)
  → Structured logging (user_id, endpoint, status, duration)
```

---

## 5. Code Organization

### Backend

| Path | Responsibility | Rules |
|------|----------------|-------|
| `app/core/` | Settings, DB, security, errors, rate limit | Единая точка конфига (pydantic-settings) |
| `app/models/` | SQLAlchemy ORM | base.py: Audit + Soft Delete mixin |
| `app/schemas/` | Pydantic DTOs | CreateDTO, UpdateDTO, ResponseDTO раздельно |
| `app/services/` | Business logic | Rank normalization, search, RBAC checks |
| `app/api/` | FastAPI routers | Thin: только вызов service, возврат schema |
| `app/bot/` | Aiogram handlers | Thin: только вызов service, отправка ответа |

**Правило:** Bot и API используют одни и те же models, schemas, services. Никакой дублирующей логики.

### Frontend

| Path | Responsibility |
|------|----------------|
| `src/lib/tma.ts` | WebApp.ready(), haptics, MainButton, BackButton |
| `src/lib/api.ts` | fetch + X-Tg-Init-Data, error handling, base URL |
| `src/hooks/` | SWR/TanStack Query — useJobs, useApply, etc. |
| `src/components/` | UI компоненты |

---

## 6. Layer Responsibilities

| Layer | Do | Don't |
|-------|----|-------|
| **Router** | Парсинг request, вызов service, return response_model | Бизнес-логика, прямые DB-запросы |
| **Service** | Вся business logic, вызов session | HTTP-зависимости, знание о FastAPI |
| **Model** | Маппинг таблиц, relationships | Валидация (это schemas) |
| **Schema** | Валидация input/output | Логика |

---

## 7. Bot Architecture

Bot и API — два процесса, общая БД:

- **Bot:** получает updates от Telegram, может открывать WebApp по deep link
- **API:** принимает HTTP от TMA
- **Shared:** User создаётся при первом /start (bot) или первом API-запросе (TMA)

Bot handlers:
- Используют `AsyncSession` (get from pool)
- Вызывают те же services (например, job_search)
- Не дублируют validation — используют schemas

---

## 8. RBAC Roles

| Role | Permissions |
|------|-------------|
| `seafarer` | View jobs, apply to jobs |
| `company_admin` | + Create/edit jobs (только своей компании) |
| `super_admin` | Full access |

**Правило:** Роль берётся из User в DB. Никогда не доверять роль из frontend/initData — только user_id.

---

## 9. Security

### Rate Limiting

- По `telegram_user_id`
- Endpoints: job search, apply, auth
- Конфиг: RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW_SECONDS
- 429 при превышении

### CORS

- ALLOWED_ORIGINS — только домены Mini App
- Без wildcard в production

### Logging

| Log | Never log |
|-----|-----------|
| user_id, endpoint, status_code, execution_time | initData, tokens, raw bodies, credentials |

---

## 10. Database

- **Async only:** `AsyncSession`, `async with session.begin()`
- **Connection pooling:** через SQLAlchemy engine
- **Soft delete:** все запросы фильтруют `is_deleted = false` (если не явно не требуется иное)
- **Indexes:** rank, vessel_type, salary, joining_date, created_at; pg_trgm для fuzzy

---

## 11. Error Handling

**Backend:** единый формат

```json
{ "detail": "Human-readable message" }
```

- Без stack traces
- Без внутренних деталей

**Frontend:** centralized handler → показ сообщения + `HapticFeedback.notificationOccurred("error")`

---

## 12. Security Flow (sequence)

```
Client                    API                     DB
  |                        |                       |
  |  POST /jobs + X-Tg-Init-Data                   |
  |------------------------>|                       |
  |                        | validate HMAC         |
  |                        | resolve User          |
  |                        |---------------------->|
  |                        |<----------------------|
  |                        | rate limit check      |
  |                        | RBAC: company_admin?  |
  |                        | service.create_job()  |
  |                        |---------------------->|
  |                        |<----------------------|
  |<------------------------|                       |
  |  201 or 4xx             |                       |
```

---

## 13. Key Rules (summary)

| Rule | Description |
|------|-------------|
| initData | Все endpoint'ы (кроме /health) требуют валидного initData |
| Config | Только pydantic-settings, без os.getenv() |
| Async | Весь backend — async def, AsyncSession |
| Soft delete | is_deleted = true, без hard delete |
| Thin routers | Только вызов service, return schema |
| Role from DB | RBAC по User.role из БД |
| Stateless API | Горизонтальное масштабирование без shared state |

---

## 14. Scalability

- API — stateless
- Session per request (connection pool)
- Rate limit — in-memory или Redis (при масштабировании)
- DB — connection pooling, индексы для поиска

---

## 15. Cross-References

| Topic | Document |
|-------|----------|
| Data models | [data-models.md](data-models.md) |
| API endpoints | [api-overview.md](api-overview.md) |
| Maritime terms | [glossary.md](glossary.md) |
| Development | [development.md](development.md) |
| Deployment | [deployment.md](deployment.md) |
