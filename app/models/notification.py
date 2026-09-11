"""
Notification Database Model — Day 10
Represents in-app notifications for users, such as price alerts and trade confirmations.
"""

import uuid
from datetime import datetime
import enum
from typing import Optional, Any
from sqlalchemy import String, ForeignKey, Boolean, DateTime, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin

class NotificationType(str, enum.Enum):
    PRICE_ALERT = "PRICE_ALERT"
    TRADE_CONFIRM = "TRADE_CONFIRM"
    SYSTEM = "SYSTEM"

class Notification(Base, TimestampMixin):
    """
    Notification entity table representing user alerts and messages.
    """

    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        doc="Unique notification identifier (UUID v4)",
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Foreign key to the User receiving the notification",
    )

    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType, name="notification_type_enum", native_enum=False),
        nullable=False,
        doc="Type of notification",
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Short title of the notification",
    )

    message: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
        doc="Full message content",
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Whether the notification has been read by the user",
    )

    related_stock_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("stocks.id", ondelete="SET NULL"),
        nullable=True,
        doc="Optional foreign key to a related Stock",
    )

    metadata_dict: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
        doc="Optional JSON metadata payload for extra context",
    )

    read_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="When the notification was marked as read",
    )
