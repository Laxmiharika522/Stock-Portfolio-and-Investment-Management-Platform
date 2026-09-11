"""
Watchlist Service Layer — Day 9
Contains business logic for managing the watchlist.
"""

import uuid
from typing import Sequence, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.watchlist import Watchlist
from app.models.stock import Stock
from app.schemas.watchlist import WatchlistCreate, WatchlistUpdate
from app.core.exceptions import ForbiddenException, NotFoundException


class WatchlistService:

    @staticmethod
    async def add_to_watchlist(
        db: AsyncSession,
        user_id: uuid.UUID,
        watchlist_in: WatchlistCreate,
    ) -> Watchlist:
        """Add a stock to the user's watchlist."""
        # Find the stock by symbol
        stmt = select(Stock).where(Stock.symbol == watchlist_in.stock_symbol.upper())
        result = await db.execute(stmt)
        stock = result.scalar_one_or_none()
        
        if not stock:
            raise NotFoundException(detail=f"Stock with symbol {watchlist_in.stock_symbol} not found")

        # Check if already in watchlist
        stmt = select(Watchlist).where(
            Watchlist.user_id == user_id, 
            Watchlist.stock_id == stock.id
        )
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            # If already exists, return existing or raise exception depending on requirements
            # We'll just update it or return it. Let's return it.
            return existing

        watchlist_item = Watchlist(
            user_id=user_id,
            stock_id=stock.id,
            target_price=watchlist_in.target_price,
            alert_type=watchlist_in.alert_type,
            notes=watchlist_in.notes,
        )
        db.add(watchlist_item)
        await db.commit()
        await db.refresh(watchlist_item)
        return watchlist_item

    @staticmethod
    async def get_user_watchlist(
        db: AsyncSession,
        user_id: uuid.UUID,
    ) -> Sequence[Watchlist]:
        """Fetch all watchlist items belonging to a specific user."""
        stmt = (
            select(Watchlist)
            .where(Watchlist.user_id == user_id)
            .order_by(Watchlist.created_at.desc())
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_watchlist_item_by_id(
        db: AsyncSession,
        item_id: uuid.UUID,
        user_id: Optional[uuid.UUID] = None,
        is_admin: bool = False,
    ) -> Watchlist:
        """Fetch a single watchlist item by ID."""
        stmt = select(Watchlist).where(Watchlist.id == item_id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()

        if not item:
            raise NotFoundException(detail="Watchlist item not found")

        if user_id and not is_admin and item.user_id != user_id:
            raise ForbiddenException(detail="Access denied: You do not own this watchlist item")

        return item

    @staticmethod
    async def update_watchlist_item(
        db: AsyncSession,
        item_id: uuid.UUID,
        user_id: uuid.UUID,
        watchlist_in: WatchlistUpdate,
        is_admin: bool = False,
    ) -> Watchlist:
        """Update an existing watchlist item after verifying user ownership."""
        item = await WatchlistService.get_watchlist_item_by_id(db, item_id, user_id, is_admin=is_admin)

        update_data = watchlist_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(item, field, value)

        # If target price or alert type changes, we might want to reset is_triggered
        if "target_price" in update_data or "alert_type" in update_data:
            item.is_triggered = False
            item.triggered_at = None

        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def remove_from_watchlist(
        db: AsyncSession,
        item_id: uuid.UUID,
        user_id: uuid.UUID,
        is_admin: bool = False,
    ) -> bool:
        """Delete a watchlist item after verifying user ownership."""
        item = await WatchlistService.get_watchlist_item_by_id(db, item_id, user_id, is_admin=is_admin)
        await db.delete(item)
        await db.commit()
        return True
