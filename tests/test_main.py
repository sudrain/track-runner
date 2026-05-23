import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRoot:
    async def test_root_returns_status(self, client: AsyncClient):
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


@pytest.mark.asyncio
class TestCORS:
    async def test_cors_preflight(self, client: AsyncClient):
        response = await client.options(
            "/api/auth/login",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
            },
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


@pytest.mark.asyncio
class TestHealth:
    async def test_health_returns_status(self, client: AsyncClient):
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ("ok", "degraded")
        assert "database" in data
