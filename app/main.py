"""
FastAPI Application Entry Point
Stock Portfolio & Investment Management Platform
Day 1: Core setup, middleware, exception handlers, and routing.
"""

from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.custom_docs import get_custom_swagger_ui_html
from app.api.v1.health import router as health_router

# ── Logging Configuration ─────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── Lifespan (startup / shutdown events) ─────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    Code before `yield` runs on startup.
    Code after `yield` runs on shutdown.
    """
    logger.info("🚀 Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)
    logger.info("📦 Environment : %s", settings.ENVIRONMENT)
    display_host = "localhost" if settings.HOST == "0.0.0.0" else settings.HOST
    logger.info("🌐 Server      : http://%s:%s", display_host, settings.PORT)
    logger.info("📚 Swagger UI  : http://%s:%s/docs", display_host, settings.PORT)
    logger.info("📖 ReDoc       : http://%s:%s/redoc", display_host, settings.PORT)

    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from app.tasks.price_monitor import check_watchlist_prices
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_watchlist_prices, 'interval', minutes=5)
    scheduler.start()
    logger.info("⏰ APScheduler started for price monitoring (5m interval).")

    yield  # ← Application is running

    logger.info("🛑 Shutting down %s", settings.APP_NAME)
    scheduler.shutdown()


# ── FastAPI Application ───────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url=None,  # Custom Swagger UI route registered below
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "Health",
            "description": "API health check and status endpoints.",
        },
        {
            "name": "Authentication",
            "description": "User registration, login, JWT token management.",
        },
        {
            "name": "Users",
            "description": "User profile management.",
        },
        {
            "name": "Portfolios",
            "description": "Create and manage investment portfolios.",
        },
        {
            "name": "Stocks",
            "description": "Stock catalog — search, filter, and view stock information.",
        },
        {
            "name": "Transactions",
            "description": "Record and view BUY/SELL transactions.",
        },
        {
            "name": "Holdings",
            "description": "View current holdings and portfolio performance.",
        },
        {
            "name": "Market Data",
            "description": "Live stock prices and historical market data.",
        },
        {
            "name": "Watchlist",
            "description": "Monitor stocks and set target price alerts.",
        },
        {
            "name": "Notifications",
            "description": "In-app notification management.",
        },
        {
            "name": "Upload",
            "description": "CSV transaction import.",
        },
        {
            "name": "Admin",
            "description": "Administrator-only operations (requires admin role).",
        },
    ],
)


# ── Middleware ────────────────────────────────────────────────────────────────

# 1. CORS — allow configured origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# 2. Request Timing Middleware — adds X-Process-Time header to every response
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000  # in ms
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    return response


# 3. Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("→ %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info(
        "← %s %s [%s]",
        request.method,
        request.url.path,
        response.status_code,
    )
    return response


# 4. Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if settings.is_production:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


# ── Exception Handlers ────────────────────────────────────────────────────────
register_exception_handlers(app)


# ── Custom Documentation Routes ──────────────────────────────────────────────
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_custom_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{settings.APP_NAME} - Interactive Docs",
    )


# ── Routers ───────────────────────────────────────────────────────────────────
# Day 1: Health check
app.include_router(health_router)

# Day 3: Auth & Users
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

# Day 4: Portfolios
from app.api.v1.portfolios import router as portfolios_router
app.include_router(portfolios_router, prefix="/api/v1")

# Day 5: Stocks
from app.api.v1.stocks import router as stocks_router
app.include_router(stocks_router, prefix="/api/v1")

# Day 6: Transactions (BUY/SELL)
from app.api.v1.transactions import router as transactions_router
app.include_router(transactions_router, prefix="/api/v1")


# Day 7+: Holdings
# from app.api.v1.holdings import router as holdings_router
# app.include_router(holdings_router, prefix="/api/v1")

# Day 8+: Market Data
from app.api.v1.market import router as market_router
app.include_router(market_router, prefix="/api/v1")

# Day 9+: Watchlist
from app.api.v1.watchlist import router as watchlist_router
app.include_router(watchlist_router, prefix="/api/v1")

# Day 10+: Notifications
from app.api.v1.notifications import router as notifications_router
app.include_router(notifications_router, prefix="/api/v1")

# Day 12+: Upload
# from app.api.v1.upload import router as upload_router
# app.include_router(upload_router, prefix="/api/v1")

# Day 13+: Admin
# from app.api.v1.admin import router as admin_router
# app.include_router(admin_router, prefix="/api/v1")
