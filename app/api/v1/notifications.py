"""
Notifications API Router — Day 10
Endpoints for managing user notifications.
"""

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.schemas.notification import NotificationOut, NotificationCountOut
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=List[NotificationOut])
async def list_notifications(
    is_read: Optional[bool] = Query(None, description="Filter by read status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all notifications for the authenticated user."""
    return await NotificationService.get_user_notifications(
        db, user_id=current_user.id, is_read=is_read, skip=skip, limit=limit
    )

@router.get("/unread-count", response_model=NotificationCountOut)
async def get_unread_count(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get the count of unread notifications for the user."""
    count = await NotificationService.get_unread_count(db, current_user.id)
    return NotificationCountOut(unread_count=count)

@router.put("/read-all", status_code=status.HTTP_200_OK)
async def mark_all_read(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Mark all unread notifications as read."""
    updated_count = await NotificationService.mark_all_as_read(db, current_user.id)
    return {"message": f"Successfully marked {updated_count} notifications as read"}

@router.put("/{notification_id}/read", response_model=NotificationOut)
async def mark_read(
    notification_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Mark a specific notification as read."""
    return await NotificationService.mark_as_read(db, notification_id, current_user.id)

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a specific notification."""
    await NotificationService.delete_notification(db, notification_id, current_user.id)
    return None
