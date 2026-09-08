"""
Transactions Router — Day 6
BUY / SELL trade execution, cash deposits, and transaction history endpoints.
All endpoints are scoped under a portfolio (ownership enforced).
"""

from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.models.transaction import TransactionType
from app.models.user import User
from app.schemas.transaction import (
    DepositRequest,
    DepositResponse,
    PaginatedTransactionResponse,
    PortfolioBalanceUpdate,
    TransactionCreate,
    TransactionOut,
    TransactionResponse,
)
from app.services.portfolio_service import PortfolioService
from app.services.transaction_service import (
    deposit_cash,
    execute_transaction,
    get_portfolio_transactions,
    get_transaction_by_id,
)

router = APIRouter(tags=["Transactions"])


# ── Helper: resolve & authorize portfolio ─────────────────────────────────────

async def _get_owned_portfolio(
    portfolio_id: uuid.UUID,
    current_user: User,
    db: AsyncSession,
):
    """Fetch portfolio and verify the current user owns it (or is admin)."""
    return await PortfolioService.get_portfolio_by_id(
        db,
        portfolio_id,
        user_id=current_user.id,
        is_admin=current_user.is_admin,
    )


# ── Deposit Cash ─────────────────────────────────────────────────────────────

@router.post(
    "/portfolios/{portfolio_id}/deposit",
    response_model=DepositResponse,
    status_code=status.HTTP_200_OK,
    summary="Deposit cash into portfolio",
    description=(
        "Adds funds to a portfolio's cash balance, enabling BUY trades. "
        "Requires portfolio ownership. Deposit amount must be > 0."
    ),
)
async def deposit_to_portfolio(
    portfolio_id: uuid.UUID,
    deposit_in: DepositRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> DepositResponse:
    portfolio = await _get_owned_portfolio(portfolio_id, current_user, db)
    updated = await deposit_cash(db, portfolio, deposit_in.amount)

    return DepositResponse(
        message=f"Successfully deposited {portfolio.currency} {deposit_in.amount:,.2f} into portfolio '{portfolio.name}'.",
        amount_deposited=deposit_in.amount,
        portfolio_balance=PortfolioBalanceUpdate(
            portfolio_id=updated.id,
            cash_balance=updated.cash_balance,
            total_invested=updated.total_invested,
            currency=updated.currency,
        ),
    )


# ── Execute Trade (BUY or SELL) ───────────────────────────────────────────────

@router.post(
    "/portfolios/{portfolio_id}/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Execute BUY or SELL transaction",
    description=(
        "Records a BUY or SELL trade for a stock within the specified portfolio. "
        "**BUY**: Deducts `(quantity × price_per_share) + fees` from `cash_balance`. "
        "Raises `400 INSUFFICIENT_FUNDS` if balance is too low. "
        "**SELL**: Adds `(quantity × price_per_share) - fees` to `cash_balance`. "
        "Raises `400 INSUFFICIENT_SHARES` if held quantity is less than requested."
    ),
)
async def create_transaction(
    portfolio_id: uuid.UUID,
    tx_in: TransactionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> TransactionResponse:
    portfolio = await _get_owned_portfolio(portfolio_id, current_user, db)
    transaction = await execute_transaction(db, portfolio, tx_in)

    return TransactionResponse(
        transaction=TransactionOut.model_validate(transaction),
        portfolio_balance=PortfolioBalanceUpdate(
            portfolio_id=portfolio.id,
            cash_balance=portfolio.cash_balance,
            total_invested=portfolio.total_invested,
            currency=portfolio.currency,
        ),
    )


# ── Transaction History ───────────────────────────────────────────────────────

@router.get(
    "/portfolios/{portfolio_id}/transactions",
    response_model=PaginatedTransactionResponse,
    status_code=status.HTTP_200_OK,
    summary="List portfolio transactions",
    description=(
        "Returns paginated BUY/SELL transaction history for a portfolio. "
        "Supports filtering by `transaction_type` (BUY/SELL) and `stock_symbol`."
    ),
)
async def list_transactions(
    portfolio_id: uuid.UUID,
    transaction_type: Optional[TransactionType] = Query(
        None, description="Filter by BUY or SELL"
    ),
    stock_symbol: Optional[str] = Query(
        None, description="Filter by stock ticker symbol (e.g. AAPL)"
    ),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> PaginatedTransactionResponse:
    await _get_owned_portfolio(portfolio_id, current_user, db)

    transactions, total = await get_portfolio_transactions(
        db,
        portfolio_id=portfolio_id,
        transaction_type=transaction_type,
        stock_symbol=stock_symbol,
        page=page,
        page_size=page_size,
    )
    items = [TransactionOut.model_validate(tx) for tx in transactions]
    return PaginatedTransactionResponse.create(
        items=items, total=total, page=page, page_size=page_size
    )


# ── Single Transaction Detail ─────────────────────────────────────────────────

@router.get(
    "/portfolios/{portfolio_id}/transactions/{transaction_id}",
    response_model=TransactionOut,
    status_code=status.HTTP_200_OK,
    summary="Get transaction detail",
    description=(
        "Retrieve a single transaction by its ID within the specified portfolio. "
        "Returns 404 if the transaction does not belong to this portfolio."
    ),
)
async def get_transaction(
    portfolio_id: uuid.UUID,
    transaction_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> TransactionOut:
    await _get_owned_portfolio(portfolio_id, current_user, db)
    transaction = await get_transaction_by_id(db, transaction_id, portfolio_id)
    return TransactionOut.model_validate(transaction)
