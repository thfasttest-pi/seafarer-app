# ⚓ SEAFARER APP
Telegram Mini App (TMA) for Seafarer Job Search

Fullstack production-ready job platform for maritime professionals.

---

## 🧩 Tech Stack

### Backend
- FastAPI (async-only)
- Aiogram 3.x
- PostgreSQL
- SQLAlchemy 2.0 (AsyncSession)
- Alembic (migrations)
- Pydantic v2
- pydantic-settings

### Frontend
- Next.js 14 (App Router)
- Tailwind CSS
- @twa-dev/sdk
- SWR or TanStack Query

---

# 🏗 Architecture Overview

Telegram WebApp  
        ↓  
   initData (HMAC)  
        ↓  
     FastAPI API  
        ↓  
   Service Layer  
        ↓  
   PostgreSQL DB  

- Telegram Mini App sends `initData`
- Backend validates via HMAC-SHA256 (BOT_TOKEN)
- All API routes require auth dependency (except /health)
- Bot and API share DB models and schemas
- Business logic lives in `/services`

---

# 📂 Project Structure

backend/
  app/
    api/          # FastAPI routers
    bot/          # Aiogram handlers
    models/       # SQLAlchemy models
    schemas/      # Pydantic DTOs
    services/     # Business logic
    core/         # settings, security, db, errors

frontend/
  src/
    components/
    hooks/
    lib/          # API client, TMA wrapper

---

# 🔐 Security

## Telegram initData

- All endpoints require initData validation
- HMAC-SHA256 using BOT_TOKEN
- No endpoint without auth dependency
- No raw initData logging
- Error format: `{ "detail": "Readable message" }`

---

# ⚙️ Environment Variables

Create `.env` file based on `.env.example`.

Example:

BOT_TOKEN=your_bot_token  
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/seafarer  
SECRET_KEY=super_secret_key  
ENVIRONMENT=development  

---

# 🚀 Local Development

## 1️⃣ Backend

### Install dependencies

cd backend  
pip install -r requirements.txt  

### Run migrations

alembic upgrade head  

### Run API

uvicorn app.main:app --reload  

### Run Telegram bot

python -m app.bot.run  

---

## 2️⃣ Frontend

cd frontend  
npm install  
npm run dev  

---

# 🗄 Database & Migrations

### Create new migration

After ANY change to models:

alembic revision --autogenerate -m "describe change"

### Apply migration

alembic upgrade head  

All migrations must be reviewed before commit.

---

# 📌 Domain Model (Job)

Each Job includes:

- rank (canonical)
- vessel_type
- dwt or grt
- engine_type
- salary
- contract_months

Optional:

- joining_date
- company_name
- verified_company
- nationality_restrictions
- internet_onboard

---

# 🔎 Search Strategy

- Rank normalization (2O, 2/O, OOW → second_officer)
- PostgreSQL indexes
- pg_trgm for fuzzy matching
- Server-side pagination only

---

# 🎨 Telegram Mini App UX

- `WebApp.ready()` before render
- Telegram theme variables for styling
- MainButton for primary actions
- Haptic feedback:
  - `impactOccurred("light")`
  - `notificationOccurred("error")`
- BackButton handling synced with router

---

# 🛡 RBAC Roles

- seafarer
- company_admin
- super_admin

Role-based permissions enforced on backend.

---

# 📊 Logging Policy

- Structured logs (JSON in production)
- Log:
  - user_id
  - endpoint
  - status_code
  - execution_time
- Never log:
  - initData
  - tokens
  - secrets

---

# 🧪 Production Readiness

- Async-only backend
- Soft delete (`is_deleted`)
- Audit fields (`created_at`, `updated_at`)
- Indexed search fields
- Rate limiting per user_id
- Centralized API error handling

---

# 📚 Documentation

Подробная документация в [`docs/`](docs/README.md):

| Документ | Описание |
|----------|----------|
| [Architecture](docs/architecture.md) | Flow, RBAC, error handling |
| [Data Models](docs/data-models.md) | User, Job, Company, Application |
| [API Overview](docs/api-overview.md) | REST endpoints |
| [Config](docs/config.md) | Env variables reference |
| [Development](docs/development.md) | Setup, troubleshooting |
| [Deployment](docs/deployment.md) | Production checklist |
| [Glossary](docs/glossary.md) | Maritime terms, ranks |
| [Infra](docs/infra.md) | Docker, Makefile, .gitignore |
| [Bootstrap](docs/tasks/00-bootstrap.md) | Project setup checklist |

---

# 📜 License

Internal project — not for public redistribution.

---

⚓ Built for real seafarers.