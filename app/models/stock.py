"""
Stock Database Model — Day 5
Represents tradable assets / stocks in the Stock Portfolio platform catalog.
"""

from __future__ import annotations

import uuid
from typing import Optional
from sqlalchemy import Boolean, Float, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Stock(Base, TimestampMixin):
    """
    Stock entity table storing company ticker symbols, sector details, and market metadata.
    """

    __tablename__ = "stocks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        doc="Unique stock identifier (UUID v4)",
    )

    symbol: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
        doc="Unique stock ticker symbol (e.g., AAPL, GOOGL, MSFT)",
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
        doc="Full corporate company name",
    )

    sector: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
        doc="Industry sector (e.g., Technology, Healthcare, Finance)",
    )

    industry: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Specific industry subcategory",
    )

    exchange: Mapped[str] = mapped_column(
        String(50),
        index=True,
        nullable=False,
        doc="Stock exchange market (e.g., NASDAQ, NYSE)",
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="USD",
        nullable=False,
        doc="Trading currency code (e.g., USD, EUR)",
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Brief summary description of the company business",
    )

    logo_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="URL to company logo image asset",
    )

    market_cap: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        doc="Market capitalization value in USD",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        doc="Whether stock trading status is active in catalog",
    )
