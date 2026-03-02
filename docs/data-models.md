# Data Models

Доменные модели Seafarer App.

---

## Общие поля (Audit + Soft Delete)

Каждая таблица наследует:

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Primary key |
| `created_at` | timestamptz | Timezone-aware |
| `updated_at` | timestamptz | Timezone-aware |
| `is_deleted` | boolean | Soft delete, default `false` |

---

## User

Пользователь (моряк, компания, админ).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | ✓ | |
| telegram_user_id | bigint | ✓ | Telegram user ID (unique) |
| telegram_username | str | | @username |
| first_name | str | | |
| last_name | str | | |
| role | enum | ✓ | seafarer, company_admin, super_admin |
| company_id | FK | | Для company_admin |
| created_at | timestamptz | ✓ | |
| updated_at | timestamptz | ✓ | |
| is_deleted | bool | ✓ | |

**Индексы:** `telegram_user_id` (unique)

---

## Company

Судовладелец / крюинг.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | ✓ | |
| name | str | ✓ | |
| verified | bool | | Верифицированная компания |
| created_at | timestamptz | ✓ | |
| updated_at | timestamptz | ✓ | |
| is_deleted | bool | ✓ | |

**Индексы:** `name` (pg_trgm для поиска)

---

## Job

Вакансия.

### Обязательные поля

| Field | Type | Description |
|-------|------|-------------|
| rank | str | Канонический ранг (см. [glossary](glossary.md)) |
| vessel_type | str | Tanker, Bulk, Container, etc. |
| dwt | int \| null | Deadweight tons |
| grt | int \| null | Gross register tons |
| engine_type | str | ME, AE, steam |
| salary | decimal | Зарплата (USD) |
| contract_months | int | Длительность контракта |

### Опциональные поля

| Field | Type | Description |
|-------|------|-------------|
| joining_date | date | Дата выхода |
| company_id | FK | Компания |
| company_name | str | Название (если без company_id) |
| verified_company | bool | Верифицированная компания |
| nationality_restrictions | str \| null | |
| internet_onboard | bool | |
| english_level | str | B2, C1, etc. |
| visa_requirements | str | |
| notes | text | |

### Audit

| Field | Type |
|-------|------|
| id | UUID |
| created_at | timestamptz |
| updated_at | timestamptz |
| is_deleted | bool |

**Индексы:**

- rank
- vessel_type
- salary
- joining_date
- created_at
- pg_trgm: company_name, vessel_type, title (если есть)

---

## Application

Отклик моряка на вакансию.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | |
| job_id | FK | |
| user_id | FK | Seafarer |
| status | enum | pending, accepted, rejected |
| created_at | timestamptz | |
| updated_at | timestamptz | |
| is_deleted | bool | |

**Индексы:** (job_id, user_id) unique, job_id, user_id

---

## Rank Normalization

Входные значения маппятся на канонические:

| Input (examples) | Canonical |
|------------------|-----------|
| 2O, 2/O, OOW, Second Officer | second_officer |
| Captain, Master | captain |
| C/E, Chief Engineer | chief_engineer |
| C/O, Chief Officer | chief_officer |
| ... | ... |

См. [glossary](glossary.md) для полного списка.
