"""
Stock API Test Suite — Day 5
Validates stock catalog listing, search, sector filtering, pagination, ticker lookup, and admin role authorization controls.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_seed_and_list_stocks(async_client: AsyncClient, token_admin: str):
    """Test seeding stocks catalog and listing with pagination."""
    # Seed stocks via admin endpoint
    seed_res = await async_client.post(
        "/api/v1/stocks/seed",
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    assert seed_res.status_code == 200
    assert "created_count" in seed_res.json()

    # List stocks (default page 1, size 10)
    response = await async_client.get("/api/v1/stocks")
    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data
    assert data["total"] >= 20
    assert len(data["items"]) == 10
    assert data["page"] == 1
    assert data["page_size"] == 10


@pytest.mark.asyncio
async def test_stock_search_and_filter(async_client: AsyncClient, token_admin: str):
    """Test stock search query and sector filter."""
    # Seed catalog
    await async_client.post(
        "/api/v1/stocks/seed",
        headers={"Authorization": f"Bearer {token_admin}"},
    )

    # Search for "Apple"
    res = await async_client.get("/api/v1/stocks?q=Apple")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 1
    assert any(item["symbol"] == "AAPL" for item in data["items"])

    # Filter by sector Technology
    res_tech = await async_client.get("/api/v1/stocks?sector=Technology")
    assert res_tech.status_code == 200
    tech_data = res_tech.json()
    assert tech_data["total"] > 0
    assert all("Technology" in item["sector"] for item in tech_data["items"])


@pytest.mark.asyncio
async def test_get_stock_by_symbol(async_client: AsyncClient, token_admin: str):
    """Test fetching stock detail by case-insensitive symbol."""
    await async_client.post(
        "/api/v1/stocks/seed",
        headers={"Authorization": f"Bearer {token_admin}"},
    )

    # Lowercase ticker lookup
    res = await async_client.get("/api/v1/stocks/aapl")
    assert res.status_code == 200
    stock = res.json()
    assert stock["symbol"] == "AAPL"
    assert stock["company_name"] == "Apple Inc."

    # Non-existent ticker lookup
    res_404 = await async_client.get("/api/v1/stocks/INVALIDSYM999")
    assert res_404.status_code == 404
    assert res_404.json()["error"]["message"] == "Stock ticker symbol 'INVALIDSYM999' was not found in catalog"


@pytest.mark.asyncio
async def test_admin_create_stock_success(async_client: AsyncClient, token_admin: str):
    """Test creating a new stock with admin privileges."""
    payload = {
        "symbol": "GOOG",
        "company_name": "Alphabet Inc. Class C",
        "sector": "Communication Services",
        "industry": "Internet Content & Information",
        "exchange": "NASDAQ",
        "currency": "USD",
        "description": "Alphabet Inc. Class C stock",
        "market_cap": 2100000000000.0,
    }
    response = await async_client.post(
        "/api/v1/stocks",
        json=payload,
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["symbol"] == "GOOG"
    assert data["company_name"] == "Alphabet Inc. Class C"


@pytest.mark.asyncio
async def test_create_stock_authorization_protection(async_client: AsyncClient, token_user_a: str):
    """Test that regular non-admin user is forbidden from creating stock (403 Forbidden)."""
    payload = {
        "symbol": "FAKE",
        "company_name": "Fake Company",
        "sector": "Technology",
        "exchange": "NASDAQ",
    }
    response = await async_client.post(
        "/api/v1/stocks",
        json=payload,
        headers={"Authorization": f"Bearer {token_user_a}"},
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ADMIN_REQUIRED"


@pytest.mark.asyncio
async def test_create_duplicate_stock_conflict(async_client: AsyncClient, token_admin: str):
    """Test creating duplicate stock symbol returns 409 Conflict."""
    payload = {
        "symbol": "DUPTICKER",
        "company_name": "Duplicate Company",
        "sector": "Finance",
        "exchange": "NYSE",
    }
    res1 = await async_client.post(
        "/api/v1/stocks",
        json=payload,
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    assert res1.status_code == 201

    # Attempt duplicate symbol insert
    res2 = await async_client.post(
        "/api/v1/stocks",
        json=payload,
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    assert res2.status_code == 409
    assert "already exists" in res2.json()["error"]["message"]


@pytest.mark.asyncio
async def test_admin_update_stock(async_client: AsyncClient, token_admin: str, token_user_a: str):
    """Test updating existing stock by admin vs forbidden non-admin."""
    # Create stock first
    payload = {
        "symbol": "UPDTICK",
        "company_name": "Original Name",
        "sector": "Technology",
        "exchange": "NASDAQ",
    }
    await async_client.post(
        "/api/v1/stocks",
        json=payload,
        headers={"Authorization": f"Bearer {token_admin}"},
    )

    # Regular user update -> 403 Forbidden
    res_user = await async_client.put(
        "/api/v1/stocks/UPDTICK",
        json={"company_name": "Hacked Name"},
        headers={"Authorization": f"Bearer {token_user_a}"},
    )
    assert res_user.status_code == 403
    assert res_user.json()["error"]["code"] == "ADMIN_REQUIRED"

    # Admin update -> 200 OK
    res_admin = await async_client.put(
        "/api/v1/stocks/UPDTICK",
        json={"company_name": "Updated Corp Name", "market_cap": 500000000.0},
        headers={"Authorization": f"Bearer {token_admin}"},
    )
    assert res_admin.status_code == 200
    updated_data = res_admin.json()
    assert updated_data["company_name"] == "Updated Corp Name"
    assert updated_data["market_cap"] == 500000000.0
