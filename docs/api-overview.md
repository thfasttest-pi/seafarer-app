# API Overview

REST API контракт. Все эндпоинты требуют валидного `X-Tg-Init-Data`, **кроме** публичных (см. раздел «Публичные endpoints»).

---

## Общее

| Header | Required | Description |
|--------|----------|-------------|
| `X-Tg-Init-Data` | Да (кроме /health) | Telegram WebApp.initData (HMAC-валидация) |
| `Content-Type` | Да (POST/PUT) | `application/json` |

**Base URL:** Защищённые endpoints — под `/api/v1`. Пример: `GET {host}/api/v1/jobs`. Публичный `/health` — на корне: `GET {host}/health`.

---

## Публичные endpoints (без auth)

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check на корне, 200 OK |

---

## Защищённые endpoints (требуют X-Tg-Init-Data)

Пути ниже — относительно `/api/v1`. Пример: `GET /jobs` → `GET {host}/api/v1/jobs`.

### Jobs

| Method | Path | Role | Description |
|--------|------|------|-------------|
| GET | /jobs | seafarer+ | Список с keyset pagination и фильтрами |
| GET | /jobs/{id} | seafarer+ | Детали вакансии (404 если не найдена или soft-deleted) |
| POST | /jobs | company_admin+ | Создать вакансию |
| PUT | /jobs/{id} | company_admin+ | Обновить (только свою) |
| DELETE | /jobs/{id} | company_admin+ | Soft delete (только свою) |

**Query params для GET /jobs:**

- `limit` — размер страницы (max 50)
- `cursor` — курсор для следующей страницы (keyset)
- `rank` — фильтр по рангу
- `vessel_type` — tanker, bulk, etc.
- `salary_min`, `salary_max` — фильтр по зарплате
- `search` — ILIKE по title/description
- `status` — draft | published | closed (default: published)

**Response:** `{ "items": [...], "next_cursor": "..." | null }`

---

## Applications

| Method | Path | Role | Description |
|--------|------|------|-------------|
| POST | /jobs/{id}/apply | seafarer | Откликнуться на вакансию |
| GET | /applications/me | seafarer | Мои отклики |
| GET | /jobs/{id}/applications | company_admin | Отклики на вакансию (свою) |

---

## Users (Self)

| Method | Path | Role | Description |
|--------|------|------|-------------|
| GET | /me | any | Текущий пользователь (id, telegram_id, role, created_at) |
| GET | /users/me | any | Текущий пользователь (alias) |
| PATCH | /users/me | any | Обновить профиль (ограниченные поля) |

---

## Companies (Admin)

| Method | Path | Role | Description |
|--------|------|------|-------------|
| GET | /companies | super_admin | Список компаний |
| POST | /companies | super_admin | Создать компанию |
| PUT | /companies/{id} | super_admin | Обновить компанию |

---

## Ошибки

| Status | Format |
|--------|--------|
| 400 | `{ "detail": "Bad request message" }` |
| 401 | `{ "detail": "Invalid initData" }` |
| 403 | `{ "detail": "Forbidden" }` |
| 404 | `{ "code": "not_found", "message": "...", "request_id": "..." }` |
| 422 | `{ "detail": "Validation error", "errors": [...] }` |
| 429 | `{ "detail": "Rate limit exceeded" }` |
