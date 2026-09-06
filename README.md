# 📈 Stock Portfolio & Investment Management API

A **production-grade FinTech backend API** built with FastAPI, Async SQLAlchemy 2.0, Alembic, and Pydantic v2 during a 15-day internship programme at ZyoraByte.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=flat&logo=sqlalchemy)](https://sqlalchemy.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql)](https://postgresql.org)
[![Day 5 Completed](https://img.shields.io/badge/Day%205-Completed-10b981?style=flat)](https://github.com/Laxmiharika522/Stock-Portfolio-and-Investment-Management-Platform)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Project Overview

A secure, scalable FinTech backend API designed to empower investors to:
- 🔐 **Register & authenticate** securely using JWT access & refresh tokens
- 💼 **Manage investment portfolios** (CRUD operations, currency preferences, strict ownership authorization)
- 📈 **Browse stock catalog** (advanced search, sector/exchange filtering, pagination metadata, and admin catalog controls)
- 📊 **Record BUY/SELL transactions** with live stock quantity tracking
- 📈 **Track portfolio holdings** with weighted average buy price & unrealized P&L
- 💰 **Fetch live market data** via external market APIs
- 👁️ **Watchlists & Target Price Alerts** with background notifications
- 👑 **Role-Based Access Control (RBAC)** for admin operations

---

## ✅ DAY 1 Implementation — Project Setup, HTTP Foundations & REST Architecture

> **Date:** 1 Sept 2026 | **Submission:** Submitted on Time | **Status:** ✅ Completed

During **Day 1**, core infrastructure, application architecture, and middleware pipelines were established:
- **FastAPI Core Setup:** Configured FastAPI entry point ([`app/main.py`](file:///d:/Zyora%20Internship/Stock_Market/app/main.py)) with lifespan manager, CORS middleware, timing header middleware (`X-Process-Time`), and security headers.
- **Environment & Settings:** Environment variable loader ([`app/core/config.py`](file:///d:/Zyora%20Internship/Stock_Market/app/core/config.py)) using `pydantic-settings` reading from `.env`.
- **Global Exception Architecture:** Unified JSON error payload format via custom exception handlers ([`app/core/exceptions.py`](file:///d:/Zyora%20Internship/Stock_Market/app/core/exceptions.py)).
- **Custom UI & Developer Portal:** Glassmorphism styled developer UI portal landing page and custom Swagger UI dark theme ([`app/core/custom_docs.py`](file:///d:/Zyora%20Internship/Stock_Market/app/core/custom_docs.py)).
- **Health Check Router:** `GET /` and `GET /health` endpoints ([`app/api/v1/health.py`](file:///d:/Zyora%20Internship/Stock_Market/app/api/v1/health.py)).

---

## ✅ DAY 2 Implementation — PostgreSQL, Async SQLAlchemy 2.0 & Database Setup

> **Date:** 2 Sept 2026 | **Submission:** Submitted on Time | **Status:** ✅ Completed

During **Day 2**, database persistence layers and async ORM models were connected:
- **Async Database Connection:** Configured async engine and session factory (`AsyncSessionLocal`) in [`app/db/session.py`](file:///d:/Zyora%20Internship/Stock_Market/app/db/session.py) supporting PostgreSQL and SQLite (`aiosqlite`).
- **Declarative Base & Mixins:** Created declarative base [`Base`](file:///d:/Zyora%20Internship/Stock_Market/app/db/base.py) with `TimestampMixin` generating automated `created_at` and `updated_at` timestamps.
- **User ORM Entity:** Defined primary [`User`](file:///d:/Zyora%20Internship/Stock_Market/app/models/user.py) model with UUID v4 primary keys, index constraints, and RBAC flags (`is_admin`).
- **Alembic Database Migrations:** Initialized Alembic environment ([`alembic/env.py`](file:///d:/Zyora%20Internship/Stock_Market/alembic/env.py)) and applied initial schema migration (`3004a631c566_create_user_table.py`).

---

## ✅ DAY 3 Implementation — User Registration, Password Hashing & JWT Authentication

> **Date:** 3 Sept 2026 | **Submission:** Submitted on Time | **Status:** ✅ Completed

During **Day 3**, complete authentication workflows and user profile features were implemented:
- **Bcrypt Password Hashing:** Plaintext passwords are never stored; hashed securely via `passlib[bcrypt]`.
- **Signed JWT Tokens:** Generated and validated signed JWT access tokens (30-min validity) and refresh tokens (7-day validity) using `python-jose` ([`app/core/security.py`](file:///d:/Zyora%20Internship/Stock_Market/app/core/security.py)).
- **Auth Routers ([`app/api/v1/auth.py`](file:///d:/Zyora%20Internship/Stock_Market/app/api/v1/auth.py)):**
  - `POST /api/v1/auth/register` — User registration with email & username uniqueness verification.
  - `POST /api/v1/auth/login` — Authenticates credentials and returns `access_token` and `refresh_token`.
  - `POST /api/v1/auth/refresh` — Generates a new access token using a valid refresh token.
  - `POST /api/v1/auth/logout` — Revokes active session.
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
  - Automated pytest integration tests verifying auth, portfolio CRUD, input validation, internal sensitive field masking (`hashed_password`), and permission isolation.

---

## ✅ DAY 5 Implementation — Stock Catalog, Search, Filtering, Pagination & Admin Controls

> **Date:** 5 Sept 2026 | **Submission:** Submitted on Time | **Status:** ✅ Completed

During **Day 5**, the global Stock catalog, search & filtering query engine, pagination response wrapper, and admin management endpoints were built and verified:
- **Stock Database Model ([`app/models/stock.py`](file:///d:/Zyora%20Internship/Stock_Market/app/models/stock.py)):**
  - Designed [`Stock`](file:///d:/Zyora%20Internship/Stock_Market/app/models/stock.py) entity holding `symbol` (unique, uppercase indexed), `company_name` (indexed), `sector` (indexed), `exchange` (indexed), `industry`, `currency`, `description`, `logo_url`, `market_cap`, and `is_active`.
  - Alembic database migration script ([`alembic/versions/7a892b104c21_create_stock_table.py`](file:///d:/Zyora%20Internship/Stock_Market/alembic/versions/7a892b104c21_create_stock_table.py)) created with indexes.
- **Pydantic v2 Schemas ([`app/schemas/stock.py`](file:///d:/Zyora%20Internship/Stock_Market/app/schemas/stock.py)):**
  - Created `StockCreate`, `StockUpdate`, `StockOut`, and generic `PaginatedStockResponse` wrapper schema containing `items`, `total`, `page`, `page_size`, and calculated `total_pages`.
- **Stock Business Service & Seed Catalog ([`app/services/stock_service.py`](file:///d:/Zyora%20Internship/Stock_Market/app/services/stock_service.py)):**
  - Built `list_stocks()` with multi-field search (`q` matching symbol or company name using case-insensitive `ilike`), sector filtering, exchange filtering, dynamic sorting (`sort_by`, `order`), and offset/limit pagination.
  - Implemented `seed_popular_stocks()` pre-loading 22 popular global equities (AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META, BRK.A, V, JNJ, WMT, JPM, PG, UNH, MA, HD, DIS, PYPL, NFLX, ADBE, AMD, INTC).
- **Stock Routers ([`app/api/v1/stocks.py`](file:///d:/Zyora%20Internship/Stock_Market/app/api/v1/stocks.py)):**
  - `GET /api/v1/stocks` — Public searchable, filterable, paginated stock catalog listing.
  - `GET /api/v1/stocks/{symbol}` — Ticker symbol details lookup (case-insensitive, 404 error handling).
  - `POST /api/v1/stocks` — Admin-only stock creation endpoint (`get_current_admin_user` dependency, 409 conflict on duplicate symbol).
  - `PUT /api/v1/stocks/{symbol}` — Admin-only stock details update endpoint (403 forbidden for non-admins).
  - `POST /api/v1/stocks/seed` — Admin catalog seed trigger endpoint.
- **Stock Automated Test Suite ([`tests/test_stocks.py`](file:///d:/Zyora%20Internship/Stock_Market/tests/test_stocks.py)):**
  - Created automated integration tests verifying stock catalog listing, keyword search, sector filtering, pagination calculation, case-insensitive symbol lookup, admin stock creation, duplicate conflict detection, and RBAC permission protection (403 Forbidden for non-admin attempts).

---

## 🌐 API Endpoint Summary

| Method | Endpoint | Auth Required | Description | Success Status | Error Codes |
|---|---|---|---|---|---|
| `GET` | `/` | No | HTML Developer Portal & API Overview | `200 OK` | — |
| `GET` | `/health` | No | API & Database Connectivity Status | `200 OK` | `503 Service Unavailable` |
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
| `GET` | `/api/v1/stocks` | No | Search, filter & paginate stock catalog | `200 OK` | `422 Validation Error` |
| `GET` | `/api/v1/stocks/{symbol}` | No | Get detailed stock record by ticker symbol | `200 OK` | `404 Not Found` |
| `POST` | `/api/v1/stocks` | Admin | Create new stock record in catalog | `201 Created` | `401 Unauthorized`, `403 Forbidden`, `409 Conflict` |
| `PUT` | `/api/v1/stocks/{symbol}` | Admin | Update existing stock record | `200 OK` | `401 Unauthorized`, `403 Forbidden`, `404 Not Found` |
| `POST` | `/api/v1/stocks/seed` | Admin | Seed popular stock catalog assets | `200 OK` | `401 Unauthorized`, `403 Forbidden` |

---

## 🔒 Security & Sensitive Data Protection (`.gitignore`)

The project enforces strict secret isolation:
- `.env` files, actual API keys, secret tokens, and private credentials are **strictly excluded from version control** via [`.gitignore`](file:///d:/Zyora%20Internship/Stock_Market/.gitignore).
- Database binaries (`*.db`, `*.sqlite`, `*.sql`), log files (`*.log`), and temporary artifacts are ignored.
- A sanitized [`.env.example`](file:///d:/Zyora%20Internship/Stock_Market/.env.example) template is provided for safe onboarding.
- Responses strictly serialize output via Pydantic schemas, hiding sensitive internal fields like `hashed_password`.
- Admin endpoints verify `is_admin` boolean flag, blocking unauthorized callers with structured `403 Forbidden` error payloads.

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
│       ├── f1a207002db9_create_portfolio_table.py
│       └── 7a892b104c21_create_stock_table.py
├── app/
│   ├── api/
│   │   ├── deps.py                # Auth dependency injectors (get_current_user, get_current_admin_user)
│   │   └── v1/
│   │       ├── auth.py            # JWT register, login, refresh, logout
│   │       ├── health.py          # GET /health & GET / endpoints
│   │       ├── portfolios.py      # Portfolio CRUD & ownership endpoints
│   │       ├── stocks.py          # Stock catalog search, filter, pagination & admin endpoints
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
│   │   ├── portfolio.py           # Portfolio database model
│   │   └── stock.py              # Stock catalog database model
│   ├── schemas/
│   │   ├── user.py                # User Pydantic v2 validation schemas
│   │   ├── portfolio.py           # Portfolio Pydantic v2 validation schemas
│   │   └── stock.py              # Stock catalog & pagination schemas
│   ├── services/
│   │   ├── auth_service.py        # User authentication & registration service
│   │   ├── portfolio_service.py   # Portfolio CRUD business logic & authorization
│   │   └── stock_service.py       # Stock catalog query engine, search, filter & seed service
│   └── main.py                    # FastAPI entry point & middleware pipeline
├── tests/
│   ├── conftest.py                # Shared async pytest fixtures & token generators (user_a, user_b, admin)
│   ├── test_auth.py               # User registration, JWT login & profile tests
│   ├── test_day2_db.py            # User model & DB health tests
│   ├── test_permissions.py        # Multi-tenant ownership isolation tests (403 Forbidden)
│   ├── test_portfolios.py         # Authenticated Portfolio CRUD API tests
│   └── test_stocks.py             # Stock catalog search, filter, pagination & admin protection tests
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

python -m venv .venv
.\.venv\Scripts\Activate.ps1
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
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

---

## 🌐 Access Points & Documentation

Once the server is running, visit:
- 📊 **Developer Portal & Live Sandbox**: [http://localhost:8000/](http://localhost:8000/)
- ⚡ **Custom Dark Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📖 **ReDoc OpenAPI Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- 🏥 **Health Check API**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🧪 Automated Test Suite Results

All 22 integration & permission unit tests pass cleanly:

```text
tests/test_auth.py ....                                                  [ 18%]
tests/test_day2_db.py ....                                               [ 36%]
tests/test_permissions.py .....                                          [ 59%]
tests/test_portfolios.py ..                                              [ 68%]
tests/test_stocks.py .......                                             [100%]

======================= 22 passed in 6.22s =======================
```

---

## 📅 15-Day Development Progress

| Day | Modules / Feature | Status |
|---|---|---|
| **Day 1** | **Project setup, FastAPI boilerplate, CORS, Exceptions, Custom UI/UX, Health routes** | ✅ Completed |
| **Day 2** | **PostgreSQL async setup, User model, Alembic migrations & declarative base** | ✅ Completed |
| **Day 3** | **JWT authentication, user registration, bcrypt hashing, profile management & refresh tokens** | ✅ Completed |
| **Day 4** | **Portfolio model, CRUD endpoints, default portfolio handling & strict ownership authorization (403)** | ✅ Completed |
| **Day 5** | **Stock catalog model, search engine, sector/exchange filtering, pagination metadata & admin endpoints** | ✅ Completed |
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
