"""
Transaction Pydantic Schemas — Day 6
Validation and serialization for BUY/SELL trade request/response payloads,
deposit requests, and paginated transaction history responses.
"""

from __future__ import annotations

import math
import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.transaction import TransactionType


# ── Request Schemas ───────────────────────────────────────────────────────────

class TransactionCreate(BaseModel):
    """
    Request body for executing a BUY or SELL trade.
    The price_per_share is client-supplied (Day 8 will inject live prices).
    """

    stock_symbol: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Ticker symbol of the stock to trade (case-insensitive)",
        json_schema_extra={"example": "AAPL"},
    )
    transaction_type: TransactionType = Field(
        ...,
        description="Trade direction: BUY or SELL",
        json_schema_extra={"example": "BUY"},
    )
    quantity: float = Field(
        ...,
        gt=0,
        description="Number of shares to trade (must be > 0, fractional allowed)",
        json_schema_extra={"example": 10.0},
    )
    price_per_share: float = Field(
        ...,
        gt=0,
        description="Price per share at time of trade (USD or portfolio currency)",
        json_schema_extra={"example": 182.50},
    )
    fees: float = Field(
        default=0.0,
        ge=0,
        description="Brokerage commission or fees for this trade",
        json_schema_extra={"example": 1.99},
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional trade notes or rationale",
        json_schema_extra={"example": "Buying on dip after earnings"},
    )
    transacted_at: Optional[datetime] = Field(
        default=None,
        description="Trade timestamp (defaults to now; can be backdated)",
        json_schema_extra={"example": "2026-09-08T10:30:00Z"},
    )

    @field_validator("quantity")
    @classmethod
    def quantity_min_precision(cls, v: float) -> float:
        if v < 0.0001:
            raise ValueError("Quantity must be at least 0.0001 shares")
        return round(v, 4)

    @field_validator("price_per_share")
    @classmethod
    def price_must_be_finite(cls, v: float) -> float:
        if not math.isfinite(v):
            raise ValueError("price_per_share must be a finite number")
        return round(v, 6)

    @field_validator("stock_symbol")
    @classmethod
    def uppercase_symbol(cls, v: str) -> str:
        return v.strip().upper()


class DepositRequest(BaseModel):
    """Request body to fund a portfolio's cash balance."""

    amount: float = Field(
        ...,
        gt=0,
        description="Amount of cash to deposit into the portfolio",
        json_schema_extra={"example": 50000.00},
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional deposit note (e.g., 'Initial funding')",
        json_schema_extra={"example": "Initial capital deposit"},
    )

    @field_validator("amount")
    @classmethod
    def amount_max_cap(cls, v: float) -> float:
        if v > 1_000_000_000:
            raise ValueError("Single deposit cannot exceed 1,000,000,000")
        return round(v, 2)


# ── Response Schemas ──────────────────────────────────────────────────────────

class StockSummary(BaseModel):
    """Minimal stock information embedded in transaction responses."""
    id: uuid.UUID
    symbol: str
    company_name: str
    sector: str
    exchange: str
    currency: str

    model_config = ConfigDict(from_attributes=True)


class TransactionOut(BaseModel):
    """
    Full transaction response object returned after BUY/SELL execution or history lookup.
    """

    id: uuid.UUID
    portfolio_id: uuid.UUID
    stock_id: uuid.UUID
    transaction_type: TransactionType
    quantity: float
    price_per_share: float
    fees: float
    total_amount: float
    notes: Optional[str]
    transacted_at: datetime
    created_at: datetime
    updated_at: datetime

    # Embedded related data
    stock: StockSummary

    model_config = ConfigDict(from_attributes=True)


class PortfolioBalanceUpdate(BaseModel):
    """Snapshot of portfolio balances returned after a trade or deposit."""
    portfolio_id: uuid.UUID
    cash_balance: float
    total_invested: float
    currency: str

    model_config = ConfigDict(from_attributes=True)


class TransactionResponse(BaseModel):
    """Wrapper returned from execute-trade endpoint combining tx + updated balance."""
    transaction: TransactionOut
    portfolio_balance: PortfolioBalanceUpdate


class DepositResponse(BaseModel):
    """Response after a successful cash deposit."""
    message: str
    amount_deposited: float
    portfolio_balance: PortfolioBalanceUpdate


class PaginatedTransactionResponse(BaseModel):
    """Paginated list of transaction history."""
    items: List[TransactionOut]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(
        cls,
        items: List[TransactionOut],
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedTransactionResponse":
        total_pages = math.ceil(total / page_size) if page_size > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
        )
