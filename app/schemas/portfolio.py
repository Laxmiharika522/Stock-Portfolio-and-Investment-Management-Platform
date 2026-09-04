"""
Portfolio Pydantic Schemas — Day 4
Data validation and serialization for Portfolio request/response objects.
"""

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class PortfolioBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, json_schema_extra={"example": "Growth Tech Portfolio"})
    description: Optional[str] = Field(None, max_length=255, json_schema_extra={"example": "Long-term high growth stocks"})
    currency: str = Field("USD", min_length=3, max_length=10, json_schema_extra={"example": "USD"})
    is_default: bool = Field(False, json_schema_extra={"example": False})


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, json_schema_extra={"example": "Updated Portfolio Name"})
    description: Optional[str] = Field(None, max_length=255)
    currency: Optional[str] = Field(None, min_length=3, max_length=10)
    is_default: Optional[bool] = None


class PortfolioOut(PortfolioBase):
    id: uuid.UUID
    user_id: uuid.UUID
    total_value: float = Field(0.0, description="Calculated total portfolio value", json_schema_extra={"example": 12500.50})
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
