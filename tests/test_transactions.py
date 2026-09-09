"""
Transaction Tests — Day 6
Tests for BUY/SELL trade execution, cash deposit, balance validation,
insufficient funds, insufficient shares, history listing, and authorization.
"""

from __future__ import annotations

import uuid
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portfolio import Portfolio
from app.models.stock import Stock
from app.models.user import User


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest_asyncio.fixture
async def portfolio_a(db_session: AsyncSession, user_a: User) -> Portfolio:
    """Portfolio belonging to user A with zero balance."""
    p = Portfolio(
        user_id=user_a.id,
        name=f"Portfolio {uuid.uuid4().hex[:6]}",
        currency="USD",
        is_default=False,
        cash_balance=0.0,
        total_invested=0.0,
    )
    db_session.add(p)
    await db_session.commit()
    await db_session.refresh(p)
    return p


@pytest_asyncio.fixture
async def sample_stock(db_session: AsyncSession) -> Stock:
    """A sample stock with a unique symbol for each test to avoid UNIQUE constraint issues."""
    unique_symbol = f"TST{uuid.uuid4().hex[:4].upper()}"
    stock = Stock(
        symbol=unique_symbol,
        company_name=f"Test Corp {unique_symbol}",
        sector="Technology",
        exchange="NASDAQ",
        currency="USD",
        is_active=True,
    )
    db_session.add(stock)
    await db_session.commit()
    await db_session.refresh(stock)
    return stock


# ── Helper ────────────────────────────────────────────────────────────────────

def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ── Deposit Tests ─────────────────────────────────────────────────────────────

class TestDeposit:

    @pytest.mark.asyncio
    async def test_deposit_success(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        token_user_a: str,
    ):
        """Depositing cash should increase portfolio cash_balance."""
        response = await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/deposit",
            json={"amount": 50000.0, "notes": "Initial funding"},
            headers=auth_header(token_user_a),
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["amount_deposited"] == 50000.0
        assert data["portfolio_balance"]["cash_balance"] == 50000.0
        assert "Successfully deposited" in data["message"]

    @pytest.mark.asyncio
    async def test_deposit_invalid_amount_zero(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        token_user_a: str,
    ):
        """Deposit of 0 should be rejected by schema validation."""
        response = await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/deposit",
            json={"amount": 0},
            headers=auth_header(token_user_a),
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_deposit_unauthorized(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
    ):
        """Deposit without auth token should return 401/403."""
        response = await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/deposit",
            json={"amount": 1000.0},
        )
        assert response.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_deposit_wrong_user(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        token_user_b: str,
    ):
        """User B cannot deposit into User A's portfolio."""
        response = await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/deposit",
            json={"amount": 1000.0},
            headers=auth_header(token_user_b),
        )
        assert response.status_code == 403


# ── BUY Transaction Tests ─────────────────────────────────────────────────────

class TestBuyTransaction:

    @pytest.mark.asyncio
    async def test_buy_success(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        sample_stock: Stock,
        token_user_a: str,
    ):
        """Fund portfolio, then execute a BUY trade successfully."""
        # Fund portfolio first
        deposit_resp = await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/deposit",
            json={"amount": 10000.0},
            headers=auth_header(token_user_a),
        )
        assert deposit_resp.status_code == 200

        # Execute BUY: 10 shares @ $150 = $1500 + $2 fee = $1502
        response = await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            json={
                "stock_symbol": sample_stock.symbol,
                "transaction_type": "BUY",
                "quantity": 10.0,
                "price_per_share": 150.0,
                "fees": 2.0,
            },
            headers=auth_header(token_user_a),
        )
        assert response.status_code == 201, response.text
        data = response.json()

        tx = data["transaction"]
        assert tx["transaction_type"] == "BUY"
        assert tx["quantity"] == 10.0
        assert tx["price_per_share"] == 150.0
        assert tx["total_amount"] == 1502.0  # gross + fees
        assert tx["stock"]["symbol"] == sample_stock.symbol

        balance = data["portfolio_balance"]
        assert balance["cash_balance"] == pytest.approx(10000.0 - 1502.0, abs=0.01)
        assert balance["total_invested"] == pytest.approx(1500.0, abs=0.01)

    @pytest.mark.asyncio
    async def test_buy_insufficient_funds(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        sample_stock: Stock,
        token_user_a: str,
    ):
        """BUY when portfolio has no / insufficient cash should return 400 INSUFFICIENT_FUNDS."""
        # portfolio_a starts with 0 cash (fresh fixture), so any BUY should fail
        response = await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            json={
                "stock_symbol": sample_stock.symbol,
                "transaction_type": "BUY",
                "quantity": 1.0,
                "price_per_share": 99999.0,
                "fees": 0.0,
            },
            headers=auth_header(token_user_a),
        )
        assert response.status_code == 400
        body = response.json()
        assert body["error"]["code"] == "INSUFFICIENT_FUNDS"

    @pytest.mark.asyncio
    async def test_buy_invalid_stock_symbol(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        token_user_a: str,
    ):
        """BUY with unknown stock symbol should return 404."""
        # Fund first so it doesn't fail on balance
        await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/deposit",
            json={"amount": 10000.0},
            headers=auth_header(token_user_a),
        )
        response = await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            json={
                "stock_symbol": "DOESNOTEXIST",
                "transaction_type": "BUY",
                "quantity": 1.0,
                "price_per_share": 100.0,
            },
            headers=auth_header(token_user_a),
        )
        assert response.status_code == 404
        body = response.json()
        assert body["error"]["code"] == "NOT_FOUND"


