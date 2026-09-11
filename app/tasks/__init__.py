"""
Background Tasks Initialization
"""

from app.tasks.price_monitor import check_watchlist_prices

__all__ = ["check_watchlist_prices"]
