"""
Auth & User API Tests — Day 3
Automated tests for user registration, authentication, JWT tokens, and user profile management.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

pytestmark = pytest.mark.asyncio


async def test_user_registration_and_login():
    """Test registering a new user and logging in to obtain JWT access token."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Register User
        reg_payload = {
            "email": "new.investor@example.com",
            "username": "newinvestor",
            "password": "Password123!",
            "full_name": "New Investor",
        }
        res_reg = await client.post("/api/v1/auth/register", json=reg_payload)
        assert res_reg.status_code == 201
        data_reg = res_reg.json()
        assert data_reg["email"] == "new.investor@example.com"
        assert data_reg["username"] == "newinvestor"

        # 2. Login User
        login_payload = {
            "username_or_email": "newinvestor",
            "password": "Password123!",
        }
        res_login = await client.post("/api/v1/auth/login", json=login_payload)
        assert res_login.status_code == 200
        data_login = res_login.json()
        assert "access_token" in data_login
        assert "refresh_token" in data_login
        token = data_login["access_token"]

        # 3. Access Protected /users/me endpoint
        headers = {"Authorization": f"Bearer {token}"}
        res_me = await client.get("/api/v1/users/me", headers=headers)
        assert res_me.status_code == 200
        data_me = res_me.json()
        assert data_me["username"] == "newinvestor"
        assert data_me["email"] == "new.investor@example.com"


async def test_invalid_login_credentials():
    """Test login with wrong password returns 401 Unauthorized."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "username_or_email": "nonexistent_user",
            "password": "WrongPassword123!",
        }
        response = await client.post("/api/v1/auth/login", json=payload)
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert data["error"]["code"] == "UNAUTHORIZED"


async def test_invalid_registration_input_returns_422():
    """Test registering with an invalid email returns 422 Unprocessable Entity with error details."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        invalid_payload = {
            "email": "not-an-email",
            "username": "us",  # too short (min 3)
            "password": "short",
        }
        response = await client.post("/api/v1/auth/register", json=invalid_payload)
        assert response.status_code == 422
        data = response.json()
        assert data["success"] is False
        assert data["error"]["code"] == "VALIDATION_ERROR"
        assert "details" in data["error"]
        assert len(data["error"]["details"]) >= 1


async def test_response_does_not_expose_internal_fields():
    """Verify that user endpoints do not expose internal sensitive fields like hashed_password."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        reg_payload = {
            "email": "privacy.user@example.com",
            "username": "privacyuser",
            "password": "SecurePassword123!",
            "full_name": "Privacy User",
        }
        res_reg = await client.post("/api/v1/auth/register", json=reg_payload)
        assert res_reg.status_code == 201
        data = res_reg.json()
        assert "hashed_password" not in data
        assert "password" not in data
        assert "id" in data
        assert "email" in data

