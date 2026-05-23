import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRegister:
    async def test_register_success(self, client: AsyncClient):
        response = await client.post(
            "/auth/register",
            json={"email": "newuser@example.com", "password": "securepass123"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "created_at" in data

    async def test_register_duplicate_email(self, client: AsyncClient):
        await client.post(
            "/auth/register",
            json={"email": "dup@example.com", "password": "securepass123"},
        )
        response = await client.post(
            "/auth/register",
            json={"email": "dup@example.com", "password": "securepass123"},
        )
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"].lower()

    async def test_register_weak_password(self, client: AsyncClient):
        response = await client.post(
            "/auth/register",
            json={"email": "weak@example.com", "password": "12345"},
        )
        assert response.status_code == 422


@pytest.mark.asyncio
class TestLogin:
    async def test_login_success(self, client: AsyncClient, test_user: dict):
        response = await client.post(
            "/auth/login",
            json={
                "email": test_user["email"],
                "password": test_user["password"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["token_type"] == "bearer"
        assert "access_token" in data
        assert "refresh_token" in data
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies

    async def test_login_wrong_password(self, client: AsyncClient, test_user: dict):
        response = await client.post(
            "/auth/login",
            json={"email": test_user["email"], "password": "wrongpass"},
        )
        assert response.status_code == 401

    async def test_login_wrong_email(self, client: AsyncClient):
        response = await client.post(
            "/auth/login",
            json={"email": "nonexistent@example.com", "password": "somepass"},
        )
        assert response.status_code == 401


@pytest.mark.asyncio
class TestMe:
    async def test_me_authenticated(self, auth_client: AsyncClient, test_user: dict):
        response = await auth_client.get("/auth/me")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user["email"]
        assert data["id"] == test_user["id"]

    async def test_me_unauthenticated(self, client: AsyncClient):
        response = await client.get("/auth/me")
        assert response.status_code == 401


@pytest.mark.asyncio
class TestRefresh:
    async def test_refresh_success(self, auth_client: AsyncClient):
        response = await auth_client.post("/auth/refresh")
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    async def test_refresh_missing_token(self, client: AsyncClient):
        response = await client.post("/auth/refresh")
        assert response.status_code == 401
        assert "missing" in response.json()["detail"].lower()
