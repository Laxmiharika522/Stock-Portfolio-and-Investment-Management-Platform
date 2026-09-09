from fastapi import APIRouter, Path
from app.schemas.market import MarketQuoteOut
from app.services.market_data_service import market_data_service

router = APIRouter(prefix="/market", tags=["Market Data"])

@router.get(
    "/quote/{symbol}",
    response_model=MarketQuoteOut,
    summary="Get Live Stock Quote",
    description="Fetches a live market quote for a given stock symbol from Alpha Vantage (or mock fallback)."
)
async def get_live_quote(
    symbol: str = Path(..., min_length=1, max_length=20, description="The stock ticker symbol")
):
    """
    Get live market data (price, change, percentage change) for a specific symbol.
    Caches responses to prevent rate limit exhaustion.
    """
    quote = await market_data_service.get_live_quote(symbol)
    return quote
