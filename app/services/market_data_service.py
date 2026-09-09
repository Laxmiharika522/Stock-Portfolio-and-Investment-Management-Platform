import logging
import random
import httpx
from cachetools import TTLCache
from app.core.config import settings

logger = logging.getLogger(__name__)

class MarketDataService:
    def __init__(self):
        # Cache for market data: {symbol: quote_dict}
        self.cache = TTLCache(maxsize=1000, ttl=settings.MARKET_DATA_CACHE_TTL)
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = settings.ALPHA_VANTAGE_API_KEY

    async def get_live_quote(self, symbol: str) -> dict:
        symbol = symbol.upper()
        if symbol in self.cache:
            return self.cache[symbol]

        if not self.api_key or self.api_key == "demo":
            logger.info(f"Using demo key, returning mock quote for {symbol}")
            mocked = self._mock_quote(symbol)
            self.cache[symbol] = mocked
            return mocked

        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                # Check for rate limits
                if "Information" in data and "rate limit" in data["Information"].lower():
                    logger.warning(f"Alpha Vantage rate limit reached for {symbol}. Using fallback.")
                    mocked = self._mock_quote(symbol)
                    self.cache[symbol] = mocked
                    return mocked

                quote_data = data.get("Global Quote", {})
                if not quote_data or "05. price" not in quote_data:
                    logger.warning(f"Invalid quote data from Alpha Vantage for {symbol}: {data}")
                    mocked = self._mock_quote(symbol)
                    self.cache[symbol] = mocked
                    return mocked

                result = {
                    "symbol": quote_data.get("01. symbol", symbol),
                    "price": float(quote_data.get("05. price", 0.0)),
                    "change": float(quote_data.get("09. change", 0.0)),
                    "change_percent": float(quote_data.get("10. change percent", "0%").strip("%")),
                    "latest_trading_day": quote_data.get("07. latest trading day", "Unknown")
                }
                self.cache[symbol] = result
                return result

        except httpx.RequestError as e:
            logger.error(f"HTTP Request failed for {symbol}: {e}")
            return self._mock_quote(symbol)
        except ValueError as e:
            logger.error(f"Failed to parse quote for {symbol}: {e}")
            return self._mock_quote(symbol)

    def _mock_quote(self, symbol: str) -> dict:
        """Fallback mock quote for testing/rate-limits."""
        price = round(random.uniform(10.0, 500.0), 2)
        change = round(random.uniform(-5.0, 5.0), 2)
        return {
            "symbol": symbol.upper(),
            "price": price,
            "change": change,
            "change_percent": round((change / price) * 100, 2),
            "latest_trading_day": "2026-09-09"
        }

market_data_service = MarketDataService()
