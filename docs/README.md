# Seafarer App — Documentation

Навигация по документации проекта.

---

## Основные документы

| Документ | Описание |
|----------|----------|
| [architecture.md](architecture.md) | Архитектура, flow, RBAC, error handling |
| [data-models.md](data-models.md) | User, Company, Job, Application — поля и индексы |
| [api-overview.md](api-overview.md) | REST API: эндпоинты, параметры, ответы |
| [config.md](config.md) | Полный справочник env-переменных |
| [development.md](development.md) | Настройка окружения, запуск, troubleshooting |
| [deployment.md](deployment.md) | Production checklist, Gunicorn, HTTPS |
| [infra.md](infra.md) | .gitignore, Docker, Makefile, EditorConfig |
| [glossary.md](glossary.md) | Ранги, vessel types, RBAC — справочник терминов |

---

## Задачи (Tasks)

| Файл | Описание |
|------|----------|
| [tasks/00-bootstrap.md](tasks/00-bootstrap.md) | Чеклист первоначальной настройки проекта |
| [tasks/01-api-auth.md](tasks/01-api-auth.md) | initData validation (HMAC-SHA256) |

---

## Быстрые ссылки

- [README](../README.md) — обзор проекта в корне
- [.env.example](../.env.example) — шаблон переменных окружения
- [.cursorrules](../.cursorrules) — Cursor rules для AI
