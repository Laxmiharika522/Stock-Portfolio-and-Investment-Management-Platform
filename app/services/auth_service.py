"""
Auth Service — Day 3
Business logic for User Registration, Authentication, JWT Token issuance, and Profile Updates.
"""

import uuid
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException, NotFoundException, UnauthorizedException, BadRequestException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut, UserUpdate, PasswordChange, Token


class AuthService:
    """Service layer handling user authentication and registration workflows."""

    @staticmethod
    async def register_user(db: AsyncSession, user_in: UserCreate) -> User:
        """Register a new user account after checking email/username uniqueness."""
        stmt = select(User).where(
            or_(User.email == user_in.email.lower(), User.username == user_in.username.lower())
        )
        existing = await db.execute(stmt)
        if existing.scalar_one_or_none():
            raise ConflictException("A user with this email or username already exists")

        new_user = User(
            email=user_in.email.lower(),
            username=user_in.username.lower(),
            hashed_password=hash_password(user_in.password),
            full_name=user_in.full_name,
            is_active=True,
            is_admin=False,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def authenticate_user(db: AsyncSession, credentials: UserLogin) -> Token:
        """Authenticate user credentials and return access + refresh tokens."""
        identifier = credentials.username_or_email.lower().strip()
        stmt = select(User).where(
            or_(User.email == identifier, User.username == identifier)
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not verify_password(credentials.password, user.hashed_password):
            raise UnauthorizedException("Invalid username/email or password")

        if not user.is_active:
            raise UnauthorizedException("User account is inactive")

        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=1800,
            user=UserOut.model_validate(user),
        )

    @staticmethod
    async def refresh_access_token(db: AsyncSession, refresh_token: str) -> dict[str, str]:
        """Issue a new access token using a valid refresh token."""
        payload = decode_token(refresh_token, expected_type="refresh")
        user_id_str = payload.get("sub")
        try:
            user_id = uuid.UUID(user_id_str)
        except (ValueError, TypeError):
            raise UnauthorizedException("Invalid user ID in token")

        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not user.is_active:
            raise UnauthorizedException("User account not found or inactive")

        new_access_token = create_access_token(subject=str(user.id))
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": "1800",
        }

    @staticmethod
    async def change_password(db: AsyncSession, user: User, pwd_in: PasswordChange) -> None:
        """Change logged-in user password after verifying current password."""
        if not verify_password(pwd_in.current_password, user.hashed_password):
            raise BadRequestException("Current password verification failed")

        user.hashed_password = hash_password(pwd_in.new_password)
        await db.commit()

    @staticmethod
    async def update_profile(db: AsyncSession, user: User, update_in: UserUpdate) -> User:
        """Update user profile details."""
        if update_in.email and update_in.email.lower() != user.email:
            stmt = select(User).where(User.email == update_in.email.lower())
            res = await db.execute(stmt)
            if res.scalar_one_or_none():
                raise ConflictException("Email address is already in use by another account")
            user.email = update_in.email.lower()

        if update_in.username and update_in.username.lower() != user.username:
            stmt = select(User).where(User.username == update_in.username.lower())
            res = await db.execute(stmt)
            if res.scalar_one_or_none():
                raise ConflictException("Username is already taken")
            user.username = update_in.username.lower()

        if update_in.full_name is not None:
            user.full_name = update_in.full_name

        await db.commit()
        await db.refresh(user)
        return user
