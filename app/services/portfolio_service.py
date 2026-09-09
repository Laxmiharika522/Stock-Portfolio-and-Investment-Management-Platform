"""
Portfolio Service Layer — Day 4
Contains business logic for managing portfolios and enforcing ownership.
"""

import uuid
from typing import Sequence, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate
from app.core.exceptions import ForbiddenException, NotFoundException


class PortfolioService:

    @staticmethod
    async def create_portfolio(
        db: AsyncSession,
        user_id: uuid.UUID,
        portfolio_in: PortfolioCreate,
    ) -> Portfolio:
        """Create a new portfolio owned by the specified user."""
        # If set as default, unset existing default portfolios for user
        if portfolio_in.is_default:
            await db.execute(
                update(Portfolio)
                .where(Portfolio.user_id == user_id)
                .values(is_default=False)
            )

        portfolio = Portfolio(
            user_id=user_id,
            name=portfolio_in.name,
            description=portfolio_in.description,
            currency=portfolio_in.currency.upper(),
            is_default=portfolio_in.is_default,
        )
        db.add(portfolio)
        await db.commit()
        await db.refresh(portfolio)
        return portfolio

    @staticmethod
    async def get_user_portfolios(
        db: AsyncSession,
        user_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Portfolio]:
        """Fetch all portfolios belonging to a specific user."""
        stmt = (
            select(Portfolio)
            .where(Portfolio.user_id == user_id)
            .order_by(Portfolio.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_portfolio_by_id(
        db: AsyncSession,
        portfolio_id: uuid.UUID,
        user_id: Optional[uuid.UUID] = None,
        is_admin: bool = False,
    ) -> Portfolio:
        """
        Fetch a single portfolio by ID.
        If user_id is provided, validates ownership (raises ForbiddenException if owned by another user).
        Admin bypasses ownership check.
        """
        stmt = select(Portfolio).where(Portfolio.id == portfolio_id)
        result = await db.execute(stmt)
        portfolio = result.scalar_one_or_none()

        if not portfolio:
            raise NotFoundException(detail="Portfolio not found")

        if user_id and not is_admin and portfolio.user_id != user_id:
            raise ForbiddenException(detail="Access denied: You do not own this portfolio")

        return portfolio

    @staticmethod
    async def update_portfolio(
        db: AsyncSession,
        portfolio_id: uuid.UUID,
        user_id: uuid.UUID,
        portfolio_in: PortfolioUpdate,
        is_admin: bool = False,
    ) -> Portfolio:
        """Update an existing portfolio after verifying user ownership."""
        portfolio = await PortfolioService.get_portfolio_by_id(db, portfolio_id, user_id, is_admin=is_admin)

        update_data = portfolio_in.model_dump(exclude_unset=True)

        if update_data.get("is_default"):
            await db.execute(
                update(Portfolio)
                .where(Portfolio.user_id == portfolio.user_id)
                .values(is_default=False)
            )

        if "currency" in update_data and update_data["currency"]:
            update_data["currency"] = update_data["currency"].upper()

        for field, value in update_data.items():
            setattr(portfolio, field, value)

        await db.commit()
        await db.refresh(portfolio)
        return portfolio

    @staticmethod
    async def delete_portfolio(
        db: AsyncSession,
        portfolio_id: uuid.UUID,
        user_id: uuid.UUID,
        is_admin: bool = False,
    ) -> bool:
        """Delete a portfolio after verifying user ownership."""
        portfolio = await PortfolioService.get_portfolio_by_id(db, portfolio_id, user_id, is_admin=is_admin)
        await db.delete(portfolio)
        await db.commit()
        return True

    @staticmethod
    async def get_portfolio_holdings(
        db: AsyncSession,
        portfolio_id: uuid.UUID,
        user_id: uuid.UUID,
        is_admin: bool = False,
    ) -> list[dict]:
        """Calculate and return holdings for a portfolio."""
        portfolio = await PortfolioService.get_portfolio_by_id(db, portfolio_id, user_id, is_admin=is_admin)

        from app.models.transaction import Transaction, TransactionType
        from sqlalchemy.orm import joinedload
        
        stmt = (
            select(Transaction)
            .options(joinedload(Transaction.stock))
            .where(Transaction.portfolio_id == portfolio_id)
            .order_by(Transaction.transacted_at.asc())
        )
        result = await db.execute(stmt)
        transactions = result.scalars().all()
        
        holdings_map = {}
        
        for tx in transactions:
            sym = tx.stock.symbol
            if sym not in holdings_map:
                holdings_map[sym] = {
                    "stock_symbol": sym,
                    "company_name": tx.stock.company_name,
                    "quantity": 0.0,
                    "total_buy_cost": 0.0,
                    "total_buy_qty": 0.0,
                    "current_price": 0.0,
                }
            
            holding = holdings_map[sym]
            
            if tx.transaction_type == TransactionType.BUY:
                holding["quantity"] += tx.quantity
                holding["total_buy_cost"] += (tx.quantity * tx.price_per_share)
                holding["total_buy_qty"] += tx.quantity
            elif tx.transaction_type == TransactionType.SELL:
                holding["quantity"] -= tx.quantity
                
            holding["current_price"] = tx.price_per_share
            
        holdings = []
        for holding in holdings_map.values():
            if holding["quantity"] > 0.00001:  # handle floating point precision
                wabp = holding["total_buy_cost"] / holding["total_buy_qty"] if holding["total_buy_qty"] > 0 else 0.0
                current_price = holding["current_price"]
                total_value = holding["quantity"] * current_price
                unrealized_pnl = total_value - (holding["quantity"] * wabp)
                unrealized_pnl_percentage = (unrealized_pnl / (holding["quantity"] * wabp) * 100) if wabp > 0 and holding["quantity"] > 0 else 0.0
                
                holdings.append({
                    "stock_symbol": holding["stock_symbol"],
                    "company_name": holding["company_name"],
                    "quantity": round(holding["quantity"], 4),
                    "weighted_average_buy_price": round(wabp, 2),
                    "current_price": round(current_price, 2),
                    "total_value": round(total_value, 2),
                    "unrealized_pnl": round(unrealized_pnl, 2),
                    "unrealized_pnl_percentage": round(unrealized_pnl_percentage, 2),
                })
                
        return holdings
