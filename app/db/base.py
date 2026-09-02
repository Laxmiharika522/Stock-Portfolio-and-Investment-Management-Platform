"""
Base Model Declarative Setup & Mixins — Day 2
SQLAlchemy 2.x DeclarativeBase and standard TimestampMixin.
"""

from datetime import datetime, timezone
from typing import Any
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all database models.
    Provides standard __repr__ for clean model debugging.
    """

    def __repr__(self) -> str:
        columns = [
            f"{col.name}={getattr(self, col.name)!r}"
            for col in self.__table__.columns
        ]
        return f"<{self.__class__.__name__}({', '.join(columns)})>"

    def to_dict(self) -> dict[str, Any]:
        """Convert model instance attributes to dictionary."""
        return {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns
        }


class TimestampMixin:
    """
    Mixin providing created_at and updated_at datetime fields.
    Defaults to UTC server timestamp on insert/update.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        doc="Timestamp when record was created",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        onupdate=func.now(),
        nullable=False,
        doc="Timestamp when record was last updated",
    )
