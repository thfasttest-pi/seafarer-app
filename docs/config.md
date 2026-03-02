# Configuration Reference

Полный справочник переменных окружения и конфигурации.

---

## Файлы

| Файл | Назначение | Коммитить? |
|------|------------|------------|
| `.env.example` | Шаблон для backend | ✓ Да |
| `frontend/.env.example` | Шаблон для frontend | ✓ Да |
| `.env` | Реальные значения (backend) | ✗ Нет |
| `frontend/.env.local` | Реальные значения (frontend) | ✗ Нет |

**Действия:** Скопировать `.env.example` → `.env`, заполнить значения.

---

## Backend (.env)

### Обязательные

| Variable | Описание | Пример |
|----------|----------|--------|
| `BOT_TOKEN` | Токен бота от @BotFather | `7123456789:AAH...` |
| `DATABASE_URL` | PostgreSQL + asyncpg | `postgresql+asyncpg://user:pass@host:5432/db` |
| `SECRET_KEY` | Криптостойкий ключ (≥32 символов) | `openssl rand -hex 32` |
| `ALLOWED_ORIGINS` | CORS origins (через запятую) | `http://localhost:3000` |

### Telegram

| Variable | Описание | Default |
|----------|----------|---------|
| `WEBAPP_URL` | URL Mini App | — |
| `TELEGRAM_BOT_USERNAME` | @username без @ | — |
| `INIT_DATA_MAX_AGE_MINUTES` | Макс. возраст initData | `60` |

### База данных

| Variable | Описание | Default |
|----------|----------|---------|
| `POSTGRES_HOST` | Хост | `localhost` |
| `POSTGRES_PORT` | Порт | `5432` |
| `POSTGRES_DB` | Имя БД | `seafarer` |
| `POSTGRES_USER` | Пользователь | `postgres` |
| `POSTGRES_PASSWORD` | Пароль | — |
| `DB_POOL_SIZE` | Размер пула соединений | (SQLAlchemy default) |
| `DB_MAX_OVERFLOW` | Доп. соединения поверх пула | (SQLAlchemy default) |

### Безопасность

| Variable | Описание | Default |
|----------|----------|---------|
| `ACCESS_TOKEN_EXPIRE_MINUTES` | TTL токенов (если будет JWT) | `60` |
| `RATE_LIMIT_REQUESTS` | Лимит запросов на окно | `100` |
| `RATE_LIMIT_WINDOW_SECONDS` | Размер окна (сек) | `60` |

### Пагинация

| Variable | Описание | Default |
|----------|----------|---------|
| `PAGINATION_DEFAULT_LIMIT` | Лимит по умолчанию | `20` |
| `PAGINATION_MAX_LIMIT` | Макс. limit в запросе | `50` |

### Логирование

| Variable | Описание | Default |
|----------|----------|---------|
| `LOG_LEVEL` | Уровень логов | `INFO` |
| `LOG_JSON` | JSON-формат (production) | `false` |
| `SLOW_QUERY_THRESHOLD_MS` | Порог для логирования медленных запросов | `300` |

### Поиск

| Variable | Описание | Default |
|----------|----------|---------|
| `ENABLE_TRIGRAM` | Включить pg_trgm | `true` |

### RBAC

| Variable | Описание | Default |
|----------|----------|---------|
| `DEFAULT_USER_ROLE` | Роль для новых пользователей | `seafarer` |

### API Server

| Variable | Описание | Default |
|----------|----------|---------|
| `API_HOST` | Хост для uvicorn | `0.0.0.0` |
| `API_PORT` | Порт | `8000` |

### CORS и документация

| Variable | Описание | Default |
|----------|----------|---------|
| `ENABLE_CORS` | Включить CORS | `true` |
| `ENABLE_DOCS` | Swagger /docs | `true` |

### Окружение

| Variable | Описание | Default |
|----------|----------|---------|
| `ENVIRONMENT` | development \| staging \| production | `development` |
| `DEBUG` | Режим отладки | `true` (dev) |
| `AUTO_RELOAD` | Uvicorn --reload | `true` (dev) |

---

## Frontend (frontend/.env.local)

| Variable | Описание | Пример |
|----------|----------|--------|
| `NEXT_PUBLIC_API_URL` | URL API | `http://localhost:8000` |
| `NEXT_PUBLIC_WEBAPP_URL` | URL Mini App | `https://app.example.com` |

**Важно:** Переменные с префиксом `NEXT_PUBLIC_` доступны в браузере. Не хранить секреты.

---

## Production Checklist

| Действие | Значение |
|----------|----------|
| ENVIRONMENT | `production` |
| DEBUG | `false` |
| LOG_JSON | `true` |
| ALLOWED_ORIGINS | Только реальные домены (без wildcard) |
| SECRET_KEY | Уникальный, криптостойкий |
| ENABLE_DOCS | `false` (опционально) |

---

## Pydantic Settings (Backend)

Конфиг загружается через `pydantic-settings`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )
    BOT_TOKEN: str
    DATABASE_URL: str
    SECRET_KEY: str
    ENVIRONMENT: str = "development"
    RATE_LIMIT_REQUESTS: int = 100
    PAGINATION_MAX_LIMIT: int = 50
    INIT_DATA_MAX_AGE_MINUTES: int = 60
    # ...
```

Использование: `Settings()` создаёт синглтон; все значения типизированы.
