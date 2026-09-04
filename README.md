# 📈 Stock Portfolio & Investment Management API

A **production-grade FinTech backend API** built with FastAPI, Async SQLAlchemy 2.0, Alembic, and Pydantic v2 during a 15-day internship programme at ZyoraByte.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=flat&logo=sqlalchemy)](https://sqlalchemy.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql)](https://postgresql.org)
[![Day 4 Completed](https://img.shields.io/badge/Day%204-Completed-10b981?style=flat)](https://github.com/Laxmiharika522/Stock-Portfolio-and-Investment-Management-Platform)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Project Overview

A secure, scalable FinTech backend API designed to empower investors to:
- 🔐 **Register & authenticate** securely using JWT access & refresh tokens
- 💼 **Manage investment portfolios** (CRUD operations, currency preferences, strict ownership authorization)
- 📊 **Record BUY/SELL transactions** with live stock quantity tracking
- 📈 **Track portfolio holdings** with weighted average buy price & unrealized P&L
- 💰 **Fetch live market data** via external market APIs
- 👁️ **Watchlists & Target Price Alerts** with background notifications
- 👑 **Role-Based Access Control (RBAC)** for admin operations

---

## ✅ DAY 3 Implementation — JWT Auth, Registration & User Profiles

> **Date:** 3 Sept 2026 | **Submission:** Submitted on Time | **Status:** ✅ Completed

During **Day 3**, complete authentication workflows and user profile features were implemented:
- **Bcrypt Password Hashing:** Plaintext passwords are never stored; hashed securely via `passlib[bcrypt]`.
- **Signed JWT Tokens:** Generated and validated signed JWT access tokens (30-min validity) and refresh tokens (7-day validity) using `python-jose`.
- **Auth Routers ([`app/api/v1/auth.py`](file:///d:/Zyora%20Internship/Stock_Market/app/api/v1/auth.py)):**
  - `POST /api/v1/auth/register` — User registration with email & username uniqueness verification.
  - `POST /api/v1/auth/login` — Returns `access_token` and `refresh_token`.
  - `POST /api/v1/auth/refresh` — Generates a new access token using a valid refresh token.
  - `POST /api/v1/auth/logout` — Logout session endpoint.
- **User Profile Routers ([`app/api/v1/users.py`](file:///d:/Zyora%20Internship/Stock_Market/app/api/v1/users.py)):**
  - `GET /api/v1/users/me` — Retrieves current authenticated profile.
  - `PUT /api/v1/users/me` — Updates profile details (email, username, full name).
  - `PUT /api/v1/users/me/password` — Password change endpoint after verifying current password.

---

## ✅ DAY 4 Implementation — Portfolio Model, CRUD & Ownership Authorization

> **Date:** 4 Sept 2026 | **Submission:** Submitted on Time | **Status:** ✅ Completed

During **Day 4**, Portfolio management and multi-tenant authorization security were built and validated:
- **Portfolio Model & Schemas:** Defined [`Portfolio`](file:///d:/Zyora%20Internship/Stock_Market/app/models/portfolio.py) entity linked to `User` via foreign key (`ON DELETE CASCADE`) and created Pydantic v2 schemas (`PortfolioCreate`, `PortfolioUpdate`, `PortfolioOut`).
- **Service Layer ([`app/services/portfolio_service.py`](file:///d:/Zyora%20Internship/Stock_Market/app/services/portfolio_service.py)):**
  - Full CRUD operations with atomic async DB session management (`db.add()`, `await db.commit()`, `await db.refresh()`).
  - Automatic single default portfolio flag enforcement per user.
- **Strict Ownership Authorization ([`app/api/v1/portfolios.py`](file:///d:/Zyora%20Internship/Stock_Market/app/api/v1/portfolios.py)):**
  - Secured endpoints using `current_user: User = Depends(get_current_active_user)`.
  - Enforced strict user boundary: If User B attempts to read, update, or delete User A's portfolio, the API immediately returns `403 Forbidden` (`FORBIDDEN`).
- **Permission & Security Test Suite ([`tests/test_permissions.py`](file:///d:/Zyora%20Internship/Stock_Market/tests/test_permissions.py)):**
  - Created 15 automated pytest integration tests verifying auth, portfolio CRUD, 422 input validation details, internal sensitive field masking (`hashed_password`), and permission isolation. All 15 tests passed cleanly.

---

## 🌐 API Endpoint Summary

| Method | Endpoint | Auth Required | Description | Success Status | Error Codes |
|---|---|---|---|---|---|
| `POST` | `/api/v1/auth/register` | No | Register new user account | `201 Created` | `409 Conflict`, `422 Validation Error` |
| `POST` | `/api/v1/auth/login` | No | Authenticate & obtain JWT tokens | `200 OK` | `401 Unauthorized` |
| `POST` | `/api/v1/auth/refresh` | No | Obtain fresh access token via refresh token | `200 OK` | `401 Unauthorized` |
| `POST` | `/api/v1/auth/logout` | Yes | Logout current user session | `200 OK` | `401 Unauthorized` |
| `GET` | `/api/v1/users/me` | Yes | Get authenticated user profile | `200 OK` | `401 Unauthorized` |
| `PUT` | `/api/v1/users/me` | Yes | Update user profile details | `200 OK` | `401 Unauthorized`, `409 Conflict` |
| `PUT` | `/api/v1/users/me/password` | Yes | Change user password | `200 OK` | `400 Bad Request`, `401 Unauthorized` |
| `POST` | `/api/v1/portfolios` | Yes | Create a new investment portfolio | `201 Created` | `401 Unauthorized`, `422 Validation Error` |
| `GET` | `/api/v1/portfolios` | Yes | List portfolios owned by user | `200 OK` | `401 Unauthorized`, `403 Forbidden` |
| `GET` | `/api/v1/portfolios/{id}` | Yes | Retrieve specific portfolio details by ID | `200 OK` | `401 Unauthorized`, `403 Forbidden`, `404 Not Found` |
| `PUT` | `/api/v1/portfolios/{id}` | Yes | Update portfolio details | `200 OK` | `401 Unauthorized`, `403 Forbidden`, `404 Not Found` |
| `DELETE` | `/api/v1/portfolios/{id}` | Yes | Delete investment portfolio | `204 No Content` | `401 Unauthorized`, `403 Forbidden`, `404 Not Found` |

---

## 🔒 Security & Sensitive Data Protection (`.gitignore`)

The project enforces strict secret isolation:
- `.env` files, actual API keys, secret tokens, and private credentials are **strictly excluded from version control** via [`.gitignore`](file:///d:/Zyora%20Internship/Stock_Market/.gitignore).
- Database binaries (`*.db`, `*.sqlite`, `*.sql`), log files (`*.log`), and temporary artifacts are ignored.
- A sanitized [`.env.example`](file:///d:/Zyora%20Internship/Stock_Market/.env.example) template is provided for safe onboarding.
- Responses strictly serialize output via Pydantic schemas, hiding sensitive internal fields like `hashed_password`.

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
│   │   ├── deps.py                # Auth dependency injectors (get_current_user)
│   │   └── v1/
│   │       ├── auth.py            # JWT register, login, refresh, logout
│   │       ├── health.py          # GET /health & GET / endpoints
│   │       ├── portfolios.py      # Portfolio CRUD & ownership endpoints
│   │       └── users.py           # User profile & password management
│   ├── core/
│   │   ├── config.py              # Pydantic v2 settings (.env loader)
│   │   ├── custom_docs.py         # Custom Swagger UI & Developer Portal
│   │   ├── exceptions.py          # Global exception handlers
│   │   └── security.py            # Bcrypt password hashing & JWT tokens
│   ├── db/
│   │   ├── base.py                # Base model & TimestampMixin
│   │   └── session.py             # Async engine & session factory
│   ├── models/
│   │   ├── user.py                # User database model
│   │   └── portfolio.py           # Portfolio database model
│   ├── schemas/
│   │   ├── user.py                # User Pydantic v2 validation schemas
│   │   └── portfolio.py           # Portfolio Pydantic v2 validation schemas
│   ├── services/
│   │   ├── auth_service.py        # User authentication & registration service
│   │   └── portfolio_service.py   # Portfolio CRUD business logic & authorization
│   └── main.py                    # FastAPI entry point & middleware pipeline
├── tests/
│   ├── conftest.py                # Shared async pytest fixtures & token generators
│   ├── test_auth.py               # User registration, JWT login & profile tests
│   ├── test_day2_db.py            # User model & DB health tests
│   ├── test_permissions.py        # Multi-tenant ownership isolation tests (403 Forbidden)
│   └── test_portfolios.py         # Authenticated Portfolio CRUD API tests
├── .env.example                   # Template environment configuration (sanitized)
├── .gitignore                     # Git exclusion rules for security
├── alembic.ini                    # Alembic configuration
├── implementation_plan.md         # 15-Day internship master blueprint
├── requirements.txt               # Installed Python packages
└── README.md                      # Project documentation
```

---

## 🚀 Quick Start & Execution

### 1. Clone the Repository & Set Up Environment
```powershell
git clone https://github.com/Laxmiharika522/Stock-Portfolio-and-Investment-Management-Platform.git
cd Stock-Portfolio-and-Investment-Management-Platform

python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

### 3. Configure Environment Variables
```powershell
cp .env.example .env
```

### 4. Run Database Migrations
```powershell
alembic upgrade head
```

### 5. Run Development Server
```powershell
python -m uvicorn app.main:app --reload --port 8000
```

### 6. Run Test Suite
```powershell
$env:PYTHONPATH="."
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

## 📅 15-Day Development Progress

| Day | Modules / Feature | Status |
|---|---|---|
| **Day 1** | **Project setup, FastAPI boilerplate, CORS, Exceptions, Custom UI/UX, Health routes** | ✅ Completed |
| **Day 2** | **API design, entities & relationships, Pydantic request/response contracts, REST plan** | ✅ Completed |
| **Day 3** | **JWT authentication, user registration, bcrypt hashing, profile management & refresh tokens** | ✅ Completed |
| **Day 4** | **Portfolio model, CRUD endpoints, default portfolio handling & strict ownership authorization (403)** | ✅ Completed |
| **Day 5** | Stock directory, catalog search, filtering & pagination | 🔲 Planned |
| **Day 6** | BUY / SELL transactions with balance validation | 🔲 Planned |
| **Day 7** | Holdings calculation (weighted average buy price & unrealized P&L) | 🔲 Planned |
| **Day 8** | Market data integration (Alpha Vantage API) | 🔲 Planned |
| **Day 9** | Watchlist & target price alerts | 🔲 Planned |
| **Day 10** | Notifications & background task monitoring | 🔲 Planned |
| **Day 11** | Advanced search, multi-field filtering & sorting | 🔲 Planned |
| **Day 12** | CSV file upload for bulk transaction import | 🔲 Planned |
| **Day 13** | Admin panel, Role-Based Access Control (RBAC) & security hardening | 🔲 Planned |
| **Day 14** | Pytest test suite & automated test runner | 🔲 Planned |
| **Day 15** | Docker containerization, deployment & final review | 🔲 Planned |

---

## 👤 Author & Acknowledgments

Built as part of the **ZyoraByte 15-Day FinTech Backend Internship Programme**.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
