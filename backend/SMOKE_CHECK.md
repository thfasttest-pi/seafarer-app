# Smoke-check: SeafarerApp backend (Windows, PowerShell)

Окружение: `C:\0_ROOT\10_ACTIVE\01_Main_Project\SeafarerApp\backend`, `.venv`, PostgreSQL локально (Windows service).

---

## 1) Проверить, что PostgreSQL доступен на localhost:5432

```powershell
cd C:\0_ROOT\10_ACTIVE\01_Main_Project\SeafarerApp\backend

# Проверка порта (должен быть LISTENING)
Get-NetTCPConnection -LocalPort 5432 -ErrorAction SilentlyContinue | Select-Object LocalAddress, LocalPort, State
```

**Ожидаемо:** строка с `State = Listen` (или `Listen`).

**Если порт не слушает** — запустить службу PostgreSQL:

```powershell
# Узнать имя службы (обычно postgresql-x64-16 или PostgreSQL)
Get-Service -Name "*postgres*"

# Запустить (подставь точное имя из вывода выше)
Start-Service -Name "postgresql-x64-16"
```

---

## 2) Создать базу seafarer (если ещё нет)

**Через psql** (если в PATH):

```powershell
psql -U postgres -c "CREATE DATABASE seafarer;"
```

**Если psql не в PATH** — найти и вызвать полный путь, например:

```powershell
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -c "CREATE DATABASE seafarer;"
```

**Проверка:**

```powershell
psql -U postgres -c "\l" | Select-String seafarer
```

Либо в pgAdmin: правый клик по "Databases" → Create → Database → имя `seafarer`.

---

## 3) Проверить DATABASE_URL в .env

Файл: `backend\.env`

- Должен быть **async** URL: `postgresql+asyncpg://...`
- Пароль с спецсимволами — в URL кодировать (например `%` → `%25`) или взять в кавычки в .env.

**Пример корректного .env:**

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/seafarer
BOT_TOKEN=123456:ABC-DEF
SECRET_KEY=your-secret-key-min-32-chars
```

Проверка загрузки настроек (из папки backend, с активированным .venv):

```powershell
.\.venv\Scripts\Activate.ps1
python -c "from app.core.settings import settings; print('OK' if 'asyncpg' in settings.DATABASE_URL else 'Use asyncpg URL')"
```

**Ожидаемо:** вывод `OK`.

---

## 4) Запустить миграции Alembic

```powershell
cd C:\0_ROOT\10_ACTIVE\01_Main_Project\SeafarerApp\backend
.\.venv\Scripts\Activate.ps1
python -m alembic upgrade head
```

**Ожидаемо:** строка вида `INFO  [alembic.runtime.migration] Running upgrade  -> 001_init, ...` и без traceback.

**Типичные ошибки:**

| Ошибка | Причина | Решение |
|--------|----------|---------|
| `connection refused` / `could not connect` | PostgreSQL не запущен или не слушает 5432 | Запустить службу (шаг 1), проверить порт |
| `database "seafarer" does not exist` | БД не создана | Выполнить шаг 2 |
| `password authentication failed` | Неверный пользователь/пароль в .env | Исправить `DATABASE_URL` в `.env` |
| `ModuleNotFoundError: app` | Запуск не из корня backend | Выполнять команды из `backend` |


---

## 5) Запустить API

```powershell
cd C:\0_ROOT\10_ACTIVE\01_Main_Project\SeafarerApp\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

**Ожидаемо:** в консоли `Uvicorn running on http://127.0.0.1:8000` без ошибок.

Окно с сервером оставить открытым; проверки делать в **другом** окне PowerShell.

---

## 6) Проверить /health

В новом окне PowerShell:

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```

**Ожидаемо:** `status : ok` (или JSON `{"status":"ok"}`).

---

## 7) Проверить /api/v1/jobs без X-Tg-Init-Data → 401 + request_id

```powershell
try { Invoke-RestMethod -Uri "http://localhost:8000/api/v1/jobs" -Method Get } catch { $_.ErrorDetails.Message }
```

Либо явно посмотреть статус и тело:

```powershell
$r = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/jobs" -Method Get -SkipHttpErrorCheck
$r.StatusCode   # должно быть 401
$r.Content      # JSON с code, message, request_id
```

**Ожидаемо:** `StatusCode = 401`, в теле JSON вида `{"code":"auth_error","message":"...","request_id":"..."}`.

---

## 8) (Опционально) Тестовые записи и keyset pagination

**Вставить данные** (через psql или pgAdmin):

```sql
INSERT INTO jobs (id, title, description, created_at)
VALUES
  (gen_random_uuid(), 'Job A', 'Desc A', now()),
  (gen_random_uuid(), 'Job B', 'Desc B', now() - interval '1 minute'),
  (gen_random_uuid(), 'Job C', 'Desc C', now() - interval '2 minutes');
```

**Проверка пагинации** — только с валидным `X-Tg-Init-Data` (из Telegram WebApp). Без него будет 401.

- Запрос с `limit=2` без cursor → первые 2 записи + `next_cursor` (если есть ещё строки).
- Запрос с `limit=2&cursor=<next_cursor>` → следующие 2, без дублей с первой страницы.
- Когда записей больше нет — `next_cursor` в ответе `null`.

Порядок: `created_at DESC`, затем `id DESC`.

---

## Smoke-check чеклист (команды + ожидаемый результат)

| # | Действие | Команда |
|---|----------|---------|
| 1 | PostgreSQL слушает 5432 | `Get-NetTCPConnection -LocalPort 5432 \| Select-Object State` → State = Listen |
| 2 | БД seafarer есть | `psql -U postgres -c "\l" \| Select-String seafarer` → строка с seafarer |
| 3 | .env с asyncpg | В `.env`: `DATABASE_URL=postgresql+asyncpg://...` |
| 4 | Миграции применены | `python -m alembic upgrade head` → без ошибок |
| 5 | API запущен | `uvicorn app.main:app --reload` → "Uvicorn running on ..." |
| 6 | Health OK | `Invoke-RestMethod http://localhost:8000/health` → `status: ok` |
| 7 | Jobs без auth → 401 | `Invoke-WebRequest http://localhost:8000/api/v1/jobs -SkipHttpErrorCheck` → StatusCode 401, в теле `code`, `message`, `request_id` |

**Итог:** пункты 1–7 выполнены без ошибок → backend считается прошедшим smoke-check.
