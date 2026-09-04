"""
Pytest configuration and shared fixtures — Day 2 to Day 4
Configures async test database, httpx AsyncClient, and auth token fixtures for FastAPI test runs.
"""

import os
import uuid
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# Set test database environment variable before importing app modules
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_stock_portfolio.db"

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models.user import User
from app.core.security import hash_password, create_access_token

# Test Async Engine
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_stock_portfolio.db"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    """Create all database tables before tests and drop them after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()
    try:
        if os.path.exists("./test_stock_portfolio.db"):
            os.remove("./test_stock_portfolio.db")
    except PermissionError:
        pass


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a fresh AsyncSession for direct DB testing within a transaction rollback."""
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Provides an AsyncClient for testing FastAPI endpoints with overridden DB dependency."""
    async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = _override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user_a(db_session: AsyncSession) -> User:
    """Fixture providing user A."""
    user = User(
        email=f"usera_{uuid.uuid4().hex[:6]}@example.com",
        username=f"usera_{uuid.uuid4().hex[:6]}",
        hashed_password=hash_password("Password123!"),
        full_name="User A",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def user_b(db_session: AsyncSession) -> User:
    """Fixture providing user B."""
    user = User(
        email=f"userb_{uuid.uuid4().hex[:6]}@example.com",
        username=f"userb_{uuid.uuid4().hex[:6]}",
        hashed_password=hash_password("Password123!"),
        full_name="User B",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def token_user_a(user_a: User) -> str:
    """Generate access token for user A."""
    return create_access_token(subject=str(user_a.id))


@pytest.fixture
def token_user_b(user_b: User) -> str:
    """Generate access token for user B."""
    return create_access_token(subject=str(user_b.id))
