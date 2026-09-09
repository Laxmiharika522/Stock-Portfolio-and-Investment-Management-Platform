from pydantic import BaseModel, Field

class MarketQuoteOut(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    price: float = Field(..., description="Current price per share")
    change: float = Field(..., description="Price change today")
    change_percent: float = Field(..., description="Percentage price change today")
    latest_trading_day: str = Field(..., description="Date of the latest trading day")

    model_config = {
        "json_schema_extra": {
            "example": {
                "symbol": "AAPL",
                "price": 150.0,
                "change": 2.5,
                "change_percent": 1.6,
                "latest_trading_day": "2026-09-09"
            }
        }
    }
