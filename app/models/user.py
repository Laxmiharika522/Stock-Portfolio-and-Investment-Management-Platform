"""
User Database Model — Day 2
Represents users, credentials, roles, and status in the Stock Portfolio platform.
"""

import uuid
from typing import Optional
from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """
    User entity table holding identity, authorization roles, and account status.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        doc="Unique user identifier (UUID v4)",
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        doc="Unique user email address",
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        doc="Unique username handle",
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Bcrypt hashed password",
    )

    full_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Optional full name display string",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        doc="Whether the user account is active",
    )

    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Whether the user has administrator privileges (RBAC)",
    )
