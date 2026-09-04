"""
Portfolio Database Model — Day 4
Represents investment portfolios owned by users.
"""

import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Portfolio(Base, TimestampMixin):
    """
    Portfolio entity storing user investment accounts, currency, and settings.
    """

    __tablename__ = "portfolios"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        doc="Unique portfolio identifier (UUID v4)",
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Owner user identifier",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Portfolio display name (e.g., Tech Stocks, Retirement)",
    )

    description: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional description of portfolio strategy",
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="USD",
        nullable=False,
        doc="Base currency code (e.g. USD, EUR, INR)",
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Whether this is the user's primary default portfolio",
    )

    # Relationships
    user: Mapped["User"] = relationship("User", backref="portfolios")
