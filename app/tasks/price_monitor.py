"""
Price Monitor Background Task — Day 9
Routinely checks watchlist items against live market data to see if target prices have been reached.
"""

import logging
from sqlalchemy import select, update
from app.db.session import AsyncSessionLocal
from app.models.watchlist import Watchlist, AlertType
from app.services.market_data_service import market_data_service

logger = logging.getLogger(__name__)

async def check_watchlist_prices():
    """
    Check all untriggered watchlist items to see if their target prices have been hit.
    Marks them as triggered if so.
    """
    logger.info("Starting watchlist price monitor task...")
    
    try:
        async with AsyncSessionLocal() as db:
            # Get all untriggered watchlists that have a target price
            stmt = (
                select(Watchlist)
                .where(Watchlist.is_triggered == False)
                .where(Watchlist.target_price.isnot(None))
            )
            result = await db.execute(stmt)
            watchlists = result.scalars().all()
            
            if not watchlists:
                logger.info("No active watchlist alerts to check.")
                return

            # Group by stock_id to minimize API calls
            stock_ids = {w.stock_id for w in watchlists}
            
            # We need symbols to query market data, so we need to join or fetch stocks
            from app.models.stock import Stock
            
            stock_stmt = select(Stock).where(Stock.id.in_(stock_ids))
            stock_result = await db.execute(stock_stmt)
            stocks = stock_result.scalars().all()
            stock_map = {s.id: s.symbol for s in stocks}

            triggered_count = 0
            from datetime import datetime, timezone

            for w in watchlists:
                symbol = stock_map.get(w.stock_id)
                if not symbol:
                    continue
                
                quote = await market_data_service.get_live_quote(symbol)
                current_price = quote.get("price")
                
                if not current_price:
                    continue
                
                current_price_decimal = current_price
                target_decimal = w.target_price

                triggered = False
                
                if w.alert_type == AlertType.ABOVE and current_price_decimal >= target_decimal:
                    triggered = True
                elif w.alert_type == AlertType.BELOW and current_price_decimal <= target_decimal:
                    triggered = True
                    
                if triggered:
                    w.is_triggered = True
                    w.triggered_at = datetime.now(timezone.utc)
                    triggered_count += 1
                    logger.info(f"Alert triggered for user {w.user_id} on {symbol}: price {current_price_decimal} is {w.alert_type} target {target_decimal}")
                    
                    from app.services.notification_service import NotificationService
                    from app.models.notification import NotificationType
                    await NotificationService.create_notification(
                        db=db,
                        user_id=w.user_id,
                        type=NotificationType.PRICE_ALERT,
                        title=f"Price Alert: {symbol}",
                        message=f"{symbol} has reached your target price of ${target_decimal}. Current price is ${current_price_decimal}.",
                        related_stock_id=w.stock_id,
                    )

            if triggered_count > 0:
                await db.commit()
                
            logger.info(f"Watchlist price monitor task completed. {triggered_count} alerts triggered.")
    except Exception as e:
        logger.error(f"Error in price monitor task: {e}", exc_info=True)
