"""
Stock Catalog API Endpoints — Day 5
Provides stock listing with search/filter/pagination, stock details lookup, and admin-only management.
"""

from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_admin_user
from app.core.exceptions import NotFoundException
from app.models.user import User
from app.schemas.stock import (
    StockCreate,
    StockUpdate,
    StockOut,
    PaginatedStockResponse,
)
from app.services.stock_service import (
    create_stock,
    get_stock_by_symbol,
    update_stock,
    list_stocks,
    seed_popular_stocks,
)

router = APIRouter(prefix="/stocks", tags=["Stocks"])


@router.get(
    "",
    response_model=PaginatedStockResponse,
    status_code=status.HTTP_200_OK,
    summary="List stocks with search, filter, and pagination",
    description="Retrieve stock catalog. Supports keyword search (`q`), filtering by sector/exchange, sorting, and pagination.",
)
async def list_stocks_endpoint(
    q: Optional[str] = Query(None, description="Search term matching symbol or company name"),
    sector: Optional[str] = Query(None, description="Filter by industry sector (e.g. Technology, Healthcare)"),
    exchange: Optional[str] = Query(None, description="Filter by exchange market (e.g. NASDAQ, NYSE)"),
    sort_by: str = Query("symbol", description="Sort field: symbol, company_name, sector, exchange, market_cap, created_at"),
    order: str = Query("asc", description="Sort direction: asc or desc"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page (max 100)"),
    db: AsyncSession = Depends(get_db),
):
    stocks, total = await list_stocks(
        db=db,
        q=q,
        sector=sector,
        exchange=exchange,
        sort_by=sort_by,
        order=order,
        page=page,
        page_size=page_size,
    )
    items = [StockOut.model_validate(s) for s in stocks]
    return PaginatedStockResponse.create(items=items, total=total, page=page, page_size=page_size)


@router.post(
    "/seed",
    status_code=status.HTTP_200_OK,
    summary="Seed popular stocks catalog (Admin only)",
    description="Populates database with 20+ top stock assets if missing.",
)
async def seed_stocks_endpoint(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    created_count = await seed_popular_stocks(db)
    return {"message": f"Successfully seeded {created_count} stocks into catalog", "created_count": created_count}


@router.get(
    "/{symbol}",
    response_model=StockOut,
    status_code=status.HTTP_200_OK,
    summary="Get stock details by ticker symbol",
    description="Fetch single stock detail record by case-insensitive ticker symbol (e.g., AAPL).",
)
async def get_stock_by_symbol_endpoint(
    symbol: str,
    db: AsyncSession = Depends(get_db),
):
    stock = await get_stock_by_symbol(db, symbol)
    if not stock:
        raise NotFoundException(message=f"Stock ticker symbol '{symbol.upper()}' was not found in catalog")
    return StockOut.model_validate(stock)


@router.post(
    "",
    response_model=StockOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new stock record (Admin only)",
    description="Adds a new ticker symbol to the global stock catalog. Requires administrator permissions.",
)
async def create_stock_endpoint(
    stock_in: StockCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    stock = await create_stock(db, stock_in)
    return StockOut.model_validate(stock)


@router.put(
    "/{symbol}",
    response_model=StockOut,
    status_code=status.HTTP_200_OK,
    summary="Update stock details (Admin only)",
    description="Modify attributes of an existing stock record. Requires administrator permissions.",
)
async def update_stock_endpoint(
    symbol: str,
    stock_in: StockUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    stock = await update_stock(db, symbol, stock_in)
    return StockOut.model_validate(stock)
