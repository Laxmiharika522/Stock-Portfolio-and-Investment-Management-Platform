"""
Notification Service Layer — Day 10
Contains business logic for managing notifications.
"""

import uuid
from typing import Sequence, Optional, Any
from datetime import datetime, timezone
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification, NotificationType
from app.core.exceptions import ForbiddenException, NotFoundException


class NotificationService:

    @staticmethod
    async def create_notification(
        db: AsyncSession,
        user_id: uuid.UUID,
        type: NotificationType,
        title: str,
        message: str,
        related_stock_id: Optional[uuid.UUID] = None,
        metadata_dict: Optional[dict[str, Any]] = None,
    ) -> Notification:
        """Create a new notification for a user."""
        notification = Notification(
            user_id=user_id,
            type=type,
            title=title,
            message=message,
            related_stock_id=related_stock_id,
            metadata_dict=metadata_dict,
        )
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        return notification

    @staticmethod
    async def get_user_notifications(
        db: AsyncSession,
        user_id: uuid.UUID,
        is_read: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Notification]:
        """Fetch notifications belonging to a specific user, with optional read status filter."""
        stmt = select(Notification).where(Notification.user_id == user_id)
        
        if is_read is not None:
            stmt = stmt.where(Notification.is_read == is_read)
            
        stmt = stmt.order_by(Notification.created_at.desc()).offset(skip).limit(limit)
        
        result = await db.execute(stmt)
        return result.scalars().all()
        
    @staticmethod
    async def get_unread_count(
        db: AsyncSession,
        user_id: uuid.UUID,
    ) -> int:
        """Get the count of unread notifications for a user."""
        from sqlalchemy import func
        stmt = select(func.count(Notification.id)).where(
            Notification.user_id == user_id,
            Notification.is_read == False
        )
        result = await db.execute(stmt)
        return result.scalar() or 0

    @staticmethod
    async def get_notification_by_id(
        db: AsyncSession,
        notification_id: uuid.UUID,
        user_id: Optional[uuid.UUID] = None,
        is_admin: bool = False,
    ) -> Notification:
        """Fetch a single notification by ID."""
        stmt = select(Notification).where(Notification.id == notification_id)
        result = await db.execute(stmt)
        notification = result.scalar_one_or_none()

        if not notification:
            raise NotFoundException(detail="Notification not found")

        if user_id and not is_admin and notification.user_id != user_id:
            raise ForbiddenException(detail="Access denied: You do not own this notification")

        return notification

    @staticmethod
    async def mark_as_read(
        db: AsyncSession,
        notification_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Notification:
        """Mark a notification as read."""
        notification = await NotificationService.get_notification_by_id(db, notification_id, user_id)
        
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = datetime.now(timezone.utc)
            await db.commit()
            await db.refresh(notification)
            
        return notification
        
    @staticmethod
    async def mark_all_as_read(
        db: AsyncSession,
        user_id: uuid.UUID,
    ) -> int:
        """Mark all unread notifications as read for a user."""
        stmt = (
            update(Notification)
            .where(Notification.user_id == user_id, Notification.is_read == False)
            .values(is_read=True, read_at=datetime.now(timezone.utc))
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount

    @staticmethod
    async def delete_notification(
        db: AsyncSession,
        notification_id: uuid.UUID,
        user_id: uuid.UUID,
        is_admin: bool = False,
    ) -> bool:
        """Delete a notification after verifying user ownership."""
        notification = await NotificationService.get_notification_by_id(db, notification_id, user_id, is_admin=is_admin)
        await db.delete(notification)
        await db.commit()
        return True
