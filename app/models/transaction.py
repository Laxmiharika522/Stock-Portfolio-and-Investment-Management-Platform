"""
Transaction Database Model — Day 6
Records each BUY or SELL stock trade executed within a portfolio.
Stores price, quantity, fees, and a computed total_amount for historical accuracy.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.portfolio import Portfolio
    from app.models.stock import Stock


class TransactionType(str, enum.Enum):
    """Enumeration of valid transaction directions."""
    BUY = "BUY"
    SELL = "SELL"


class Transaction(Base, TimestampMixin):
    """
    Transaction entity recording each individual BUY or SELL trade.
    Total amount = (quantity × price_per_share) ± fees.
    """

    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        doc="Unique transaction identifier (UUID v4)",
    )

    portfolio_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Portfolio this trade belongs to",
    )

    stock_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("stocks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Stock being bought or sold",
    )

    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, name="transactiontype"),
        nullable=False,
        index=True,
        doc="Direction of trade: BUY or SELL",
    )

    quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        doc="Number of shares traded (fractional shares allowed, min 0.0001)",
    )

    price_per_share: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        doc="Price per share at the time of trade (client-supplied until Day 8 live feed)",
    )

    fees: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
        doc="Brokerage fees / commissions for this trade",
    )

    total_amount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        doc="Net trade value: (quantity × price_per_share) + fees for BUY, minus fees for SELL",
    )

    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Optional user notes or trade rationale",
    )

    transacted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
        doc="Timestamp of the trade (can be backdated by the client)",
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    portfolio: Mapped["Portfolio"] = relationship(
        "Portfolio",
        back_populates="transactions",
    )
    stock: Mapped["Stock"] = relationship(
        "Stock",
        lazy="joined",  # Always eager-load stock info for responses
    )
