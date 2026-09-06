"""
Stock Service Layer — Day 5
Implements business logic for stock catalog management, search, filtering, pagination, and stock seeding.
"""

from __future__ import annotations

import logging
from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, or_, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException, NotFoundException
from app.models.stock import Stock
from app.schemas.stock import StockCreate, StockUpdate

logger = logging.getLogger(__name__)

# Catalog seed data containing 22 popular US & global equities across sectors
POPULAR_STOCKS_SEED = [
    {
        "symbol": "AAPL",
        "company_name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "exchange": "NASDAQ",
        "currency": "USD",
        "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories.",
        "logo_url": "https://logo.clearbit.com/apple.com",
        "market_cap": 3450000000000.0,
    },
    {
        "symbol": "MSFT",
        "company_name": "Microsoft Corporation",
        "sector": "Technology",
        "industry": "Software - Infrastructure",
        "exchange": "NASDAQ",
        "currency": "USD",
        "description": "Microsoft Corporation develops and supports software, services, devices and solutions worldwide.",
        "logo_url": "https://logo.clearbit.com/microsoft.com",
        "market_cap": 3100000000000.0,
    },
    {
        "symbol": "GOOGL",
        "company_name": "Alphabet Inc.",
        "sector": "Communication Services",
        "industry": "Internet Content & Information",
        "exchange": "NASDAQ",
        "currency": "USD",
        "description": "Alphabet Inc. offers search, cloud infrastructure, online advertising, and digital entertainment products.",
        "logo_url": "https://logo.clearbit.com/abc.xyz",
        "market_cap": 2200000000000.0,
    },
    {
        "symbol": "AMZN",
        "company_name": "Amazon.com Inc.",
        "sector": "Consumer Cyclical",
        "industry": "Internet Retail",
        "exchange": "NASDAQ",
        "currency": "USD",
        "description": "Amazon.com Inc. engages in retail sales, cloud computing services (AWS), and digital streaming.",
        "logo_url": "https://logo.clearbit.com/amazon.com",
        "market_cap": 1950000000000.0,
    },
    {
        "symbol": "NVDA",
        "company_name": "NVIDIA Corporation",
        "sector": "Technology",
        "industry": "Semiconductors",
        "exchange": "NASDAQ",
        "currency": "USD",
        "description": "NVIDIA Corporation designs graphics processing units (GPUs) and AI computing chips.",
        "logo_url": "https://logo.clearbit.com/nvidia.com",
        "market_cap": 3000000000000.0,
    },
    {
        "symbol": "TSLA",
        "company_name": "Tesla Inc.",
        "sector": "Consumer Cyclical",
        "industry": "Auto Manufacturers",
        "exchange": "NASDAQ",
        "currency": "USD",
        "description": "Tesla Inc. designs, manufactures, and sells electric vehicles, solar panels, and energy storage systems.",
        "logo_url": "https://logo.clearbit.com/tesla.com",
        "market_cap": 750000000000.0,
    },
    {
        "symbol": "META",
        "company_name": "Meta Platforms Inc.",
        "sector": "Communication Services",
        "industry": "Internet Content & Information",
        "exchange": "NASDAQ",
        "currency": "USD",
        "description": "Meta Platforms Inc. operates social platforms including Facebook, Instagram, WhatsApp, and Threads.",
        "logo_url": "https://logo.clearbit.com/meta.com",
        "market_cap": 1300000000000.0,
    },
    {
        "symbol": "BRK.A",
        "company_name": "Berkshire Hathaway Inc.",
        "sector": "Financial",
        "industry": "Financial Conglomerate",
        "exchange": "NYSE",
        "currency": "USD",
        "description": "Berkshire Hathaway Inc. is a multinational conglomerate holding company led by Warren Buffett.",
        "logo_url": "https://logo.clearbit.com/berkshirehathaway.com",
        "market_cap": 980000000000.0,
    },
    {
        "symbol": "V",
        "company_name": "Visa Inc.",
        "sector": "Financial",
        "industry": "Credit Services",
        "exchange": "NYSE",
        "currency": "USD",
        "description": "Visa Inc. operates a global digital payments network facilitating electronic funds transfers.",
        "logo_url": "https://logo.clearbit.com/visa.com",
        "market_cap": 570000000000.0,
    },
    {
        "symbol": "JNJ",
        "company_name": "Johnson & Johnson",
        "sector": "Healthcare",
        "industry": "Pharmaceuticals",
        "exchange": "NYSE",
        "currency": "USD",
        "description": "Johnson & Johnson researches, develops, manufactures, and sells healthcare products globally.",
        "logo_url": "https://logo.clearbit.com/jnj.com",
        "market_cap": 380000000000.0,
    },
    {
        "symbol": "WMT",
        "company_name": "Walmart Inc.",
        "sector": "Consumer Defensive",
        "industry": "Discount Stores",
        "exchange": "NYSE",
        "currency": "USD",
        "description": "Walmart Inc. operates retail discount stores, supercenters, and e-commerce websites.",
        "logo_url": "https://logo.clearbit.com/walmart.com",
        "market_cap": 580000000000.0,
    },
    {
        "symbol": "JPM",
        "company_name": "JPMorgan Chase & Co.",
        "sector": "Financial",
        "industry": "Banks - Diversified",
        "exchange": "NYSE",
        "currency": "USD",
        "description": "JPMorgan Chase & Co. is a global financial services firm and investment bank.",
        "logo_url": "https://logo.clearbit.com/jpmorganchase.com",
        "market_cap": 610000000000.0,
    },
    {
        "symbol": "PG",
        "company_name": "Procter & Gamble Co.",
        "sector": "Consumer Defensive",
        "industry": "Household & Personal Products",
        "exchange": "NYSE",
        "currency": "USD",
        "description": "Procter & Gamble manufactures and markets branded consumer packaged goods.",
        "logo_url": "https://logo.clearbit.com/pg.com",
        "market_cap": 400000000000.0,
    },
    {
        "symbol": "UNH",
        "company_name": "UnitedHealth Group Inc.",
        "sector": "Healthcare",
        "industry": "Healthcare Plans",
        "exchange": "NYSE",
        "currency": "USD",
        "description": "UnitedHealth Group provides health care coverage and health technology services.",
        "logo_url": "https://logo.clearbit.com/unitedhealthgroup.com",
        "market_cap": 520000000000.0,
    },
    {
        "symbol": "MA",
        "company_name": "Mastercard Incorporated",
        "sector": "Financial",
        "industry": "Credit Services",
        "exchange": "NYSE",
        "currency": "USD",
        "description": "Mastercard connects consumers, financial institutions, and merchants globally for payment processing.",
        "logo_url": "https://logo.clearbit.com/mastercard.com",
        "market_cap": 440000000000.0,
    },
    {
        "symbol": "HD",
        "company_name": "The Home Depot Inc.",
        "sector": "Consumer Cyclical",
        "industry": "Home Improvement Retail",
        "exchange": "NYSE",
        "currency": "USD",
        "description": "The Home Depot is the world's largest home improvement specialty retailer.",
        "logo_url": "https://logo.clearbit.com/homedepot.com",
        "market_cap": 370000000000.0,
    },
    {
        "symbol": "DIS",
        "company_name": "The Walt Disney Company",
        "sector": "Communication Services",
        "industry": "Entertainment",
        "exchange": "NYSE",
        "currency": "USD",
        "description": "The Walt Disney Company operates theme parks, media networks, and streaming services.",
        "logo_url": "https://logo.clearbit.com/disney.com",
        "market_cap": 175000000000.0,
    },
    {
        "symbol": "PYPL",
        "company_name": "PayPal Holdings Inc.",
        "sector": "Financial",
        "industry": "Credit Services",
        "exchange": "NASDAQ",
        "currency": "USD",
        "description": "PayPal operates a global digital platform enabling online payments and money transfers.",
        "logo_url": "https://logo.clearbit.com/paypal.com",
        "market_cap": 72000000000.0,
    },
    {
        "symbol": "NFLX",
        "company_name": "Netflix Inc.",
        "sector": "Communication Services",
        "industry": "Entertainment",
        "exchange": "NASDAQ",
        "currency": "USD",
        "description": "Netflix Inc. provides subscription-based video streaming and entertainment content.",
        "logo_url": "https://logo.clearbit.com/netflix.com",
        "market_cap": 290000000000.0,
    },
    {
        "symbol": "ADBE",
        "company_name": "Adobe Inc.",
        "sector": "Technology",
        "industry": "Software - Infrastructure",
        "exchange": "NASDAQ",
        "currency": "USD",
        "description": "Adobe Inc. offers creative cloud software, digital media, and document solutions.",
        "logo_url": "https://logo.clearbit.com/adobe.com",
        "market_cap": 240000000000.0,
    },
    {
        "symbol": "AMD",
        "company_name": "Advanced Micro Devices Inc.",
        "sector": "Technology",
        "industry": "Semiconductors",
        "exchange": "NASDAQ",
        "currency": "USD",
        "description": "AMD produces computer processors, microprocessors, and graphics processors.",
        "logo_url": "https://logo.clearbit.com/amd.com",
        "market_cap": 230000000000.0,
    },
    {
        "symbol": "INTC",
        "company_name": "Intel Corporation",
        "sector": "Technology",
        "industry": "Semiconductors",
        "exchange": "NASDAQ",
        "currency": "USD",
        "description": "Intel Corporation designs and manufactures semiconductor microprocessors and chipsets.",
        "logo_url": "https://logo.clearbit.com/intel.com",
        "market_cap": 95000000000.0,
    },
]


