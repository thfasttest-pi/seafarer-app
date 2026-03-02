# 01 — Telegram initData Auth

Реализация валидации Telegram initData (HMAC-SHA256) для защиты API.

---

## Цель

Все защищённые endpoints API требуют валидный `X-Tg-Init-Data`. Единственное исключение: `GET /health`.

---

## Требования

### 1. Зависимость FastAPI

- Создать `app/core/security.py` (или `app/core/initdata.py`)
- Реализовать функцию `validate_init_data(init_data: str) -> TelegramUserData`
- Использовать как dependency: `Depends(get_current_user)`
- При невалидном initData → raise `HTTPException(401, detail="Invalid initData")`
- При просроченном auth_date → raise `HTTPException(401, detail="initData expired")`

### 2. HMAC-SHA256 Validation

- Парсить initData как key=value (query string)
- Строить `data_check_string` (отсортированные пары, без `hash`)
- HMAC-SHA256(data_check_string, SHA256(BOT_TOKEN))
- Сравнить с `hash` из initData
- Проверить `auth_date` (не старше `INIT_DATA_MAX_AGE_MINUTES`)

### 3. User Resolution

- Извлечь `user` (JSON) из initData
- Получить `user_id` (Telegram user ID)
- Найти или создать User в DB
- Вернуть `User` в request.state / dependency

### 4. Применение

- Подключить dependency ко всем роутерам, кроме `/health`
- `/health` — без auth
- Swagger `/docs` — без auth (если ENABLE_DOCS)

---

## Чеклист

- [ ] `app/core/security.py` — validate_init_data()
- [ ] `app/core/dependencies.py` — get_current_user(init_data: str)
- [ ] Глобально: router с dependency для `/api/v1/*`
- [ ] `/health` — вне protected scope
- [ ] Тесты: valid initData → 200, invalid → 401

---

## Ссылки

- [Telegram WebApp initData](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app)
- [architecture.md](../architecture.md) — секция 3. initData Validation
