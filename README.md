# 📈 Stock Portfolio & Investment Management API

A **production-grade FinTech backend API** built with FastAPI, Async SQLAlchemy 2.0, Alembic, and Pydantic v2 during a 15-day internship programme at ZyoraByte.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=flat&logo=sqlalchemy)](https://sqlalchemy.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql)](https://postgresql.org)
[![Day 2 Completed](https://img.shields.io/badge/Day%202-Completed-10b981?style=flat)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Project Overview

A secure, scalable FinTech backend API designed to empower investors to:
- 🔐 **Register & authenticate** securely using JWT access & refresh tokens
- 💼 **Manage investment portfolios** (CRUD operations, currency preferences)
- 📊 **Record BUY/SELL transactions** with live stock quantity tracking
- 📈 **Track portfolio holdings** with weighted average buy price & unrealized P&L
- 💰 **Fetch live market data** via Alpha Vantage API
- 👁️ **Watchlists & Target Price Alerts** with background notifications
- 👑 **Role-Based Access Control (RBAC)** for admin operations

---

## ✅ DAY 2 Implementation — API Design, Entities & Database Architecture

> **Date:** 1 Sept 2026 | **Submission:** Submitted on Time | **Status:** ✅ Completed

During **Day 2**, the project entities, relationships, Pydantic request/response contracts, async database layer, Alembic migrations, and REST endpoint plans covering success & error cases were fully established.

### 🌟 Day 2 Feature Breakdown & Completion Guide

#### 1. 🗄️ Entities & Relationships Mapped
- **`User` Entity (`users` table):** Mapped in [`app/models/user.py`](file:///d:/Zyora%20Internship/Stock_Market/app/models/user.py) with UUID v4 primary key (`id`), indexed `email` & `username`, `hashed_password`, `full_name`, `is_active`, `is_admin`, and auto-managed timestamps (`created_at`, `updated_at`).
- **`Portfolio` Entity (`portfolios` table):** Mapped in [`app/models/portfolio.py`](file:///d:/Zyora%20Internship/Stock_Market/app/models/portfolio.py) with UUID v4 primary key (`id`), `name`, `description`, base `currency` (default `"USD"`), and `is_default` flag.
- **Entity Relationship:** 1-to-many relationship (`User ──< Portfolio`) configured with SQLAlchemy `ForeignKey("users.id", ondelete="CASCADE")` and bidirectional ORM `relationship("User", backref="portfolios")`.

#### 2. 📝 Pydantic Request & Response Contracts
Pydantic v2 schemas defined in [`app/schemas/portfolio.py`](file:///d:/Zyora%20Internship/Stock_Market/app/schemas/portfolio.py) for strict request validation and response serialization:
- **`PortfolioBase`:** Common base attributes (`name`, `description`, `currency`, `is_default`) with OpenAPI field metadata and length constraints.
- **`PortfolioCreate` (Request Contract):** Inherits from `PortfolioBase` for `POST /api/v1/portfolios`.
- **`PortfolioUpdate` (Request Contract):** Optional fields for partial updates via `PUT /api/v1/portfolios/{id}`.
- **`PortfolioOut` (Response Contract):** Output payload containing `id`, `user_id`, computed `total_value`, `created_at`, and `updated_at` with `model_config = ConfigDict(from_attributes=True)`.

#### 3. 🌐 REST Endpoint Plan (Success & Error Cases)
Endpoints implemented in [`app/api/v1/portfolios.py`](file:///d:/Zyora%20Internship/Stock_Market/app/api/v1/portfolios.py) and error contracts handled via [`app/core/exceptions.py`](file:///d:/Zyora%20Internship/Stock_Market/app/core/exceptions.py):

| Method | Endpoint | Description | Success Status | Handled Error Cases |
|---|---|---|---|---|
| `POST` | `/api/v1/portfolios` | Create a new investment portfolio | `201 Created` | `400 Bad Request`, `422 Validation Error` |
| `GET` | `/api/v1/portfolios` | List portfolios owned by user (with pagination) | `200 OK` | `401 Unauthorized`, `500 Server Error` |
| `GET` | `/api/v1/portfolios/{id}` | Retrieve specific portfolio details by ID | `200 OK` | `404 Not Found`, `403 Forbidden` |
| `PUT` | `/api/v1/portfolios/{id}` | Update portfolio name, currency, or default status | `200 OK` | `404 Not Found`, `403 Forbidden`, `422 Validation Error` |
| `DELETE` | `/api/v1/portfolios/{id}` | Delete portfolio account | `204 No Content` | `404 Not Found`, `403 Forbidden` |

##### 🛡️ Standardized Error Response Contract
All error cases yield a predictable, production-grade JSON error structure:
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Portfolio with id '3fa85f64-5717-4562-b3fc-2c963f66afa6' not found",
    "details": null
  }
}
```

### 📊 Summary Matrix

| Deliverable | Module / File | Description | Status |
|---|---|---|---|
| **Async DB Session Engine** | [`app/db/session.py`](file:///d:/Zyora%20Internship/Stock_Market/app/db/session.py) | Connection pooling (`create_async_engine`), `AsyncSessionLocal` factory, `get_db()` dependency, and live health check. | ✅ Complete |
| **Declarative Base & Mixin** | [`app/db/base.py`](file:///d:/Zyora%20Internship/Stock_Market/app/db/base.py) | `Base(DeclarativeBase)` root class & `TimestampMixin` providing auto `created_at` and `updated_at` timestamps. | ✅ Complete |
| **User & Portfolio ORM Models** | [`app/models/`](file:///d:/Zyora%20Internship/Stock_Market/app/models/) | Mapped entity tables with foreign keys (`ON DELETE CASCADE`), UUID primary keys, and bidirectional ORM relationships. | ✅ Complete |
| **Pydantic v2 Schemas** | [`app/schemas/portfolio.py`](file:///d:/Zyora%20Internship/Stock_Market/app/schemas/portfolio.py) | Input validation and output serialization schemas (`PortfolioCreate`, `PortfolioUpdate`, `PortfolioOut`). | ✅ Complete |
| **Alembic Migrations** | [`alembic/`](file:///d:/Zyora%20Internship/Stock_Market/alembic/) | Configured `env.py` for async SQLAlchemy; autogenerated and applied migrations (`create_user_table` & `create_portfolio_table`). | ✅ Complete |
| **Portfolio REST Endpoints** | [`app/api/v1/portfolios.py`](file:///d:/Zyora%20Internship/Stock_Market/app/api/v1/portfolios.py) | Full CRUD operations (`POST`, `GET` list, `GET` single, `PUT`, `DELETE`) with ownership validation. | ✅ Complete |
| **DB Health Endpoint** | [`app/api/v1/health.py`](file:///d:/Zyora%20Internship/Stock_Market/app/api/v1/health.py) | Integrated live `check_db_connection()` query reporting `"database": "connected"`. | ✅ Complete |
| **Automated Pytest Suite** | [`tests/`](file:///d:/Zyora%20Internship/Stock_Market/tests/) | Pytest fixtures (`conftest.py`) and test suites (`test_day2_db.py`, `test_portfolios.py`). Passed 6/6 tests (100%). | ✅ Complete |

---

## ✅ DAY 3 Implementation — Database Setup, Async SQLAlchemy & User Authentication

> **Date:** 2 Sept 2026 | **Submission:** Submitted on Time | **Status:** ✅ Completed

During **Day 3**, PostgreSQL/SQLite connectivity was configured using async SQLAlchemy 2.0, core entity tables were represented as ORM models, the Alembic migration pipeline was established, and full **User Registration & JWT Authentication** features were built and integrated.

### 🌟 Day 3 Feature Breakdown & Completion Guide

#### 1. ⚡ Async Database Session Configured
- **Engine & Pool Configuration:** [`app/db/session.py`](file:///d:/Zyora%20Internship/Stock_Market/app/db/session.py) initializes `create_async_engine(settings.DATABASE_URL)` with `pool_size=10`, `max_overflow=20`, and `pool_pre_ping=True`.
- **Async Session Factory:** `AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)`.
- **FastAPI Dependency:** `get_db()` yields an async session per request with automatic commit on success, rollback on exception, and session closure.
- **Connection Health Check:** `check_db_connection()` executes `SELECT 1` asynchronously to report database connectivity.

#### 2. 🧱 Core Tables Represented as ORM Models
- **`Base` Declarative Root & `TimestampMixin`:** Defined in [`app/db/base.py`](file:///d:/Zyora%20Internship/Stock_Market/app/db/base.py) providing auto-managed UTC `created_at` and `updated_at` timestamps across models.
- **`User` Model:** Defined in [`app/models/user.py`](file:///d:/Zyora%20Internship/Stock_Market/app/models/user.py) (`users` table) with UUID primary key, indexed `email` & `username`, `hashed_password`, `full_name`, `is_active`, and `is_admin`.
- **`Portfolio` Model:** Defined in [`app/models/portfolio.py`](file:///d:/Zyora%20Internship/Stock_Market/app/models/portfolio.py) (`portfolios` table) linked to users via `user_id` Foreign Key (`ON DELETE CASCADE`) and bidirectional ORM `relationship("User", backref="portfolios")`.

#### 3. 🔄 Migration Upgrades & Downgrades
- **Async Environment:** [`alembic/env.py`](file:///d:/Zyora%20Internship/Stock_Market/alembic/env.py) configured with `async_engine_from_config` and `Base.metadata` autogenerate target.
- **`create_user_table` Migration ([`3004a631c566`](file:///d:/Zyora%20Internship/Stock_Market/alembic/versions/3004a631c566_create_user_table.py)):** Includes `upgrade()` (`op.create_table('users')`, indexes) and clean `downgrade()` (`op.drop_table('users')`, dropping indexes).
- **`create_portfolio_table` Migration ([`f1a207002db9`](file:///d:/Zyora%20Internship/Stock_Market/alembic/versions/f1a207002db9_create_portfolio_table.py)):** Includes `upgrade()` (`op.create_table('portfolios')`, FK constraint) and clean `downgrade()` (`op.drop_table('portfolios')`).
- **Verified Current Revision:** `f1a207002db9 (head)`.

#### 4. 🔐 Security, JWT Authentication & Profile Features
- **Bcrypt Password Hashing:** [`app/core/security.py`](file:///d:/Zyora%20Internship/Stock_Market/app/core/security.py) with `hash_password()` and `verify_password()`.
- **JWT Token Issuance:** Generation and decoding of signed JWT access (30 min) and refresh (7 day) tokens via `python-jose`.
- **Auth Endpoints ([`app/api/v1/auth.py`](file:///d:/Zyora%20Internship/Stock_Market/app/api/v1/auth.py)):**
  - `POST /api/v1/auth/register` — Register user with unique email/username checks.
  - `POST /api/v1/auth/login` — Authenticate and issue `access_token` & `refresh_token`.
  - `POST /api/v1/auth/refresh` — Issue fresh access token.
- **User Profile Endpoints ([`app/api/v1/users.py`](file:///d:/Zyora%20Internship/Stock_Market/app/api/v1/users.py)):**
  - `GET /api/v1/users/me` — Retrieve authenticated user profile.
  - `PUT /api/v1/users/me` — Update user profile details.
  - `PUT /api/v1/users/me/password` — Change user password after verifying current password.
- **Dependency Injection ([`app/api/deps.py`](file:///d:/Zyora%20Internship/Stock_Market/app/api/deps.py)):** `get_current_user`, `get_current_active_user`, and `get_current_admin_user`.
- **Automated Pytest Suite:** [`tests/test_auth.py`](file:///d:/Zyora%20Internship/Stock_Market/tests/test_auth.py) passed 8/8 tests (100%).

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.141 |
| Language | Python 3.13 |
| Database | PostgreSQL 15 / SQLite (via `aiosqlite`) |
| ORM | SQLAlchemy 2.x (async) |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| UI / Portal | Glassmorphic HTML5 + Custom Swagger UI Dark Theme |
| Testing | Pytest + pytest-asyncio + httpx |
| Containerization | Docker + Docker Compose |

---

## 📁 Project Structure

```
stock_portfolio/
├── alembic/
│   ├── env.py                     # Async Alembic migration environment
│   └── versions/                  # Database migration scripts
│       ├── 3004a631c566_create_user_table.py
│       └── f1a207002db9_create_portfolio_table.py
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── health.py          # GET /health & GET / endpoints
│   │       └── portfolios.py      # Portfolio CRUD endpoints
│   ├── core/
│   │   ├── config.py              # Pydantic v2 settings (.env loader)
│   │   ├── custom_docs.py         # Custom Swagger UI & Developer Portal
│   │   └── exceptions.py          # Global exception handlers
│   ├── db/
│   │   ├── base.py                # Base model & TimestampMixin
│   │   └── session.py             # Async engine & session factory
│   ├── models/
│   │   ├── user.py                # User database model
│   │   └── portfolio.py           # Portfolio database model
│   ├── schemas/
│   │   └── portfolio.py           # Portfolio Pydantic v2 validation schemas
│   ├── services/
│   │   └── portfolio_service.py   # Portfolio CRUD business logic & authorization
│   └── main.py                    # FastAPI entry point & middleware pipeline
├── tests/
│   ├── conftest.py                # Shared async pytest database fixtures
│   ├── test_day2_db.py            # User model & DB health tests
│   └── test_portfolios.py         # Portfolio CRUD API tests
├── .env                           # Local environment configuration (Git ignored)
├── .env.example                   # Template environment configuration
├── .gitignore                     # Git exclusions rules for security
├── alembic.ini                    # Alembic configuration
├── implementation_plan.md         # 15-Day internship master blueprint
├── requirements.txt               # Installed Python packages
└── README.md                      # Project documentation
```

---

## 🚀 Quick Start & Execution

### 1. Prerequisites
- Python 3.11+ (Python 3.13 recommended)
- Git

### 2. Clone the Repository & Set Up Environment
```powershell
# Clone repo
git clone https://github.com/Laxmiharika522/Stock-Portfolio-and-Investment-Management-Platform.git
cd Stock-Portfolio-and-Investment-Management-Platform

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
# source venv/bin/activate    # macOS/Linux
```

### 3. Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
cp .env.example .env
```

### 5. Run Database Migrations
```powershell
alembic upgrade head
```

### 6. Run Development Server
Start Uvicorn with auto-reload:
```powershell
python -m uvicorn app.main:app --reload --port 8000
```

### 7. Run Test Suite
```powershell
python -m pytest tests/ -v
```

---

## 🌐 Access Points & Documentation

Once the server is running, visit:

- 📊 **Developer Portal & Live Sandbox**: [http://localhost:8000/](http://localhost:8000/)
- ⚡ **Custom Dark Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📖 **ReDoc OpenAPI Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- 🏥 **Health Check API**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🔒 Security & Sensitive Data Protection (`.gitignore`)

The project enforces strict secret isolation:
- `.env` files, API keys, and secret tokens are strictly excluded from version control via `.gitignore`.
- Database binaries (`*.db`, `*.sqlite`, `*.sql`), log files (`*.log`), and temporary artifacts are ignored.
- An sanitized [`.env.example`](file:///d:/Zyora%20Internship/Stock_Market/.env.example) template is provided for safe onboarding.

---

## 📅 15-Day Development Progress

| Day | Modules / Feature | Status |
|---|---|---|
| **Day 1** | **Project setup, FastAPI boilerplate, CORS, Exceptions, Custom UI/UX, Health routes** | ✅ Completed |
| **Day 2** | **API design, entities & relationships, Pydantic request/response contracts, REST plan** | ✅ Completed |
| **Day 3** | **PostgreSQL / SQLite async SQLAlchemy 2.0 DB setup, User & Portfolio ORM models, Alembic migrations** | ✅ Completed |
| Day 4 | User registration, Password hashing (bcrypt), JWT login & refresh tokens | 🔲 Next |
| Day 5 | Stock directory, catalog search, filtering & pagination | 🔲 Planned |
| Day 6 | BUY / SELL transactions with balance validation | 🔲 Planned |
| Day 7 | Holdings calculation (weighted average buy price & unrealized P&L) | 🔲 Planned |
| Day 8 | Market data integration (Alpha Vantage API) | 🔲 Planned |
| Day 9 | Watchlist & target price alerts | 🔲 Planned |
| Day 10 | Notifications & background task monitoring | 🔲 Planned |
| Day 11 | Advanced search, multi-field filtering & sorting | 🔲 Planned |
| Day 12 | CSV file upload for bulk transaction import | 🔲 Planned |
| Day 13 | Admin panel, Role-Based Access Control (RBAC) & security hardening | 🔲 Planned |
| Day 14 | Pytest test suite & automated test runner | 🔲 Planned |
| Day 15 | Docker containerization, deployment & final review | 🔲 Planned |

---

## 👤 Author & Acknowledgments

Built as part of the **ZyoraByte 15-Day FinTech Backend Internship Programme**.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
