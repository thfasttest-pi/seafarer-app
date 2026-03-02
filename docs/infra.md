# Infrastructure Reference

Инфраструктура и инструменты проекта.

---

## Файлы

| Файл | Назначение |
|------|------------|
| `.gitignore` | Игнорируемые файлы для git |
| `.editorconfig` | Единые правила форматирования |
| `docker-compose.yml` | Локальный PostgreSQL |
| `Makefile` | Команды для разработки |

---

## .gitignore

Игнорируется:

- **Environment:** .env, .env.local, .env.*.local
- **Python:** __pycache__, .venv, venv, *.pyc, .mypy_cache, .ruff_cache
- **Node:** node_modules, .next, out
- **IDE:** .idea, .vscode
- **Logs:** *.log, logs/
- **Testing:** .coverage, .pytest_cache, htmlcov/
- **Secrets:** *.pem, *.key, secrets/

Коммитим: .env.example, migrations, исходный код.

---

## .editorconfig

| Тип | indent | eol | trim | final newline |
|-----|--------|-----|------|---------------|
| *.py | 4 spaces | LF | yes | yes |
| *.{js,ts,tsx,json,yml} | 2 spaces | LF | yes | yes |
| Makefile | tab | LF | yes | yes |

Charset: UTF-8.

---

## Docker Compose

```bash
docker compose up -d      # Запустить PostgreSQL
docker compose down       # Остановить
```

Сервис `postgres`:
- Порт: 5432
- User: postgres
- Password: password
- DB: seafarer
- Volume: seafarer_pgdata (persistent)

DATABASE_URL: `postgresql+asyncpg://postgres:password@localhost:5432/seafarer`

---

## Makefile

| Target | Описание |
|--------|----------|
| `make help` | Список команд |
| `make db-up` | Запуск PostgreSQL |
| `make db-down` | Остановка PostgreSQL |
| `make migrate` | alembic upgrade head |
| `make migrate-create M="desc"` | Создать миграцию |
| `make api` | Запуск FastAPI |
| `make bot` | Запуск Telegram bot |
| `make frontend` | Запуск Next.js |
| `make install` | pip install + npm install |

---

## Cursor Rules (.cursorrules)

Правила для AI в Cursor:
- Security (initData, rate limit, logging)
- Async-only backend
- Project structure
- Configuration (pydantic-settings)
- Database, Pydantic, RBAC
- Error handling
- Frontend TMA
- Prohibitions
- Git, file naming, editor
- Infra

Путь: корень проекта.
