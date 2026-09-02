"""
Database Session Configuration — Async SQLAlchemy 2.0
Provides async engine, session factory, dependency injection, and health checks.
"""

from typing import AsyncGenerator
import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

logger = logging.getLogger(__name__)

# ── Async Database Engine ──────────────────────────────────────────────────────
# Creates an async connection pool targeting PostgreSQL (via asyncpg)
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True,
    pool_pre_ping=True,      # Automatically verify connection health before checkout
    pool_size=10,             # Default pool size for concurrent connections
    max_overflow=20,          # Extra connections allowed during spikes
)

# ── Async Session Factory ─────────────────────────────────────────────────────
# Session generator for all DB operations
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent attributes from expiring after commit in async mode
    autoflush=False,
)


# ── Dependency Injection for FastAPI Endpoints ────────────────────────────────
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency yielding an async SQLAlchemy session per request.
    Handles commit on success, rollback on exception, and automatic closure.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ── Health / Utility Check ────────────────────────────────────────────────────
async def check_db_connection() -> bool:
    """
    Verifies database connectivity by executing a lightweight query.
    Returns True if connection succeeds, False otherwise.
    """
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception as exc:
        logger.error("Database connection check failed: %s", exc)
        return False
