"""
Watchlist Pydantic Schemas — Day 9
Input validation and serialization schemas for Watchlist endpoints.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

from app.models.watchlist import AlertType

class WatchlistBase(BaseModel):
    """Base schema holding common watchlist attributes."""
    
    target_price: Optional[Decimal] = Field(None, ge=0, example=150.0, description="Optional target price to trigger an alert")
    alert_type: Optional[AlertType] = Field(None, description="Type of alert (ABOVE or BELOW target price)")
    notes: Optional[str] = Field(None, max_length=500, example="Buy if it drops below this price.", description="Optional personal notes")


class WatchlistCreate(WatchlistBase):
    """Schema for adding a stock to the watchlist."""
    
    stock_symbol: str = Field(..., min_length=1, max_length=20, example="AAPL", description="Stock ticker symbol to add")


class WatchlistUpdate(BaseModel):
    """Schema for updating an existing watchlist item."""
    
    target_price: Optional[Decimal] = Field(None, ge=0, example=160.0)
    alert_type: Optional[AlertType] = None
    notes: Optional[str] = Field(None, max_length=500)


class WatchlistOut(WatchlistBase):
    """Schema for returning detailed watchlist information in API responses."""

    id: UUID
    user_id: UUID
    stock_id: UUID
    is_triggered: bool
    triggered_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
