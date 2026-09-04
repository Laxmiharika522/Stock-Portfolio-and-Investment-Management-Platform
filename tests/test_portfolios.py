"""
Tests for Day 4 — Portfolio Model, Service & API Endpoints
Validates Portfolio CRUD operations and JWT-authenticated access.
"""

import pytest
from httpx import AsyncClient
from app.models.user import User


@pytest.mark.asyncio
async def test_create_and_list_portfolio(async_client: AsyncClient, user_a: User, token_user_a: str):
    """Verify creating a portfolio and retrieving user portfolios via authenticated API."""
    headers = {"Authorization": f"Bearer {token_user_a}"}

    # 1. Create Portfolio
    payload = {
        "name": "Tech Growth Fund",
        "description": "High yield tech stocks",
        "currency": "USD",
        "is_default": True
    }
    response = await async_client.post("/api/v1/portfolios", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Tech Growth Fund"
    assert data["currency"] == "USD"
    assert data["is_default"] is True
    assert data["user_id"] == str(user_a.id)
    portfolio_id = data["id"]

    # 2. List Portfolios
    list_resp = await async_client.get("/api/v1/portfolios", headers=headers)
    assert list_resp.status_code == 200
    portfolios = list_resp.json()
    assert len(portfolios) >= 1
    assert any(p["id"] == portfolio_id for p in portfolios)


@pytest.mark.asyncio
async def test_get_update_delete_portfolio(async_client: AsyncClient, user_a: User, token_user_a: str):
    """Verify GET, PUT, and DELETE on portfolio endpoints for owner user."""
    headers = {"Authorization": f"Bearer {token_user_a}"}

    # Create
    create_resp = await async_client.post(
        "/api/v1/portfolios",
        json={"name": "Crypto Reserve", "currency": "USD"},
        headers=headers,
    )
    assert create_resp.status_code == 201
    portfolio_id = create_resp.json()["id"]

    # Get Single
    get_resp = await async_client.get(f"/api/v1/portfolios/{portfolio_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Crypto Reserve"

    # Update
    update_resp = await async_client.put(
        f"/api/v1/portfolios/{portfolio_id}",
        json={"name": "Digital Assets Fund", "is_default": True},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Digital Assets Fund"
    assert update_resp.json()["is_default"] is True

    # Delete
    del_resp = await async_client.delete(f"/api/v1/portfolios/{portfolio_id}", headers=headers)
    assert del_resp.status_code in (200, 204)

    # Verify 404 after deletion
    get_again = await async_client.get(f"/api/v1/portfolios/{portfolio_id}", headers=headers)
    assert get_again.status_code == 404
