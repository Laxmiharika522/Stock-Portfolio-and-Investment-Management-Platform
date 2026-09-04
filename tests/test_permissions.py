"""
Permission & Ownership Isolation Tests — Day 4
Ensures strict multi-tenant data isolation: User A cannot read, update, or delete User B's resources.
"""

import pytest
from httpx import AsyncClient
from app.models.user import User


@pytest.mark.asyncio
async def test_unauthenticated_access_rejected(async_client: AsyncClient):
    """Verify endpoints return 401 Unauthorized when missing Authorization header."""
    res_list = await async_client.get("/api/v1/portfolios")
    assert res_list.status_code == 401

    res_me = await async_client.get("/api/v1/users/me")
    assert res_me.status_code == 401


@pytest.mark.asyncio
async def test_user_b_cannot_get_user_a_portfolio(
    async_client: AsyncClient,
    user_a: User,
    user_b: User,
    token_user_a: str,
    token_user_b: str,
):
    """User A creates a portfolio; User B attempts to access it -> 403 Forbidden."""
    headers_a = {"Authorization": f"Bearer {token_user_a}"}
    headers_b = {"Authorization": f"Bearer {token_user_b}"}

    # 1. User A creates portfolio
    create_res = await async_client.post(
        "/api/v1/portfolios",
        json={"name": "User A Secret Vault", "currency": "USD"},
        headers=headers_a,
    )
    assert create_res.status_code == 201
    portfolio_id = create_res.json()["id"]

    # 2. User B tries to read User A's portfolio
    get_res = await async_client.get(f"/api/v1/portfolios/{portfolio_id}", headers=headers_b)
    assert get_res.status_code == 403
    assert get_res.json()["error"]["code"] == "FORBIDDEN"


@pytest.mark.asyncio
async def test_user_b_cannot_update_user_a_portfolio(
    async_client: AsyncClient,
    user_a: User,
    user_b: User,
    token_user_a: str,
    token_user_b: str,
):
    """User A creates a portfolio; User B attempts to update it -> 403 Forbidden."""
    headers_a = {"Authorization": f"Bearer {token_user_a}"}
    headers_b = {"Authorization": f"Bearer {token_user_b}"}

    # 1. User A creates portfolio
    create_res = await async_client.post(
        "/api/v1/portfolios",
        json={"name": "User A Holdings", "currency": "USD"},
        headers=headers_a,
    )
    assert create_res.status_code == 201
    portfolio_id = create_res.json()["id"]

    # 2. User B tries to update User A's portfolio
    update_res = await async_client.put(
        f"/api/v1/portfolios/{portfolio_id}",
        json={"name": "Hacked Name"},
        headers=headers_b,
    )
    assert update_res.status_code == 403
    assert update_res.json()["error"]["code"] == "FORBIDDEN"


@pytest.mark.asyncio
async def test_user_b_cannot_delete_user_a_portfolio(
    async_client: AsyncClient,
    user_a: User,
    user_b: User,
    token_user_a: str,
    token_user_b: str,
):
    """User A creates a portfolio; User B attempts to delete it -> 403 Forbidden."""
    headers_a = {"Authorization": f"Bearer {token_user_a}"}
    headers_b = {"Authorization": f"Bearer {token_user_b}"}

    # 1. User A creates portfolio
    create_res = await async_client.post(
        "/api/v1/portfolios",
        json={"name": "User A Delete Target", "currency": "USD"},
        headers=headers_a,
    )
    assert create_res.status_code == 201
    portfolio_id = create_res.json()["id"]

    # 2. User B tries to delete User A's portfolio
    delete_res = await async_client.delete(
        f"/api/v1/portfolios/{portfolio_id}",
        headers=headers_b,
    )
    assert delete_res.status_code == 403
    assert delete_res.json()["error"]["code"] == "FORBIDDEN"


@pytest.mark.asyncio
async def test_user_b_cannot_list_user_a_portfolios(
    async_client: AsyncClient,
    user_a: User,
    user_b: User,
    token_user_b: str,
):
    """User B attempts to list User A's portfolios using ?user_id query param -> 403 Forbidden."""
    headers_b = {"Authorization": f"Bearer {token_user_b}"}

    list_res = await async_client.get(
        f"/api/v1/portfolios?user_id={user_a.id}",
        headers=headers_b,
    )
    assert list_res.status_code == 403
    assert list_res.json()["error"]["code"] == "FORBIDDEN"
