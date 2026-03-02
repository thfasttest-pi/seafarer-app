# =============================================================================
# SEAFARER APP — Makefile (Development)
# =============================================================================

.PHONY: help db-up db-down migrate migrate-create api bot frontend install install-backend install-frontend

help:
	@echo "Seafarer App — targets:"
	@echo "  make db-up          — start PostgreSQL (docker compose)"
	@echo "  make db-down        — stop PostgreSQL"
	@echo "  make migrate        — alembic upgrade head"
	@echo "  make migrate-create — create migration (use: make migrate-create M='desc')"
	@echo "  make api        — run FastAPI (uvicorn)"
	@echo "  make bot        — run Telegram bot"
	@echo "  make frontend   — run Next.js dev"
	@echo "  make install    — install backend + frontend deps"
	@echo "  make install-backend"
	@echo "  make install-frontend"

db-up:
	docker compose up -d postgres

db-down:
	docker compose down

migrate:
	cd backend && alembic upgrade head

migrate-create:
	cd backend && alembic revision --autogenerate -m "$(M)"

api:
	cd backend && uvicorn app.main:app --reload

bot:
	cd backend && python -m app.bot.run

frontend:
	cd frontend && npm run dev

install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

install: install-backend install-frontend
