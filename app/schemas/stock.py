"""
Stock Pydantic Schemas — Day 5
Input validation and serialization schemas for Stock endpoints and pagination responses.
"""

from __future__ import annotations

import math
from datetime import datetime
from uuid import UUID
from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel, Field, ConfigDict, field_validator

T = TypeVar("T")


class StockBase(BaseModel):
    """Base schema holding common stock attributes."""

    symbol: str = Field(..., min_length=1, max_length=20, example="AAPL", description="Stock ticker symbol")
    company_name: str = Field(..., min_length=1, max_length=255, example="Apple Inc.", description="Company full name")
    sector: str = Field(..., min_length=1, max_length=100, example="Technology", description="Industry sector")
    industry: Optional[str] = Field(None, max_length=100, example="Consumer Electronics", description="Industry subcategory")
    exchange: str = Field(..., min_length=1, max_length=50, example="NASDAQ", description="Exchange market")
    currency: str = Field("USD", min_length=1, max_length=10, example="USD", description="Currency code")
    description: Optional[str] = Field(None, example="Apple designs and manufactures mobile devices and computers.", description="Company summary")
    logo_url: Optional[str] = Field(None, max_length=500, example="https://logo.clearbit.com/apple.com", description="Company logo URL")
    market_cap: Optional[float] = Field(None, ge=0, example=3000000000000.0, description="Market capitalization USD")
    is_active: bool = Field(True, description="Active status in stock catalog")

    @field_validator("symbol")
    @classmethod
    def uppercase_symbol(cls, v: str) -> str:
        return v.strip().upper()


class StockCreate(StockBase):
    """Schema for creating a new stock (Admin only)."""
    pass


class StockUpdate(BaseModel):
    """Schema for updating an existing stock (Admin only)."""

    company_name: Optional[str] = Field(None, min_length=1, max_length=255)
    sector: Optional[str] = Field(None, min_length=1, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    exchange: Optional[str] = Field(None, min_length=1, max_length=50)
    currency: Optional[str] = Field(None, min_length=1, max_length=10)
    description: Optional[str] = None
    logo_url: Optional[str] = None
    market_cap: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None


class StockOut(StockBase):
    """Schema for returning detailed stock information in API responses."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedStockResponse(BaseModel):
    """Paginated wrapper response schema for stock listings."""

    items: List[StockOut]
    total: int = Field(..., example=20, description="Total matching items count")
    page: int = Field(..., example=1, description="Current page number (1-indexed)")
    page_size: int = Field(..., example=10, description="Number of items per page")
    total_pages: int = Field(..., example=2, description="Total available pages count")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def create(cls, items: List[StockOut], total: int, page: int, page_size: int) -> PaginatedStockResponse:
        total_pages = math.ceil(total / page_size) if page_size > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
