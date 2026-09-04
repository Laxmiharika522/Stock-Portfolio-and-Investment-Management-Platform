# 📈 Stock Portfolio & Investment Management Platform
### 15-Day Internship Implementation Plan — Production-Grade FinTech Backend

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | FastAPI (async) |
| **Language** | Python 3.11+ |
| **Database** | PostgreSQL 15 |
| **ORM** | SQLAlchemy 2.x (async) |
| **Migrations** | Alembic |
| **Validation** | Pydantic v2 |
| **Auth** | JWT (python-jose), bcrypt (passlib) |
| **Market Data** | Alpha Vantage / Yahoo Finance (yfinance) |
| **Background Tasks** | FastAPI BackgroundTasks + APScheduler |
| **Testing** | Pytest + pytest-asyncio + httpx |
| **Containerization** | Docker + Docker Compose |
| **Cache** | Redis (optional, for rate-limit & price cache) |
| **Deployment** | Railway / Render / Fly.io |
| **Docs** | OpenAPI / Swagger (built-in) |
| **Version Control** | Git + GitHub |

---

## 📐 Database Models (7 Models)

```
User ──< Portfolio ──< Holding ──< Stock
         │                         │
         └──< Transaction ─────────┘
         │
         └──< Watchlist ──> Stock
         │
         └──< Notification
```

---

## 📁 Project Structure (Final)

```
stock_portfolio/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── portfolios.py
│   │   │   ├── stocks.py
│   │   │   ├── transactions.py
│   │   │   ├── holdings.py
│   │   │   ├── watchlist.py
│   │   │   ├── notifications.py
│   │   │   ├── market.py
│   │   │   ├── upload.py
│   │   │   └── admin.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── exceptions.py
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── init_db.py
│   ├── models/
│   │   ├── user.py
│   │   ├── portfolio.py
│   │   ├── stock.py
│   │   ├── holding.py
│   │   ├── transaction.py
│   │   ├── watchlist.py
│   │   └── notification.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── portfolio.py
│   │   ├── stock.py
│   │   ├── holding.py
│   │   ├── transaction.py
│   │   ├── watchlist.py
│   │   └── notification.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── portfolio_service.py
│   │   ├── transaction_service.py
│   │   ├── market_service.py
│   │   ├── notification_service.py
│   │   └── upload_service.py
│   ├── tasks/
│   │   └── price_monitor.py
│   └── main.py
├── alembic/
│   ├── env.py
│   └── versions/
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_portfolios.py
│   ├── test_transactions.py
│   ├── test_holdings.py
│   ├── test_watchlist.py
│   ├── test_admin.py
│   └── test_permissions.py   ← CRITICAL isolation tests
├── .env
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 📅 Day-by-Day Plan

---

### ✅ DAY 1 — Project Setup, HTTP Foundations & Environment

**Goal:** Lay the foundation. Understand HTTP/REST, set up the repo and run your first FastAPI app.

**Learning Concepts:**
- HTTP methods: GET, POST, PUT, PATCH, DELETE
- Status codes: 200, 201, 400, 401, 403, 404, 422, 500
- REST resource naming conventions
- FastAPI project structure & routing

**Tasks:**
1. Create GitHub repo: `stock-portfolio-api`
2. Set up Python virtual environment (`python -m venv venv`)
3. Install core dependencies:
   ```
   fastapi uvicorn[standard] python-dotenv pydantic[email] pydantic-settings
   ```
4. Create `app/main.py` with:
   - `/` health check endpoint
   - `/health` with DB status
   - Global exception handlers
   - CORS middleware
5. Create `app/core/config.py` using `pydantic-settings` for `.env` loading
6. Create structured error responses (custom `HTTPException` handler)
7. Write `README.md` stub with project overview
8. Push to GitHub with commit: `Day 1: Project setup, FastAPI boilerplate, REST foundations`

**Deliverables:**
- Running FastAPI server at `http://localhost:8000`
- Swagger docs at `/docs`
- Clean project structure committed to GitHub

