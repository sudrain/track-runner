from datetime import UTC, datetime, timedelta

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRunningStats:
    async def test_stats_empty(self, auth_client: AsyncClient):
        response = await auth_client.get("/api/statistics/running")
        assert response.status_code == 200
        data = response.json()
        assert data["week_km"] == 0
        assert data["month_km"] == 0
        assert data["year_km"] == 0
        assert data["week_avg_tempo"] is None
        assert data["month_avg_tempo"] is None
        assert data["year_avg_tempo"] is None

    async def test_stats_with_data(self, auth_client: AsyncClient):
        await auth_client.post(
            "/api/cardio/",
            json={
                "name": "Today Run",
                "datetime": datetime.now(UTC)
                .isoformat(),
                "notes": "",
                "intervals": [
                    {"duration_minutes": 30, "distance_km": 5.0},
                ],
            },
        )
        response = await auth_client.get("/api/statistics/running")
        assert response.status_code == 200
        data = response.json()
        assert data["week_km"] >= 5.0
        assert data["month_km"] >= 5.0
        assert data["year_km"] >= 5.0
        assert data["week_avg_tempo"] == 6.0
        assert data["month_avg_tempo"] == 6.0
        assert data["year_avg_tempo"] == 6.0

    async def test_stats_old_workout_excluded(self, auth_client: AsyncClient):
        old_date = (datetime.now(UTC) - timedelta(days=60)).isoformat()
        await auth_client.post(
            "/api/cardio/",
            json={
                "name": "Old Run",
                "datetime": old_date,
                "notes": "",
                "intervals": [
                    {"duration_minutes": 30, "distance_km": 100.0},
                ],
            },
        )
        response = await auth_client.get("/api/statistics/running")
        data = response.json()
        assert data["week_km"] == 0
        assert data["month_km"] == 0
        assert data["year_km"] == 100.0
        assert data["week_avg_tempo"] is None
        assert data["month_avg_tempo"] is None
        assert data["year_avg_tempo"] == 0.3

    async def test_stats_unauthorized(self, client: AsyncClient):
        response = await client.get("/api/statistics/running")
        assert response.status_code == 401
