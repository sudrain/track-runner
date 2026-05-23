import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRateLimitRegister:
    async def test_too_many_requests(self, client: AsyncClient):
        for i in range(5):
            resp = await client.post(
                "/auth/register",
                json={
                    "email": f"user{i}@example.com",
                    "password": "securepass123",
                },
            )
            assert resp.status_code == 201, f"request {i} failed: {resp.text}"
        # 6th request should be rate-limited
        resp = await client.post(
            "/auth/register",
            json={
                "email": "overflow@example.com",
                "password": "securepass123",
            },
        )
        assert resp.status_code == 429


@pytest.mark.asyncio
class TestRateLimitLogin:
    async def test_too_many_requests(self, client: AsyncClient, test_user: dict):
        for i in range(10):
            resp = await client.post(
                "/auth/login",
                json={
                    "email": test_user["email"],
                    "password": "wrongpass",
                },
            )
            assert resp.status_code == 401, f"request {i} failed: {resp.text}"
        # 11th request should be rate-limited
        resp = await client.post(
            "/auth/login",
            json={
                "email": test_user["email"],
                "password": "wrongpass",
            },
        )
        assert resp.status_code == 429
