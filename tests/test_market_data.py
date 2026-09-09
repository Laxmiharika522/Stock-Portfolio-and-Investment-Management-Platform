import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from app.services.market_data_service import market_data_service

@pytest.mark.asyncio
async def test_get_live_quote_mock_fallback(async_client: AsyncClient):
    """Test the fallback mock mechanism in MarketDataService when API key is demo."""
    quote = await market_data_service.get_live_quote("AAPL")
    assert quote["symbol"] == "AAPL"
    assert "price" in quote
    assert "change" in quote
    assert "change_percent" in quote
    assert quote["latest_trading_day"] == "2026-09-09"

@pytest.mark.asyncio
async def test_market_quote_api_endpoint(async_client: AsyncClient, monkeypatch):
    """Test the /market/quote/{symbol} endpoint."""
    async def mock_quote(symbol):
        return {
            "symbol": symbol.upper(),
            "price": 150.0,
            "change": 2.5,
            "change_percent": 1.6,
            "latest_trading_day": "2026-09-09"
        }
    
    monkeypatch.setattr(market_data_service, "get_live_quote", mock_quote)
    
    response = await async_client.get("/api/v1/market/quote/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["price"] == 150.0
    assert data["change"] == 2.5