# ── SELL Transaction Tests ────────────────────────────────────────────────────

class TestSellTransaction:

    @pytest.mark.asyncio
    async def test_sell_success(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        sample_stock: Stock,
        token_user_a: str,
    ):
        """BUY shares first, then SELL some — balance should increase after SELL."""
        headers = auth_header(token_user_a)

        # Fund + BUY 20 shares @ $100
        await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/deposit",
            json={"amount": 5000.0},
            headers=headers,
        )
        await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            json={
                "stock_symbol": sample_stock.symbol,
                "transaction_type": "BUY",
                "quantity": 20.0,
                "price_per_share": 100.0,
                "fees": 0.0,
            },
            headers=headers,
        )

        # SELL 5 shares @ $110 = $550 - $1 fee = $549 net proceeds
        response = await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            json={
                "stock_symbol": sample_stock.symbol,
                "transaction_type": "SELL",
                "quantity": 5.0,
                "price_per_share": 110.0,
                "fees": 1.0,
            },
            headers=headers,
        )
        assert response.status_code == 201, response.text
        data = response.json()

        tx = data["transaction"]
        assert tx["transaction_type"] == "SELL"
        assert tx["total_amount"] == pytest.approx(549.0, abs=0.01)  # 550 - 1 fee

    @pytest.mark.asyncio
    async def test_sell_insufficient_shares(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        sample_stock: Stock,
        token_user_a: str,
    ):
        """Selling more shares than owned should return 400 INSUFFICIENT_SHARES."""
        headers = auth_header(token_user_a)

        # Fund + BUY 2 shares
        await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/deposit",
            json={"amount": 1000.0},
            headers=headers,
        )
        await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            json={
                "stock_symbol": sample_stock.symbol,
                "transaction_type": "BUY",
                "quantity": 2.0,
                "price_per_share": 100.0,
            },
            headers=headers,
        )

        # Try selling 100 shares (only own 2)
        response = await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            json={
                "stock_symbol": sample_stock.symbol,
                "transaction_type": "SELL",
                "quantity": 100.0,
                "price_per_share": 100.0,
            },
            headers=headers,
        )
        assert response.status_code == 400
        body = response.json()
        assert body["error"]["code"] == "INSUFFICIENT_SHARES"
        assert "owned_quantity" in body["error"]["details"]

    @pytest.mark.asyncio
    async def test_sell_with_no_holdings(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        sample_stock: Stock,
        token_user_a: str,
    ):
        """SELL without any prior BUY should return 400 INSUFFICIENT_SHARES."""
        response = await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            json={
                "stock_symbol": sample_stock.symbol,
                "transaction_type": "SELL",
                "quantity": 1.0,
                "price_per_share": 100.0,
            },
            headers=auth_header(token_user_a),
        )
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "INSUFFICIENT_SHARES"


# ── Transaction History Tests ─────────────────────────────────────────────────

