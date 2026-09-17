"""
Admin Router — Day 13
Administrator-only endpoints for managing users, stocks, and viewing system stats.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin_user
from app.db.session import get_db
from app.models.user import User
from app.models.portfolio import Portfolio
from app.models.transaction import Transaction
from app.models.stock import Stock
from app.schemas.user import UserOut

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=list[UserOut])
async def list_users(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """List all users."""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.put("/users/{user_id}/activate")
async def toggle_user_active(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Activate or deactivate a user."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = not user.is_active
    await db.commit()
    return {"message": f"User is_active set to {user.is_active}"}


@router.put("/users/{user_id}/role")
async def toggle_user_role(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Promote or demote a user to/from admin role."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_admin = not user.is_admin
    await db.commit()
    return {"message": f"User is_admin set to {user.is_admin}"}


@router.get("/stats")
async def get_system_stats(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Get overall platform statistics."""
    users_count = await db.scalar(select(func.count(User.id)))
    portfolios_count = await db.scalar(select(func.count(Portfolio.id)))
    transactions_count = await db.scalar(select(func.count(Transaction.id)))
    stocks_count = await db.scalar(select(func.count(Stock.id)))
    
    return {
        "total_users": users_count,
        "total_portfolios": portfolios_count,
        "total_transactions": transactions_count,
        "total_stocks": stocks_count,
    }


@router.get("/audit-log")
async def get_audit_log(
    admin: User = Depends(get_current_admin_user)
):
    """Get audit logs of admin actions (mocked)."""
    return [
        {"action": "Promoted user X to admin", "timestamp": "2026-09-17T12:00:00Z"},
        {"action": "Deactivated user Y", "timestamp": "2026-09-17T13:30:00Z"},
    ]
