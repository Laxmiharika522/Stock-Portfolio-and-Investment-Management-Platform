import asyncio
import httpx
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"

async def run_demo():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # 1. Check health
        logger.info("Checking API Health...")
        response = await client.get("/health")
        logger.info(f"Health Check Response: {response.status_code}")

        # 2. Register user
        logger.info("\nRegistering a new user...")
        user_data = {
            "email": "demo_user@example.com",
            "username": "demo_user",
            "password": "Password123!",
            "full_name": "Demo User"
        }
        # Try to register, ignore 409 if already exists
        response = await client.post("/api/v1/auth/register", json=user_data)
        if response.status_code not in (201, 409):
            logger.error(f"Failed to register user: {response.text}")
            return
        
        # 3. Login
        logger.info("\nLogging in...")
        login_data = {
            "username_or_email": "demo_user",
            "password": "Password123!"
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        if response.status_code != 200:
            logger.error(f"Failed to login: {response.text}")
            return
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        logger.info("Successfully logged in.")

        # 4. Get default portfolio
        logger.info("\nGetting user portfolios...")
        response = await client.get("/api/v1/portfolios", headers=headers)
        portfolios = response.json()
        if not portfolios:
            logger.info("No portfolio found. Creating one...")
            portfolio_data = {
                "name": "My Primary Portfolio",
                "currency": "USD"
            }
            response = await client.post("/api/v1/portfolios", json=portfolio_data, headers=headers)
            if response.status_code != 201:
                logger.error(f"Failed to create portfolio: {response.text}")
                return
            portfolio_id = response.json()["id"]
        else:
            portfolio_id = portfolios[0]["id"]
            
        logger.info(f"Using portfolio ID: {portfolio_id}")

        # 5. Deposit cash
        logger.info("\nDepositing $10,000 cash...")
        deposit_data = {"amount": 10000}
        response = await client.post(f"/api/v1/portfolios/{portfolio_id}/deposit", json=deposit_data, headers=headers)
        logger.info(f"Deposit response: {response.status_code}")

        # 6. View available stocks
        logger.info("\nFetching available stocks...")
        response = await client.get("/api/v1/stocks?page_size=5")
        stocks = response.json().get("items", [])
        if not stocks:
            logger.error("No stocks available in catalog. Did you seed them?")
            return
        stock_symbol = stocks[0]["symbol"]
        logger.info(f"Selected stock to trade: {stock_symbol}")

        # 7. Buy stock
        logger.info(f"\nBuying 10 shares of {stock_symbol}...")
        buy_data = {
            "stock_symbol": stock_symbol,
            "transaction_type": "BUY",
            "quantity": 10,
            "price_per_share": 150.0
        }
        response = await client.post(f"/api/v1/portfolios/{portfolio_id}/transactions", json=buy_data, headers=headers)
        logger.info(f"Buy Response: {response.status_code} - {response.text}")

        # 8. Check holdings
        logger.info("\nChecking portfolio holdings...")
        response = await client.get(f"/api/v1/portfolios/{portfolio_id}/holdings", headers=headers)
        holdings = response.json()
        logger.info(f"Holdings: {holdings}")

        # 9. Sell stock
        logger.info(f"\nSelling 5 shares of {stock_symbol}...")
        sell_data = {
            "stock_symbol": stock_symbol,
            "transaction_type": "SELL",
            "quantity": 5,
            "price_per_share": 160.0
        }
        response = await client.post(f"/api/v1/portfolios/{portfolio_id}/transactions", json=sell_data, headers=headers)
        logger.info(f"Sell Response: {response.status_code} - {response.text}")

        # 10. Check transactions history
        logger.info("\nChecking transaction history...")
        response = await client.get(f"/api/v1/portfolios/{portfolio_id}/transactions", headers=headers)
        history = response.json().get("items", [])
        logger.info(f"Total transactions: {len(history)}")

        logger.info("\n=== Demo Complete ===")

if __name__ == "__main__":
    asyncio.run(run_demo())
