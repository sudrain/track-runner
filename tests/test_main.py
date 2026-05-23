import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
class TestRoot:
    async def test_root_returns_status(self):
        from app.main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            response = await c.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


@pytest.mark.asyncio
class TestCORS:
    async def test_cors_preflight(self):
        from app.main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            response = await c.options(
                "/auth/login",
                headers={
                    "Origin": "http://example.com",
                    "Access-Control-Request-Method": "POST",
                },
            )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


@pytest.mark.asyncio
class TestHealth:
    async def test_health_returns_status(self):
        from app.main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            response = await c.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ("ok", "degraded")
        assert "database" in data
