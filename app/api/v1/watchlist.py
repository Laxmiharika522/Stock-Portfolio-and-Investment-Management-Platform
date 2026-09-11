"""
Watchlist Router — Day 9
Endpoints for managing watchlist and target price alerts.
"""

import uuid
from typing import List
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.watchlist import WatchlistCreate, WatchlistOut, WatchlistUpdate
from app.services.watchlist_service import WatchlistService

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])


@router.post(
    "",
    response_model=WatchlistOut,
    status_code=status.HTTP_201_CREATED,
    summary="Add stock to watchlist",
    description="Adds a stock to the user's watchlist with an optional target price alert.",
)
async def add_to_watchlist(
    watchlist_in: WatchlistCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> WatchlistOut:
    watchlist_item = await WatchlistService.add_to_watchlist(db, current_user.id, watchlist_in)
    return WatchlistOut.model_validate(watchlist_item)


@router.get(
    "",
    response_model=List[WatchlistOut],
    summary="List user watchlist",
    description="Fetches all watchlist items for the authenticated user.",
)
async def list_watchlist(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> List[WatchlistOut]:
    items = await WatchlistService.get_user_watchlist(db, current_user.id)
    return [WatchlistOut.model_validate(i) for i in items]


@router.put(
    "/{item_id}",
    response_model=WatchlistOut,
    summary="Update watchlist item",
    description="Updates a watchlist item's target price or alert type.",
)
async def update_watchlist(
    item_id: uuid.UUID,
    watchlist_in: WatchlistUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> WatchlistOut:
    item = await WatchlistService.update_watchlist_item(
        db, item_id, user_id=current_user.id, watchlist_in=watchlist_in, is_admin=current_user.is_admin
    )
    return WatchlistOut.model_validate(item)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove from watchlist",
    description="Removes a stock from the user's watchlist.",
)
async def remove_from_watchlist(
    item_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    await WatchlistService.remove_from_watchlist(
        db, item_id, user_id=current_user.id, is_admin=current_user.is_admin
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
