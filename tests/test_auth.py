import pytest
from httpx import AsyncClient

from app.utils.security import create_refresh_token


@pytest.mark.asyncio
class TestRegister:
    async def test_register_success(self, client: AsyncClient):
        response = await client.post(
            "/api/auth/register",
            json={"email": "newuser@example.com", "password": "securepass123"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "created_at" in data

    async def test_register_duplicate_email(self, client: AsyncClient):
        await client.post(
            "/api/auth/register",
            json={"email": "dup@example.com", "password": "securepass123"},
        )
        response = await client.post(
            "/api/auth/register",
            json={"email": "dup@example.com", "password": "securepass123"},
        )
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"].lower()

    async def test_register_weak_password(self, client: AsyncClient):
        response = await client.post(
            "/api/auth/register",
            json={"email": "weak@example.com", "password": "12345"},
        )
        assert response.status_code == 422




@pytest.mark.asyncio
class TestLogin:
    async def test_login_success(self, client: AsyncClient, test_user: dict):
        response = await client.post(
            "/api/auth/login",
            json={
                "email": test_user["email"],
                "password": test_user["password"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user["email"]
        assert "id" in data
        assert "created_at" in data
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies

    async def test_login_wrong_password(self, client: AsyncClient, test_user: dict):
        response = await client.post(
            "/api/auth/login",
            json={"email": test_user["email"], "password": "wrongpass"},
        )
        assert response.status_code == 401

    async def test_login_wrong_email(self, client: AsyncClient):
        response = await client.post(
            "/api/auth/login",
            json={"email": "nonexistent@example.com", "password": "somepass"},
        )
        assert response.status_code == 401


@pytest.mark.asyncio
class TestMe:
    async def test_me_authenticated(self, auth_client: AsyncClient, test_user: dict):
        response = await auth_client.get("/api/auth/me")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user["email"]
        assert data["id"] == test_user["id"]

    async def test_me_unauthenticated(self, client: AsyncClient):
        response = await client.get("/api/auth/me")
        assert response.status_code == 401


@pytest.mark.asyncio
class TestRefresh:
    async def test_refresh_success(self, auth_client: AsyncClient):
        response = await auth_client.post("/api/auth/refresh")
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True

    async def test_refresh_missing_token(self, client: AsyncClient):
        response = await client.post("/api/auth/refresh")
        assert response.status_code == 401
        assert "missing" in response.json()["detail"].lower()

    async def test_refresh_invalid_token(self, client: AsyncClient):
        client.cookies.set("refresh_token", "obviously-invalid-token")
        response = await client.post("/api/auth/refresh")
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    async def test_refresh_expired_token(self, client: AsyncClient):
        expired = create_refresh_token({"sub": "any"})
        # Override exp to be in the past
        from jose import jwt

        from app.config import ALGORITHM, JWT_AUDIENCE, SECRET_KEY

        payload = jwt.decode(
            expired, SECRET_KEY,
            algorithms=[ALGORITHM],
            audience=JWT_AUDIENCE,
        )
        payload["exp"] = 0
        tampered = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        client.cookies.set("refresh_token", tampered)
        response = await client.post("/api/auth/refresh")
        assert response.status_code == 401

    async def test_refresh_token_without_jti(self, client: AsyncClient):
        from jose import jwt

        from app.config import ALGORITHM, JWT_AUDIENCE, SECRET_KEY
        from app.utils.security import create_refresh_token

        token = create_refresh_token({"sub": "user-123"})
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM], audience=JWT_AUDIENCE
        )
        del payload["jti"]
        tampered = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        client.cookies.set("refresh_token", tampered)
        response = await client.post("/api/auth/refresh")
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    async def test_refresh_token_reuse(self, auth_client: AsyncClient):
        old_refresh = auth_client.cookies.get("refresh_token")
        # First refresh rotates the token
        resp1 = await auth_client.post("/api/auth/refresh")
        assert resp1.status_code == 200
        # Reuse the old token
        auth_client.cookies.set("refresh_token", old_refresh)
        resp2 = await auth_client.post("/api/auth/refresh")
        assert resp2.status_code == 401
        assert "revoked" in resp2.json()["detail"].lower()


@pytest.mark.asyncio
class TestLogout:
    async def test_logout_success(self, auth_client: AsyncClient):
        response = await auth_client.post("/api/auth/logout")
        assert response.status_code == 204
        me = await auth_client.get("/api/auth/me")
        assert me.status_code == 401

    async def test_logout_revokes_refresh_token(
        self, auth_client: AsyncClient
    ):
        old_refresh = auth_client.cookies.get("refresh_token")
        await auth_client.post("/api/auth/logout")
        auth_client.cookies.set("refresh_token", old_refresh)
        response = await auth_client.post("/api/auth/refresh")
        assert response.status_code == 401
        assert "revoked" in response.json()["detail"].lower()

    async def test_logout_unauthenticated(self, client: AsyncClient):
        response = await client.post("/api/auth/logout")
        assert response.status_code == 204
