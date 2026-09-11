"""
Watchlist Database Model — Day 9
Represents the many-to-many relationship between users and stocks for target price monitoring.
"""

import uuid
from datetime import datetime
from typing import Optional
from decimal import Decimal
import enum
from sqlalchemy import String, ForeignKey, Numeric, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin

class AlertType(str, enum.Enum):
    ABOVE = "ABOVE"
    BELOW = "BELOW"

class Watchlist(Base, TimestampMixin):
    """
    Watchlist entity table associating a user to a stock with optional target price alerts.
    """

    __tablename__ = "watchlists"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        doc="Unique watchlist item identifier (UUID v4)",
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Foreign key to the User who owns this watchlist item",
    )

    stock_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("stocks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Foreign key to the Stock being watched",
    )

    target_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(precision=15, scale=4),
        nullable=True,
        doc="Optional target price to trigger an alert",
    )

    alert_type: Mapped[Optional[AlertType]] = mapped_column(
        Enum(AlertType, name="alert_type_enum", native_enum=False),
        nullable=True,
        doc="Type of alert (ABOVE or BELOW target price)",
    )

    notes: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="Optional personal notes about why this stock is on the watchlist",
    )

    is_triggered: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Whether the alert target price has been hit",
    )

    triggered_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="When the alert was triggered",
    )