async def get_stock_by_symbol(db: AsyncSession, symbol: str) -> Optional[Stock]:
    """Retrieve a single stock record by its ticker symbol (case-insensitive)."""
    stmt = select(Stock).where(func.upper(Stock.symbol) == symbol.strip().upper())
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_stock_by_id(db: AsyncSession, stock_id: UUID) -> Optional[Stock]:
    """Retrieve a single stock record by its UUID primary key."""
    stmt = select(Stock).where(Stock.id == stock_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_stock(db: AsyncSession, stock_in: StockCreate) -> Stock:
    """
    Create a new stock in catalog.
    Raises ConflictException if symbol already exists.
    """
    existing = await get_stock_by_symbol(db, stock_in.symbol)
    if existing:
        raise ConflictException(f"Stock with symbol '{stock_in.symbol.upper()}' already exists")

    stock = Stock(
        symbol=stock_in.symbol.strip().upper(),
        company_name=stock_in.company_name.strip(),
        sector=stock_in.sector.strip(),
        industry=stock_in.industry.strip() if stock_in.industry else None,
        exchange=stock_in.exchange.strip().upper(),
        currency=stock_in.currency.strip().upper(),
        description=stock_in.description,
        logo_url=stock_in.logo_url,
        market_cap=stock_in.market_cap,
        is_active=stock_in.is_active,
    )
    db.add(stock)
    await db.commit()
    await db.refresh(stock)
    logger.info("Created new stock: %s (%s)", stock.symbol, stock.company_name)
    return stock


async def update_stock(db: AsyncSession, symbol: str, stock_in: StockUpdate) -> Stock:
    """
    Update an existing stock attributes by symbol.
    Raises NotFoundException if symbol is not found.
    """
    stock = await get_stock_by_symbol(db, symbol)
    if not stock:
        raise NotFoundException(f"Stock with symbol '{symbol.upper()}' not found")

    update_data = stock_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            if field in ("sector", "exchange", "currency") and isinstance(value, str):
                setattr(stock, field, value.strip())
            else:
                setattr(stock, field, value)

    await db.commit()
    await db.refresh(stock)
    logger.info("Updated stock: %s", stock.symbol)
    return stock


async def list_stocks(
    db: AsyncSession,
    q: Optional[str] = None,
    sector: Optional[str] = None,
    exchange: Optional[str] = None,
    sort_by: str = "symbol",
    order: str = "asc",
    page: int = 1,
    page_size: int = 10,
    is_active_only: bool = True,
) -> Tuple[List[Stock], int]:
    """
    List stocks with search filter, sector filter, exchange filter, sorting, and pagination.
    Returns (stocks_list, total_count).
    """
    query = select(Stock)

    if is_active_only:
        query = query.where(Stock.is_active.is_(True))

    if q:
        search_pattern = f"%{q.strip()}%"
        query = query.where(
            or_(
                Stock.symbol.ilike(search_pattern),
                Stock.company_name.ilike(search_pattern),
            )
        )

    if sector:
        query = query.where(Stock.sector.ilike(f"%{sector.strip()}%"))

    if exchange:
        query = query.where(Stock.exchange.ilike(f"%{exchange.strip()}%"))

    # Count matching total records
    count_stmt = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    # Sorting logic
    sort_column_map = {
        "symbol": Stock.symbol,
        "company_name": Stock.company_name,
        "sector": Stock.sector,
        "exchange": Stock.exchange,
        "market_cap": Stock.market_cap,
        "created_at": Stock.created_at,
    }
    sort_column = sort_column_map.get(sort_by.lower(), Stock.symbol)
    sort_order = desc(sort_column) if order.lower() == "desc" else asc(sort_column)

    query = query.order_by(sort_order)

    # Pagination offset & limit
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    stocks = list(result.scalars().all())

    return stocks, total


async def seed_popular_stocks(db: AsyncSession) -> int:
    """
    Seed popular stock records if they do not already exist.
    Returns count of new stocks created.
    """
    created_count = 0
    for stock_data in POPULAR_STOCKS_SEED:
        existing = await get_stock_by_symbol(db, stock_data["symbol"])
        if not existing:
            stock = Stock(**stock_data)
            db.add(stock)
            created_count += 1

    if created_count > 0:
        await db.commit()
        logger.info("Seeded %d popular stocks into database", created_count)

    return created_count
