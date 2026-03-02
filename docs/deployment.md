# Deployment

Краткое руководство по развёртыванию Seafarer App.

---

## Требования

- PostgreSQL 15+
- Python 3.11+
- Node.js 18+
- HTTPS для Mini App (обязательно для TMA)

---

## Checklist перед production

- [ ] `ENVIRONMENT=production`
- [ ] `DEBUG=false`
- [ ] `LOG_JSON=true`
- [ ] `SECRET_KEY` — криптостойкий случайный ключ
- [ ] `BOT_TOKEN` — production бот
- [ ] `DATABASE_URL` — production БД с connection pooling
- [ ] `ALLOWED_ORIGINS` — только домен Mini App (без wildcard)
- [ ] Rate limiting включён и настроен
- [ ] Миграции применены: `alembic upgrade head`

---

## Backend

Рекомендуется: Gunicorn + Uvicorn workers.

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

Или через Docker / systemd — процесс должен оставаться запущенным.

---

## Frontend

```bash
npm run build
# Статика в .next/ или out/ — раздавать через CDN / Nginx
```

Для TMA нужен HTTPS. Варианты: Vercel, Cloudflare Pages, свой Nginx + Let's Encrypt.

---

## Bot

Отдельный процесс (или контейнер):

```bash
python -m app.bot.run
```

---

## Мониторинг

- Health check: `GET /health`
- Логи: structured JSON, `user_id`, `endpoint`, `status_code`, `execution_time`
- Не логировать: initData, tokens, credentials
