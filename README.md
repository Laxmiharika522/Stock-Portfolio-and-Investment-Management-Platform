# 📈 Stock Portfolio & Investment Management API

A **production-grade FinTech backend API** built with FastAPI during a 15-day internship programme at ZyoraByte.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql)](https://postgresql.org)
[![Day 1 Completed](https://img.shields.io/badge/Day%201-Completed-10b981?style=flat)](https://github.com)
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

## ✅ DAY 1 Implementation — Complete Overview

During **Day 1**, the core architectural foundations, configuration system, middleware pipeline, exception handling, health routes, custom dark-mode Swagger UI, and developer portal were fully established.

### 🌟 Day 1 Features & Accomplishments

| Feature | Module / File | Description | Status |
|---|---|---|---|
| **FastAPI Core Setup** | `app/main.py` | Initialized FastAPI app with lifespan startup/shutdown logger events. | ✅ Complete |
| **Pydantic v2 Config** | `app/core/config.py` | Configured environment settings loader (`BaseSettings`) parsing `.env`. | ✅ Complete |
| **Custom Exceptions** | `app/core/exceptions.py` | Centralized exception hierarchy (`AppException`, `NotFoundError`, `AuthenticationError`, `RateLimitError`, etc.) & JSON handlers. | ✅ Complete |
| **Glassmorphism Docs** | `app/core/custom_docs.py` | Custom dark-mode glassmorphic theme for Swagger UI (`/docs`) & Developer Portal (`/`). | ✅ Complete |
| **Security & Timing** | `app/main.py` | CORS, TrustedHost, `X-Process-Time` timing header, security headers, and request loggers. | ✅ Complete |
| **Health Endpoints** | `app/api/v1/health.py` | Serves `GET /` (Developer Portal HTML / JSON) and `GET /health` (System status). | ✅ Complete |
| **Dependencies Setup** | `requirements.txt` | Locked dependencies (FastAPI, Uvicorn, SQLAlchemy 2.0, AsyncPG, Pydantic v2, Pytest, etc.). | ✅ Complete |

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.141 |
| Language | Python 3.13 |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.x (async) |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| UI / Portal | Glassmorphic HTML5 + Custom Swagger UI Dark Theme |
| Market Data | Alpha Vantage API |
| Testing | Pytest + pytest-asyncio + httpx |
| Containerization | Docker + Docker Compose |

---

## 📁 Project Structure (Day 1 State)

```
stock_portfolio/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── health.py          # GET /health & GET / endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Pydantic v2 settings (.env loader)
│   │   ├── custom_docs.py         # Custom Swagger UI & Developer Portal
│   │   └── exceptions.py          # Global exception handlers
│   ├── __init__.py
│   └── main.py                    # FastAPI entry point & middleware pipeline
├── .env                           # Active environment configuration
├── .env.example                   # Template environment configuration
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
git clone https://github.com/YOUR_USERNAME/stock-portfolio-api.git
cd stock-portfolio-api

# Create & activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate    # macOS/Linux
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

### 5. Run Development Server
Start Uvicorn with auto-reload:
```powershell
python -m uvicorn app.main:app --reload --port 8000
```

---

## 🌐 Access Points & Documentation

Once the server is running, visit:

- 📊 **Developer Portal & Live Sandbox**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- ⚡ **Custom Dark Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 📖 **ReDoc OpenAPI Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- 🏥 **Health Check API**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 📋 Environment Variables (`.env`)

| Variable | Description | Default / Example |
|---|---|---|
| `APP_NAME` | Name of the application | `Stock Portfolio API` |
| `ENVIRONMENT` | Running environment | `development` |
| `DEBUG` | Enable debug logging | `true` |
| `DATABASE_URL` | PostgreSQL async connection URL | `postgresql+asyncpg://postgres:postgres@localhost:5432/stock_portfolio` |
| `SECRET_KEY` | JWT token signature key | `super-secret-key-change-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access Token lifetime | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh Token lifetime | `7` |
| `ALPHA_VANTAGE_API_KEY` | Stock market data key | `demo` |

---

## 📅 15-Day Development Progress

| Day | Modules / Feature | Status |
|---|---|---|
| **Day 1** | **Project setup, FastAPI boilerplate, CORS, Exceptions, Custom UI/UX, Health routes** | ✅ Completed |
| Day 2 | PostgreSQL connection, Async SQLAlchemy 2.0, User ORM model, Alembic migrations | 🔲 Next |
| Day 3 | User registration, Password hashing (bcrypt), JWT login & refresh tokens | 🔲 Planned |
| Day 4 | Portfolio CRUD operations, currency settings & ownership rules | 🔲 Planned |
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