---

### ✅ DAY 2 — PostgreSQL, Async SQLAlchemy & Database Setup

**Goal:** Connect FastAPI to PostgreSQL using async SQLAlchemy. Understand ORM models and sessions.

**Learning Concepts:**
- Async vs sync DB sessions
- SQLAlchemy 2.x declarative base
- Connection pooling
- Database URL configuration

**Tasks:**
1. Install dependencies:
   ```
   asyncpg sqlalchemy[asyncio] alembic psycopg2-binary
   ```
2. Create `app/db/session.py` — async engine + session factory
3. Create `app/db/base.py` — `DeclarativeBase` with `created_at`, `updated_at` mixins
4. Create the **User** model (`app/models/user.py`):
   - `id` (UUID), `email`, `username`, `hashed_password`
   - `full_name`, `is_active`, `is_admin`, `created_at`, `updated_at`
5. Initialize Alembic: `alembic init alembic`
6. Configure `alembic/env.py` for async engine
7. Create first migration: `alembic revision --autogenerate -m "create_user_table"`
8. Apply migration: `alembic upgrade head`
9. Verify table in PostgreSQL
10. Push: `Day 2: PostgreSQL async setup, User model, Alembic migration`

**Deliverables:**
- PostgreSQL connected via async SQLAlchemy
- `users` table created via Alembic
- Migration files committed

---

### ✅ DAY 3 — User Registration, Password Hashing & JWT Authentication

**Goal:** Implement complete auth system with secure password storage and JWT tokens.

**Learning Concepts:**
- bcrypt password hashing (never store plain text)
- JWT structure: header.payload.signature
- Access vs Refresh tokens
- Dependency injection in FastAPI

**Tasks:**
1. Install:
   ```
   passlib[bcrypt] python-jose[cryptography]
   ```
2. Create `app/core/security.py`:
   - `hash_password()`, `verify_password()`
   - `create_access_token()`, `create_refresh_token()`
   - `decode_token()`
3. Create Pydantic schemas (`app/schemas/user.py`):
   - `UserCreate`, `UserLogin`, `UserOut`, `Token`, `TokenRefresh`
4. Create `app/api/v1/auth.py`:
   - `POST /auth/register` — register with email uniqueness check
   - `POST /auth/login` — return access + refresh tokens
   - `POST /auth/refresh` — refresh access token
   - `POST /auth/logout` (token blacklist concept)
5. Create `app/api/deps.py`:
   - `get_current_user` dependency
   - `get_current_active_user` dependency
   - `get_current_admin_user` dependency
6. Create `app/api/v1/users.py`:
   - `GET /users/me` — get own profile
   - `PUT /users/me` — update profile
   - `PUT /users/me/password` — change password
7. Push: `Day 3: JWT auth, user registration, password hashing, profile endpoints`

**Deliverables:**
- Working register + login flow
- JWT token returned and usable in Swagger Authorize
- Protected `/users/me` endpoint

---

### ✅ DAY 4 — Portfolio Model, CRUD & Ownership Authorization

**Goal:** Build Portfolio management with strict ownership enforcement.

