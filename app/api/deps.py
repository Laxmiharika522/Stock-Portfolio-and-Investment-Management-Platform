"""
FastAPI Dependencies — Day 3
Provides reusable dependency injection functions for authentication and database sessions.
"""

import uuid
from typing import AsyncGenerator
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AdminRequiredException, UnauthorizedException
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User

# OAuth2 scheme extracting Bearer token from HTTP Authorization header
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user(
    token: str = Depends(reusable_oauth2),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Extract and validate the current authenticated user from Bearer JWT access token."""
    if not token:
        raise UnauthorizedException("Authentication token is missing")

    payload = decode_token(token, expected_type="access")
    user_id_str: str = payload.get("sub", "")
    try:
        user_id = uuid.UUID(user_id_str)
    except (ValueError, TypeError):
        raise UnauthorizedException("Invalid user ID in token payload")

    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise UnauthorizedException("User associated with token no longer exists")

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Verify that current user account is active."""
    if not current_user.is_active:
        raise UnauthorizedException("User account is inactive")
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Verify that current user has admin privileges (RBAC)."""
    if not current_user.is_admin:
        raise AdminRequiredException()
    return current_user
