import time

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.utils.rate_limit import _cleanup_store, _store
from app.utils.security import create_access_token


@pytest.mark.asyncio
class TestGetCurrentUserEdgeCases:
    async def test_me_invalid_token(self, client: AsyncClient):
        client.cookies.set("access_token", "garbage-token")
        response = await client.get("/api/auth/me")
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    async def test_me_token_without_sub(self, client: AsyncClient):
        token = create_access_token(data={})
        client.cookies.set("access_token", token)
        response = await client.get("/api/auth/me")
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    async def test_me_user_deleted(
        self, auth_client: AsyncClient, session: AsyncSession
    ):
        resp = await auth_client.get("/api/auth/me")
        user_id = resp.json()["id"]
        user = await session.get(User, user_id)
        await session.delete(user)
        await session.commit()
        response = await auth_client.get("/api/auth/me")
        assert response.status_code == 401
        assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
class TestRefreshEdgeCases:
    async def test_refresh_user_deleted(
        self, auth_client: AsyncClient, session: AsyncSession
    ):
        resp = await auth_client.get("/api/auth/me")
        user_id = resp.json()["id"]
        user = await session.get(User, user_id)
        await session.delete(user)
        await session.commit()
        response = await auth_client.post("/api/auth/refresh")
        assert response.status_code == 401
        assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
class TestLogoutEdgeCases:
    async def test_logout_invalid_token(self, client: AsyncClient):
        client.cookies.set("refresh_token", "garbage-token")
        response = await client.post("/api/auth/logout")
        assert response.status_code == 204


@pytest.mark.asyncio
class TestGlobalExceptionHandler:
    async def test_http_exception_returns_proper_response(self):
        from fastapi import HTTPException
        from starlette.requests import Request

        from app.main import global_exception_handler

        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": "GET",
            "path": "/test",
            "raw_path": b"/test",
            "headers": [],
            "query_string": b"",
            "client": ("127.0.0.1", 50000),
            "server": ("testserver", 80),
            "scheme": "http",
        }
        request = Request(scope)
        response = await global_exception_handler(
            request, HTTPException(status_code=404, detail="Not found")
        )
        assert response.status_code == 404
        assert response.body == b'{"detail":"Not found"}'

    async def test_non_http_exception_returns_500(self):
        from starlette.requests import Request

        from app.main import global_exception_handler

        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": "GET",
            "path": "/test",
            "raw_path": b"/test",
            "headers": [],
            "query_string": b"",
            "client": ("127.0.0.1", 50000),
            "server": ("testserver", 80),
            "scheme": "http",
        }
        request = Request(scope)
        response = await global_exception_handler(request, ValueError("Boom"))
        assert response.status_code == 500
        assert response.body == b'{"detail":"Internal server error"}'


class TestRateLimitInternals:
    def test_cleanup_store_removes_stale_keys(self):
        _store.clear()
        now = time.time()
        _store["stale"] = [now - 10000]
        _store["fresh"] = [now - 100]
        _store["mixed"] = [now - 10000, now - 100]
        _cleanup_store()
        assert "stale" not in _store
        assert "fresh" in _store
        assert len(_store["fresh"]) == 1
        assert "mixed" in _store
        assert len(_store["mixed"]) == 1
        _store.clear()


@pytest.mark.asyncio
class TestRateLimitTrustedProxy:
    async def test_trusted_proxy_uses_x_real_ip(self, client: AsyncClient):
        import app.config

        original = app.config.TRUSTED_PROXY
        app.config.TRUSTED_PROXY = True
        _store.clear()
        try:
            for i in range(5):
                resp = await client.post(
                    "/api/auth/register",
                    json={
                        "email": f"tp{i}@example.com",
                        "password": "securepass123",
                    },
                    headers={"X-Real-IP": "10.0.0.1"},
                )
                assert resp.status_code == 201, f"request {i} failed: {resp.text}"
            resp = await client.post(
                "/api/auth/register",
                json={
                    "email": "tp-ovf@example.com",
                    "password": "securepass123",
                },
                headers={"X-Real-IP": "10.0.0.1"},
            )
            assert resp.status_code == 429
        finally:
            app.config.TRUSTED_PROXY = original
            _store.clear()


@pytest.mark.asyncio
class TestStatsEdgeCases:
    async def test_ensure_tz_rejects_naive(self):
        from datetime import datetime

        from app.routers.statistics import _ensure_tz

        naive = datetime(2026, 5, 25, 12, 0, 0)
        with pytest.raises(ValueError, match="timezone-aware"):
            _ensure_tz(naive)
