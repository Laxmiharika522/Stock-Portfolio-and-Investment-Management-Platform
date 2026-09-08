"""
Portfolio Database Model — Day 4 / Day 6
Represents investment portfolios owned by users.
Day 6 adds: cash_balance, total_invested, and transactions relationship.
"""

import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.transaction import Transaction


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

    cash_balance: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
        doc="Available cash balance for trading (virtual wallet in portfolio currency)",
    )

    total_invested: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
        doc="Cumulative cost basis of all BUY trades (excludes fees)",
    )

    # Relationships
    user: Mapped["User"] = relationship("User", backref="portfolios")
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        lazy="select",
    )