class TestTransactionHistory:

    @pytest.mark.asyncio
    async def test_list_transactions(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        sample_stock: Stock,
        token_user_a: str,
    ):
        """Transaction list should return paginated results with correct structure."""
        headers = auth_header(token_user_a)

        # Fund and make a trade
        await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/deposit",
            json={"amount": 5000.0},
            headers=headers,
        )
        await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            json={
                "stock_symbol": sample_stock.symbol,
                "transaction_type": "BUY",
                "quantity": 5.0,
                "price_per_share": 100.0,
            },
            headers=headers,
        )

        response = await async_client.get(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            headers=headers,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "total_pages" in data
        assert data["total"] >= 1
        # Each item should have transaction_type
        for item in data["items"]:
            assert item["transaction_type"] in ("BUY", "SELL")

    @pytest.mark.asyncio
    async def test_list_transactions_filter_by_type(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        token_user_a: str,
    ):
        """Filtering by BUY should only return BUY transactions."""
        response = await async_client.get(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            params={"transaction_type": "BUY"},
            headers=auth_header(token_user_a),
        )
        assert response.status_code == 200
        data = response.json()
        for item in data["items"]:
            assert item["transaction_type"] == "BUY"

    @pytest.mark.asyncio
    async def test_get_transaction_detail(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        sample_stock: Stock,
        token_user_a: str,
    ):
        """Fetching a single transaction by ID should return full details."""
        headers = auth_header(token_user_a)

        # Ensure funds exist
        await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/deposit",
            json={"amount": 2000.0},
            headers=headers,
        )
        create_resp = await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            json={
                "stock_symbol": sample_stock.symbol,
                "transaction_type": "BUY",
                "quantity": 3.0,
                "price_per_share": 200.0,
            },
            headers=headers,
        )
        assert create_resp.status_code == 201
        tx_id = create_resp.json()["transaction"]["id"]

        detail_resp = await async_client.get(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions/{tx_id}",
            headers=headers,
        )
        assert detail_resp.status_code == 200
        detail = detail_resp.json()
        assert detail["id"] == tx_id
        assert detail["quantity"] == 3.0

    @pytest.mark.asyncio
    async def test_get_nonexistent_transaction(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        token_user_a: str,
    ):
        """Fetching a transaction with a random UUID should return 404."""
        response = await async_client.get(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions/{uuid.uuid4()}",
            headers=auth_header(token_user_a),
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_transactions_wrong_user(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        token_user_b: str,
    ):
        """User B should not be able to see User A's transaction history."""
        response = await async_client.get(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            headers=auth_header(token_user_b),
        )
        assert response.status_code == 403


# ── Holdings Tests ────────────────────────────────────────────────────────────

class TestHoldings:

    @pytest.mark.asyncio
    async def test_get_holdings_success(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        sample_stock: Stock,
        token_user_a: str,
        monkeypatch
    ):
        async def mock_get_live_quote(symbol):
            return {"symbol": symbol, "price": 200.0}
            
        from app.services.market_data_service import market_data_service
        monkeypatch.setattr(market_data_service, "get_live_quote", mock_get_live_quote)

        headers = auth_header(token_user_a)

        # 1. Deposit funds
        await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/deposit",
            json={"amount": 10000.0},
            headers=headers,
        )

        # 2. BUY 10 shares @ 100
        await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            json={
                "stock_symbol": sample_stock.symbol,
                "transaction_type": "BUY",
                "quantity": 10.0,
                "price_per_share": 100.0,
            },
            headers=headers,
        )

        # 3. BUY 10 shares @ 150
        await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            json={
                "stock_symbol": sample_stock.symbol,
                "transaction_type": "BUY",
                "quantity": 10.0,
                "price_per_share": 150.0,
            },
            headers=headers,
        )

        # 4. SELL 5 shares @ 200
        await async_client.post(
            f"/api/v1/portfolios/{portfolio_a.id}/transactions",
            json={
                "stock_symbol": sample_stock.symbol,
                "transaction_type": "SELL",
                "quantity": 5.0,
                "price_per_share": 200.0,
            },
            headers=headers,
        )

        response = await async_client.get(
            f"/api/v1/portfolios/{portfolio_a.id}/holdings",
            headers=headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        
        holding = data[0]
        assert holding["stock_symbol"] == sample_stock.symbol
        assert holding["quantity"] == 15.0
        assert holding["weighted_average_buy_price"] == 125.0
        assert holding["current_price"] == 200.0
        assert holding["total_value"] == 3000.0
        assert holding["unrealized_pnl"] == 1125.0

    @pytest.mark.asyncio
    async def test_get_holdings_wrong_user(
        self,
        async_client: AsyncClient,
        portfolio_a: Portfolio,
        token_user_b: str,
    ):
        """User B should not be able to see User A's holdings."""
        response = await async_client.get(
            f"/api/v1/portfolios/{portfolio_a.id}/holdings",
            headers=auth_header(token_user_b),
        )
        assert response.status_code == 403