**Learning Concepts:**
- One-to-many relationships in SQLAlchemy
- Ownership checks (User A ≠ User B's data)
- CRUD service layer pattern

**Tasks:**
1. Create **Portfolio** model (`app/models/portfolio.py`):
   - `id`, `user_id` (FK→User), `name`, `description`
   - `currency` (default: USD), `is_default`, `created_at`, `updated_at`
2. Create Alembic migration: `alembic revision --autogenerate -m "create_portfolio_table"`
3. Create schemas: `PortfolioCreate`, `PortfolioUpdate`, `PortfolioOut`
4. Create `app/services/portfolio_service.py` with full CRUD
5. Create `app/api/v1/portfolios.py`:
   - `POST /portfolios` — create portfolio
   - `GET /portfolios` — list user's portfolios (only own!)
   - `GET /portfolios/{id}` — get specific portfolio (ownership check → 403 if not own)
   - `PUT /portfolios/{id}` — update portfolio
   - `DELETE /portfolios/{id}` — soft delete
6. **Critical:** Every endpoint must verify `portfolio.user_id == current_user.id`
7. Add response model with `total_value` placeholder
8. Push: `Day 4: Portfolio CRUD, ownership authorization, one-to-many relationships`

**Deliverables:**
- Portfolio endpoints working
- User A cannot access User B's portfolios (returns 403)

---

### ✅ DAY 5 — Stock Model, Search, Filtering & Pagination

**Goal:** Build the Stock catalog with advanced search, filter, and pagination.

**Learning Concepts:**
- SQLAlchemy query building with filters
- Offset/limit vs cursor-based pagination
- ilike for case-insensitive search
- Indexing for performance

**Tasks:**
1. Create **Stock** model (`app/models/stock.py`):
   - `id`, `symbol` (unique, indexed), `company_name`, `sector`, `industry`
   - `exchange`, `currency`, `description`, `logo_url`
   - `market_cap`, `is_active`, `created_at`, `updated_at`
2. Alembic migration: `create_stock_table`
3. Create schemas: `StockCreate`, `StockUpdate`, `StockOut`, `StockSearch`
4. Create `app/api/v1/stocks.py`:
   - `GET /stocks` — list with search, filter, sort, pagination
     - Query params: `q`, `sector`, `exchange`, `sort_by`, `order`, `page`, `page_size`
   - `GET /stocks/{symbol}` — get stock by symbol
   - `POST /stocks` — admin only (create stock)
   - `PUT /stocks/{symbol}` — admin only (update stock)
5. Create `PaginatedResponse` generic schema
6. Seed script: insert 20+ popular stocks (AAPL, GOOGL, MSFT, etc.)
7. Add DB indexes: `symbol`, `sector`, `exchange`
8. Push: `Day 5: Stock catalog, search/filter/pagination, admin-only endpoints`

**Deliverables:**
- Stocks searchable by symbol/name/sector
- Pagination working with metadata (total, page, pages)

---

### ✅ DAY 6 — Transaction Model & BUY/SELL Business Logic

**Goal:** Implement the core financial logic — recording and validating transactions.

**Learning Concepts:**
- Complex business rules in service layer
- Database transactions (atomicity)
- Preventing overselling (data integrity)

**Tasks:**
1. Create **Transaction** model (`app/models/transaction.py`):
   - `id`, `portfolio_id` (FK), `stock_id` (FK), `user_id` (FK)
   - `type` (enum: BUY/SELL), `quantity`, `price_per_share`
   - `total_amount`, `fees`, `notes`, `transaction_date`, `created_at`
2. Create **Holding** model (`app/models/holding.py`):
   - `id`, `portfolio_id` (FK), `stock_id` (FK), `user_id` (FK)
   - `quantity`, `average_buy_price`, `total_invested`, `created_at`, `updated_at`
3. Alembic migration: `create_transaction_holding_tables`
4. Create `app/services/transaction_service.py`:
   - BUY logic: create transaction → upsert holding (update avg price using weighted avg)
   - SELL logic: validate enough shares → create transaction → reduce holding quantity
   - **Weighted Average Price formula:**
     `new_avg = (old_qty * old_avg + new_qty * new_price) / (old_qty + new_qty)`
   - Auto-delete holding if quantity reaches 0
5. Create `app/api/v1/transactions.py`:
   - `POST /portfolios/{id}/transactions` — record BUY or SELL
   - `GET /portfolios/{id}/transactions` — list with filters (type, date range, stock)
   - `GET /portfolios/{id}/transactions/{tx_id}` — get specific transaction
6. Push: `Day 6: BUY/SELL transactions, holding updates, weighted avg price logic`

**Deliverables:**
- BUY records holding and calculates weighted average price
- SELL validates quantity, returns 400 if insufficient shares

---

### ✅ DAY 7 — Holdings Endpoints & Portfolio Performance Calculation

**Goal:** Expose holdings data and implement profit/loss calculations.

**Learning Concepts:**
- Financial metrics: unrealized P&L, portfolio value
- Async service orchestration
- Data aggregation patterns

**Tasks:**
1. Create `app/api/v1/holdings.py`:
   - `GET /portfolios/{id}/holdings` — list all holdings with current value
   - `GET /portfolios/{id}/holdings/{stock_symbol}` — specific holding detail
2. Create portfolio performance calculation in `portfolio_service.py`:
   ```
   total_invested = sum(holding.quantity * holding.average_buy_price)
   current_value  = sum(holding.quantity * current_market_price)
   profit_loss    = current_value - total_invested
   pl_percentage  = (profit_loss / total_invested) * 100
   ```
3. Update `GET /portfolios/{id}` response to include:
   - `total_invested`, `current_value`, `profit_loss`, `pl_percentage`
   - `holdings_count`, `top_holdings`
4. Create `GET /portfolios/{id}/performance` — detailed performance breakdown:
   - Per-holding P&L
   - Sector allocation
   - Best/worst performing stocks
5. Add `GET /portfolios/summary` — aggregated view across all user portfolios
6. Push: `Day 7: Holdings API, portfolio performance, P&L calculation`

**Deliverables:**
- Portfolio shows total value, profit/loss, P&L %
- Holdings show per-stock performance

---

### ✅ DAY 8 — External Market Data API Integration

**Goal:** Fetch real-time stock prices from an external API and cache results.

**Learning Concepts:**
- Async HTTP clients (httpx)
- API key management via environment variables
- Caching to avoid rate limits
- Graceful fallback / mock data

**Tasks:**
1. Install: `httpx`
2. Create `app/services/market_service.py`:
   - Alpha Vantage or Yahoo Finance (`yfinance`) integration
   - `get_current_price(symbol: str) -> Decimal`
   - `get_batch_prices(symbols: list[str]) -> dict`
   - Fallback to mock prices if API unavailable
3. Implement in-memory LRU cache (15-min TTL) using `cachetools` or `functools.lru_cache`
   - Optional: Redis cache for production
4. Create `app/api/v1/market.py`:
   - `GET /market/price/{symbol}` — get current price
   - `GET /market/prices` — batch prices (comma-separated symbols)
   - `GET /market/quote/{symbol}` — full quote (price, change, % change, volume)
   - `GET /market/history/{symbol}` — historical price data
5. Update performance calculation to use live prices
6. Handle API errors gracefully (rate limits, unknown symbols)
7. Push: `Day 8: External market data integration, price caching, live P&L`

**Deliverables:**
- Live prices fetched from external API
- Portfolio value updates with real prices
- Graceful degradation when API is unavailable

---

### ✅ DAY 9 — Watchlist & Target Price Monitoring

**Goal:** Build the watchlist feature and background price monitoring.

**Learning Concepts:**
- Many-to-many through association model
- FastAPI BackgroundTasks
- Event-driven architecture basics

**Tasks:**
1. Create **Watchlist** model (`app/models/watchlist.py`):
   - `id`, `user_id` (FK), `stock_id` (FK)
   - `target_price`, `alert_type` (enum: ABOVE/BELOW), `notes`
   - `is_triggered`, `triggered_at`, `created_at`
2. Alembic migration: `create_watchlist_table`
3. Create schemas: `WatchlistCreate`, `WatchlistUpdate`, `WatchlistOut`
4. Create `app/api/v1/watchlist.py`:
   - `POST /watchlist` — add stock to watchlist with target price
   - `GET /watchlist` — list user's watchlist with current prices
   - `PUT /watchlist/{id}` — update target price
   - `DELETE /watchlist/{id}` — remove from watchlist
5. Create `app/tasks/price_monitor.py`:
   - Background task: check watchlist prices against targets
   - Trigger notification when target price is hit
6. Wire background task to run on `POST /watchlist` and on market data refresh
7. Push: `Day 9: Watchlist with target prices, background price monitoring`

**Deliverables:**
- Users can create watchlist items with target prices
- Background task detects when price crosses target

---

### ✅ DAY 10 — Notifications System & Advanced Background Tasks

**Goal:** Build the in-app notification system and scheduled monitoring.

**Learning Concepts:**
- FastAPI BackgroundTasks vs APScheduler
- Notification patterns
- Idempotency in notifications

**Tasks:**
1. Create **Notification** model (`app/models/notification.py`):
   - `id`, `user_id` (FK), `type` (enum: PRICE_ALERT, SYSTEM, TRADE_CONFIRM, etc.)
   - `title`, `message`, `is_read`, `related_stock_id`, `metadata` (JSON)
   - `created_at`, `read_at`
2. Alembic migration: `create_notification_table`
3. Create `app/services/notification_service.py`:
   - `create_notification(user_id, type, title, message)`
   - `mark_as_read(notification_id, user_id)`
   - `get_unread_count(user_id)`
4. Create `app/api/v1/notifications.py`:
   - `GET /notifications` — list with filter (read/unread, type)
   - `PUT /notifications/{id}/read` — mark as read
   - `PUT /notifications/read-all` — mark all as read
   - `GET /notifications/unread-count` — count badge
   - `DELETE /notifications/{id}` — delete
5. Install APScheduler: schedule price check every 5 minutes
6. Wire notifications: trade confirmations, price alerts, system messages
7. Push: `Day 10: In-app notifications, APScheduler price monitoring, alert system`

**Deliverables:**
- Notifications created on BUY/SELL and price alerts
- Scheduled task runs every 5 minutes

---

### ✅ DAY 11 — Advanced Search, Filtering, Sorting & Pagination

**Goal:** Add production-grade query capabilities across all major endpoints.

**Learning Concepts:**
- Reusable query parameter patterns
- SQLAlchemy dynamic filter building
- Cursor-based pagination
- Query performance optimization

**Tasks:**
1. Create reusable `app/core/pagination.py`:
   - `PaginationParams` dependency class
   - `paginate(query, params)` utility
   - Standard `Page[T]` generic response schema
2. Enhance `GET /portfolios/{id}/transactions` with:
   - Filter: `type` (BUY/SELL), `stock_symbol`, `date_from`, `date_to`
   - Sort: `transaction_date`, `total_amount`, `quantity`
   - Search: stock symbol or company name
3. Enhance `GET /stocks` with:
   - Full-text search across `symbol` + `company_name`
   - Filter: `sector`, `exchange`, `is_active`
   - Sort: `market_cap`, `symbol`, `company_name`
4. Add `GET /portfolios/{id}/holdings` with:
   - Sort: `profit_loss`, `current_value`, `quantity`
   - Filter by sector
5. Add transaction summary/analytics endpoint:
   - `GET /portfolios/{id}/analytics` — monthly P&L, sector breakdown, trading volume
6. Push: `Day 11: Advanced search, filtering, sorting, pagination across all endpoints`

**Deliverables:**
- All list endpoints support `?q=&sort_by=&order=asc/desc&page=&page_size=`
- Consistent paginated response format

---

### ✅ DAY 12 — File Upload: CSV Transaction Import

**Goal:** Allow users to bulk-import transactions via CSV upload with full validation.

**Learning Concepts:**
- FastAPI file upload (`UploadFile`)
- CSV parsing and validation
- Error collection and reporting
- File size and type validation

**Tasks:**
1. Install: `python-multipart pandas` (or standard `csv` module)
2. Create `app/services/upload_service.py`:
   - Validate file type (`.csv` only)
   - Validate file size (max 5MB)
   - Parse and validate CSV rows:
     - Required columns: `symbol`, `type`, `quantity`, `price`, `date`
     - Validate each row individually
     - Collect all errors (don't stop at first error)
   - Dry-run mode: validate without committing
   - Import mode: process all valid rows, report skipped rows
3. Create `app/api/v1/upload.py`:
   - `POST /portfolios/{id}/import` — upload CSV, return success/error report
   - `POST /portfolios/{id}/import/validate` — dry-run validation only
4. Create CSV template endpoint:
   - `GET /upload/template` — download sample CSV template
5. Return structured import report:
   ```json
   {
     "total_rows": 50,
     "successful": 48,
     "failed": 2,
     "errors": [
       {"row": 5, "error": "Insufficient shares for SELL transaction"}
     ]
   }
   ```
6. Push: `Day 12: CSV transaction import, file validation, bulk upload with error reporting`

**Deliverables:**
- CSV upload works with validation
- Import report shows per-row success/failure

---

### ✅ DAY 13 — Admin Panel, RBAC & Security Hardening

**Goal:** Build admin endpoints, implement role-based authorization, and harden security.

**Learning Concepts:**
- Role-based access control (RBAC)
- Rate limiting
- Input sanitization
- Security headers

**Tasks:**
1. Create `app/api/v1/admin.py` — admin-only endpoints:
   - `GET /admin/users` — list all users with filters
   - `PUT /admin/users/{id}/activate` — activate/deactivate user
   - `PUT /admin/users/{id}/role` — promote/demote admin
   - `GET /admin/stats` — platform statistics (total users, portfolios, transactions)
   - `GET /admin/stocks` — full stock management
   - `POST /admin/stocks` — create stock (moved here from public)
   - `DELETE /admin/stocks/{symbol}` — delete stock
2. Install `slowapi`: add rate limiting to auth endpoints
   - `/auth/login`: 5 requests/minute
   - `/auth/register`: 3 requests/minute
3. Add security headers middleware (HSTS, X-Content-Type-Options)
4. Implement token blacklisting on logout (Redis or DB set)
5. Add `GET /admin/audit-log` — log of admin actions
6. Validate all user inputs against injection (Pydantic handles most, add extra checks)
7. Push: `Day 13: Admin panel, RBAC, rate limiting, security hardening`

**Deliverables:**
- Normal users cannot access `/admin/*` (403)
- Rate limiting active on auth endpoints
- Security headers present in all responses

---

### ✅ DAY 14 — Testing Suite: Pytest, Integration Tests & Permission Isolation

**Goal:** Write comprehensive tests covering all major features with emphasis on permission isolation.

**Learning Concepts:**
- pytest-asyncio for async tests
- httpx AsyncClient for API testing
- Test fixtures and conftest
- Permission isolation testing patterns

**Tasks:**
1. Install: `pytest pytest-asyncio httpx pytest-cov`
2. Create `tests/conftest.py`:
   - Async test DB (separate test database)
   - `async_client` fixture
   - `user_a_token`, `user_b_token` fixtures
   - `admin_token` fixture
   - Seed data fixtures (portfolios, stocks, transactions)
3. Write tests:

   **`test_auth.py`:**
   - Register with valid/invalid data
   - Login with correct/wrong password
   - Access protected endpoint without token
   - Refresh token flow

   **`test_portfolios.py`:**
   - Create, read, update, delete portfolio
   - List returns only user's portfolios

   **`test_permissions.py` (CRITICAL):**
   - User A cannot GET User B's portfolio → 403
   - User A cannot PUT User B's portfolio → 403
   - User A cannot DELETE User B's portfolio → 403
   - User A cannot view User B's transactions → 403
   - Non-admin cannot access `/admin/*` → 403
   - Admin CAN access `/admin/*` → 200

   **`test_transactions.py`:**
   - BUY creates holding
   - SELL reduces holding
   - SELL more than owned → 400
   - Weighted average price calculation correct

   **`test_holdings.py`:**
   - Holdings update after BUY/SELL
   - P&L calculation accuracy

   **`test_watchlist.py`:**
   - Add/remove from watchlist
   - Target price notification trigger

4. Run: `pytest tests/ --cov=app --cov-report=html`
5. Aim for **>80% code coverage**
6. Push: `Day 14: Comprehensive test suite, permission isolation tests, 80%+ coverage`

**Deliverables:**
- All tests passing
- Coverage report showing >80%
- Permission isolation tests explicitly passing

---

### ✅ DAY 15 — Docker, Deployment, Documentation & Final Review

**Goal:** Containerize, deploy, document, and present the production-ready API.

**Tasks:**

**Morning — Docker & Deployment:**
1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```
2. Create `docker-compose.yml`:
   - `api` service (FastAPI)
   - `db` service (PostgreSQL)
   - `redis` service (optional)
   - Environment variables via `.env`
3. Test locally: `docker-compose up --build`
4. Deploy to Railway / Render / Fly.io:
   - Connect GitHub repo
   - Set environment variables
   - Run migrations on deploy: `alembic upgrade head`

**Afternoon — Documentation:**
5. Enhance OpenAPI docs in `main.py`:
   - Custom title, description, version
   - Tag descriptions for each router
   - Example request/response bodies in schemas
6. Write comprehensive `README.md`:
   - Project overview + architecture diagram
   - Tech stack table
   - Setup instructions (local + Docker)
   - Environment variables table
   - API endpoints overview with examples
   - Running tests section
   - Deployment link

**Final Push:**
7. Final commit: `Day 15: Docker deployment, OpenAPI documentation, README, production-ready API`
8. Tag release: `git tag v1.0.0`
9. Ensure all GitHub commits are meaningful (15 meaningful commits minimum)

**Deliverables:**
- Live deployed API URL
- Swagger UI accessible at `/docs`
- ReDoc at `/redoc`
- Complete README
- Docker image builds successfully
- All 15 days committed to GitHub

---

## 🌟 Advanced / Bonus Features (Add Throughout)

| Feature | Where to Add |
|---|---|
| Portfolio snapshot history (daily values) | Day 7 |
| Email notifications (SendGrid/Mailgun) | Day 10 |
| Two-factor auth (TOTP) | Day 13 |
| WebSocket real-time price feed | Day 8 |
| AI portfolio insights (OpenAI API) | Day 11 |
| Redis caching for market data | Day 8 |
| Celery for heavy async tasks | Day 10 |
| S3 file storage for CSV uploads | Day 12 |

---

## 🚀 Daily GitHub Commit Convention

```
Day 1: Project setup, FastAPI boilerplate, REST foundations
Day 2: PostgreSQL async setup, User model, Alembic migration
Day 3: JWT auth, user registration, password hashing, profile endpoints
Day 4: Portfolio CRUD, ownership authorization, one-to-many relationships
Day 5: Stock catalog, search/filter/pagination, admin-only endpoints
Day 6: BUY/SELL transactions, holding updates, weighted avg price logic
Day 7: Holdings API, portfolio performance, P&L calculation
Day 8: External market data integration, price caching, live P&L
Day 9: Watchlist with target prices, background price monitoring
Day 10: In-app notifications, APScheduler price monitoring, alert system
Day 11: Advanced search, filtering, sorting, pagination across all endpoints
Day 12: CSV transaction import, file validation, bulk upload
Day 13: Admin panel, RBAC, rate limiting, security hardening
Day 14: Comprehensive test suite, permission isolation tests, 80%+ coverage
Day 15: Docker deployment, OpenAPI documentation, README, production-ready
```

---

## 📊 Internship Completion Checklist

- [ ] ≥12 of 15 days submitted
- [ ] ≤3 missed submissions
- [ ] Ownership/authorization checks implemented and tested
- [ ] API deployed (live URL accessible)
- [ ] Alembic migrations committed
- [ ] Pytest tests written and passing
- [ ] OpenAPI/Swagger documentation complete
- [ ] README with setup instructions
- [ ] Minimum 4 related database models (7 implemented)
- [ ] Live technical review on Day 15 passed
