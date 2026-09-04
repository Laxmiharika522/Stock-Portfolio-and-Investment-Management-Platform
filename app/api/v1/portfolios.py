"""
Portfolio Router — Day 4
Endpoints for managing investment portfolios with strict ownership authorization.
"""

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.core.exceptions import ForbiddenException
from app.models.user import User
from app.schemas.portfolio import PortfolioCreate, PortfolioOut, PortfolioUpdate
from app.services.portfolio_service import PortfolioService

router = APIRouter(prefix="/portfolios", tags=["Portfolios"])


@router.post(
    "",
    response_model=PortfolioOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create portfolio",
    description="Creates a new investment portfolio for the currently authenticated user.",
)
async def create_portfolio(
    portfolio_in: PortfolioCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> PortfolioOut:
    portfolio = await PortfolioService.create_portfolio(db, current_user.id, portfolio_in)
    return PortfolioOut.model_validate(portfolio)


@router.get(
    "",
    response_model=List[PortfolioOut],
    summary="List user portfolios",
    description="Fetches all portfolios owned by the authenticated user.",
)
async def list_portfolios(
    user_id: Optional[uuid.UUID] = Query(None, description="Target user ID (Admin only to view other user portfolios)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> List[PortfolioOut]:
    target_user_id = current_user.id
    if user_id and user_id != current_user.id:
        if not current_user.is_admin:
            raise ForbiddenException(detail="Access denied: Cannot view another user's portfolios")
        target_user_id = user_id

    portfolios = await PortfolioService.get_user_portfolios(db, target_user_id, skip=skip, limit=limit)
    return [PortfolioOut.model_validate(p) for p in portfolios]


@router.get(
    "/{portfolio_id}",
    response_model=PortfolioOut,
    summary="Get portfolio details",
    description="Retrieves a specific portfolio by ID after verifying ownership (403 if not owned).",
)
async def get_portfolio(
    portfolio_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> PortfolioOut:
    portfolio = await PortfolioService.get_portfolio_by_id(
        db, portfolio_id, user_id=current_user.id, is_admin=current_user.is_admin
    )
    return PortfolioOut.model_validate(portfolio)


@router.put(
    "/{portfolio_id}",
    response_model=PortfolioOut,
    summary="Update portfolio",
    description="Updates a portfolio's details (name, description, currency, default status) after verifying ownership.",
)
async def update_portfolio(
    portfolio_id: uuid.UUID,
    portfolio_in: PortfolioUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> PortfolioOut:
    portfolio = await PortfolioService.update_portfolio(
        db, portfolio_id, user_id=current_user.id, portfolio_in=portfolio_in, is_admin=current_user.is_admin
    )
    return PortfolioOut.model_validate(portfolio)


@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete portfolio",
    description="Deletes an investment portfolio after verifying ownership.",
)
async def delete_portfolio(
    portfolio_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    await PortfolioService.delete_portfolio(
        db, portfolio_id, user_id=current_user.id, is_admin=current_user.is_admin
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
