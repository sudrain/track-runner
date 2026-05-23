import pytest
from httpx import AsyncClient

from app.utils.rate_limit import _store


@pytest.fixture(autouse=True)
def _clear_rate_limit_store():
    _store.clear()


@pytest.mark.asyncio
class TestRateLimitRegister:
    async def test_too_many_requests(self, client: AsyncClient):
        for i in range(5):
            resp = await client.post(
                "/api/auth/register",
                json={
                    "email": f"user{i}@example.com",
                    "password": "securepass123",
                },
            )
            assert resp.status_code == 201, f"request {i} failed: {resp.text}"
        # 6th request should be rate-limited
        resp = await client.post(
            "/api/auth/register",
            json={
                "email": "overflow@example.com",
                "password": "securepass123",
            },
        )
        assert resp.status_code == 429

    async def test_x_real_ip_spoof_ignored(self, client: AsyncClient):
        for i in range(5):
            resp = await client.post(
                "/api/auth/register",
                json={
                    "email": f"spoof{i}@example.com",
                    "password": "securepass123",
                },
                headers={"X-Real-IP": f"10.0.0.{i}"},
            )
            assert resp.status_code == 201, f"request {i} failed: {resp.text}"
        resp = await client.post(
            "/api/auth/register",
            json={"email": "spoof-ovf@example.com", "password": "securepass123"},
            headers={"X-Real-IP": "10.0.0.99"},
        )
        assert resp.status_code == 429


@pytest.mark.asyncio
class TestRateLimitLogin:
    async def test_too_many_requests(self, client: AsyncClient, test_user: dict):
        for i in range(10):
            resp = await client.post(
                "/api/auth/login",
                json={
                    "email": test_user["email"],
                    "password": "wrongpass",
                },
            )
            assert resp.status_code == 401, f"request {i} failed: {resp.text}"
        # 11th request should be rate-limited
        resp = await client.post(
            "/api/auth/login",
            json={
                "email": test_user["email"],
                "password": "wrongpass",
            },
        )
        assert resp.status_code == 429
