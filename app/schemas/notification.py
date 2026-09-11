"""
Notification Pydantic Schemas — Day 10
Input validation and serialization schemas for Notification endpoints.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, Field

from app.models.notification import NotificationType

class NotificationCreate(BaseModel):
    """Schema for creating a new notification internally (not usually via API)."""
    type: NotificationType
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1, max_length=1000)
    related_stock_id: Optional[UUID] = None
    metadata_dict: Optional[dict[str, Any]] = None

class NotificationUpdate(BaseModel):
    """Schema for updating a notification (e.g. marking as read)."""
    is_read: Optional[bool] = None

class NotificationOut(BaseModel):
    """Schema for returning detailed notification information in API responses."""
    id: UUID
    user_id: UUID
    type: NotificationType
    title: str
    message: str
    is_read: bool
    related_stock_id: Optional[UUID]
    metadata_dict: Optional[dict[str, Any]]
    read_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NotificationCountOut(BaseModel):
    """Schema for returning unread notification count."""
    unread_count: int
