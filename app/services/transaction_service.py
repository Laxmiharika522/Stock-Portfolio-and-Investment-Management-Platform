"""
Transaction Service — Day 6
Core business logic for executing BUY/SELL trades, balance validation,
cash deposits, and transaction history retrieval.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional, Sequence, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.exceptions import (
    BadRequestException,
    ForbiddenException,
    InsufficientFundsException,
    InsufficientSharesException,
    NotFoundException,
)
from app.models.portfolio import Portfolio
from app.models.stock import Stock
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate


# ── Internal Helpers ──────────────────────────────────────────────────────────

async def _get_stock_by_symbol(db: AsyncSession, symbol: str) -> Stock:
    """Fetch an active stock by ticker symbol (case-insensitive). Raises 404 if missing."""
    stmt = select(Stock).where(
        Stock.symbol == symbol.upper(),
        Stock.is_active.is_(True),
    )
    result = await db.execute(stmt)
    stock = result.scalar_one_or_none()
    if not stock:
        raise NotFoundException(
            message=f"Stock symbol '{symbol.upper()}' not found in catalog or is inactive."
        )
    return stock


async def _get_held_quantity(
    db: AsyncSession, portfolio_id: uuid.UUID, stock_id: uuid.UUID
) -> float:
    """
    Calculate the net quantity currently held for a stock in a portfolio.
    Net = sum(BUY quantities) - sum(SELL quantities).
    """
    buy_stmt = select(func.coalesce(func.sum(Transaction.quantity), 0.0)).where(
        Transaction.portfolio_id == portfolio_id,
        Transaction.stock_id == stock_id,
        Transaction.transaction_type == TransactionType.BUY,
    )
    sell_stmt = select(func.coalesce(func.sum(Transaction.quantity), 0.0)).where(
        Transaction.portfolio_id == portfolio_id,
        Transaction.stock_id == stock_id,
        Transaction.transaction_type == TransactionType.SELL,
    )
    buy_result = await db.execute(buy_stmt)
    sell_result = await db.execute(sell_stmt)

    total_bought: float = buy_result.scalar() or 0.0
    total_sold: float = sell_result.scalar() or 0.0
    return round(total_bought - total_sold, 4)


# ── Core Transaction Operations ───────────────────────────────────────────────

async def deposit_cash(
    db: AsyncSession,
    portfolio: Portfolio,
    amount: float,
) -> Portfolio:
    """
    Deposit cash into a portfolio's cash_balance.
    Amount must be > 0 (validated by schema, but double-checked here).
    """
    if amount <= 0:
        raise BadRequestException("Deposit amount must be greater than zero")

    portfolio.cash_balance = round(portfolio.cash_balance + amount, 2)
    await db.commit()
    await db.refresh(portfolio)
    return portfolio


async def execute_transaction(
    db: AsyncSession,
    portfolio: Portfolio,
    tx_in: TransactionCreate,
) -> Transaction:
    """
    Execute a BUY or SELL transaction with full validation.

    BUY logic:
      - total_cost = (quantity × price_per_share) + fees
      - Validates: cash_balance >= total_cost
      - Deducts total_cost from cash_balance
      - Increments total_invested by (quantity × price_per_share)

    SELL logic:
      - net_proceeds = (quantity × price_per_share) - fees
      - Validates: held_quantity >= requested quantity
      - Adds net_proceeds to cash_balance
      - Decrements total_invested by (quantity × price_per_share)
    """
    # 1. Resolve stock
    stock = await _get_stock_by_symbol(db, tx_in.stock_symbol)

    # 2. Compute amounts
    gross_value = round(tx_in.quantity * tx_in.price_per_share, 2)
    fees = round(tx_in.fees, 2)

    if tx_in.transaction_type == TransactionType.BUY:
        total_amount = round(gross_value + fees, 2)

        # 3a. Balance check
        if portfolio.cash_balance < total_amount:
            raise InsufficientFundsException(
                required=total_amount,
                available=portfolio.cash_balance,
                currency=portfolio.currency,
            )

        # 4a. Deduct from portfolio
        portfolio.cash_balance = round(portfolio.cash_balance - total_amount, 2)
        portfolio.total_invested = round(portfolio.total_invested + gross_value, 2)

    else:  # SELL
        total_amount = round(gross_value - fees, 2)  # net proceeds after fees

        # 3b. Holdings check
        held_qty = await _get_held_quantity(db, portfolio.id, stock.id)
        if held_qty < tx_in.quantity:
            raise InsufficientSharesException(
                symbol=stock.symbol,
                owned=held_qty,
                requested=tx_in.quantity,
            )

        # 4b. Add proceeds to portfolio
        portfolio.cash_balance = round(portfolio.cash_balance + total_amount, 2)
        # Decrement total_invested proportionally (can't go below 0)
        portfolio.total_invested = round(
            max(0.0, portfolio.total_invested - gross_value), 2
        )

    # 5. Create transaction record
    tx_time = tx_in.transacted_at or datetime.now(timezone.utc)
    transaction = Transaction(
        portfolio_id=portfolio.id,
        stock_id=stock.id,
        transaction_type=tx_in.transaction_type,
        quantity=tx_in.quantity,
        price_per_share=tx_in.price_per_share,
        fees=fees,
        total_amount=total_amount,
        notes=tx_in.notes,
        transacted_at=tx_time,
    )

    db.add(transaction)
    await db.commit()
    await db.refresh(portfolio)
    # Eager-load stock on the transaction for the response
    stmt = (
        select(Transaction)
        .options(joinedload(Transaction.stock))
        .where(Transaction.id == transaction.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


# ── History Retrieval ─────────────────────────────────────────────────────────

async def get_portfolio_transactions(
    db: AsyncSession,
    portfolio_id: uuid.UUID,
    transaction_type: Optional[TransactionType] = None,
    stock_symbol: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> Tuple[Sequence[Transaction], int]:
    """
    Retrieve paginated transaction history for a portfolio.
    Supports optional filtering by transaction_type and stock_symbol.
    Returns (transactions, total_count).
    """
    base_where = [Transaction.portfolio_id == portfolio_id]

    if transaction_type:
        base_where.append(Transaction.transaction_type == transaction_type)

    if stock_symbol:
        # Join to filter by stock symbol
        stock_stmt = select(Stock.id).where(Stock.symbol == stock_symbol.upper())
        stock_result = await db.execute(stock_stmt)
        stock_id = stock_result.scalar_one_or_none()
        if stock_id:
            base_where.append(Transaction.stock_id == stock_id)
        else:
            return [], 0  # Symbol not found → empty result

    # Count total
    count_stmt = select(func.count()).select_from(Transaction).where(*base_where)
    count_result = await db.execute(count_stmt)
    total: int = count_result.scalar() or 0

    # Fetch page
    offset = (page - 1) * page_size
    stmt = (
        select(Transaction)
        .options(joinedload(Transaction.stock))
        .where(*base_where)
        .order_by(Transaction.transacted_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    transactions = result.scalars().all()

    return transactions, total


async def get_transaction_by_id(
    db: AsyncSession,
    transaction_id: uuid.UUID,
    portfolio_id: uuid.UUID,
) -> Transaction:
    """
    Fetch a single transaction by ID, scoped to the given portfolio.
    Raises 404 if not found (also prevents cross-portfolio access).
    """
    stmt = (
        select(Transaction)
        .options(joinedload(Transaction.stock))
        .where(
            Transaction.id == transaction_id,
            Transaction.portfolio_id == portfolio_id,
        )
    )
    result = await db.execute(stmt)
    transaction = result.scalar_one_or_none()

    if not transaction:
        raise NotFoundException(
            message=f"Transaction '{transaction_id}' not found in this portfolio."
        )
    return transaction
