"""
Tests for Day 2 — PostgreSQL, Async SQLAlchemy & User Model
"""

import uuid
import pytest
from sqlalchemy import select
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.db.session import check_db_connection


@pytest.mark.asyncio
async def test_user_model_creation(db_session: AsyncSession):
    """Verify creating a User model in the database and checking attributes."""
    user = User(
        email="john.doe@example.com",
        username="johndoe",
        hashed_password="securehashedpassword123",
        full_name="John Doe",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    assert isinstance(user.id, uuid.UUID)
    assert user.email == "john.doe@example.com"
    assert user.username == "johndoe"
    assert user.full_name == "John Doe"
    assert user.is_active is True
    assert user.is_admin is False
    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.asyncio
async def test_user_model_query_by_username(db_session: AsyncSession):
    """Verify querying a User by username using SQLAlchemy select."""
    user = User(
        email="jane.doe@example.com",
        username="janedoe",
        hashed_password="anotherhashedpassword456",
        full_name="Jane Doe",
        is_admin=True,
    )
    db_session.add(user)
    await db_session.commit()

    stmt = select(User).where(User.username == "janedoe")
    result = await db_session.execute(stmt)
    fetched_user = result.scalar_one_or_none()

    assert fetched_user is not None
    assert fetched_user.email == "jane.doe@example.com"
    assert fetched_user.is_admin is True


@pytest.mark.asyncio
async def test_check_db_connection():
    """Verify database connection health check function."""
    is_alive = await check_db_connection()
    assert is_alive is True


@pytest.mark.asyncio
async def test_health_endpoint_db_status(async_client: AsyncClient):
    """Verify GET /health returns database: connected status."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
