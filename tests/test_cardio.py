from datetime import datetime, timedelta, timezone

import pytest
from httpx import AsyncClient

_WORKOUT_DATA = {
    "name": "Morning Run",
    "datetime": "2026-05-20T06:00:00",
    "notes": "Good run",
    "intervals": [
        {
            "duration_minutes": 30.0,
            "distance_km": 5.0,
            "tempo_min_per_km": 6.0,
            "avg_heart_rate": 145,
        }
    ],
}


@pytest.mark.asyncio
class TestCreateCardio:
    async def test_create_success(self, auth_client: AsyncClient):
        response = await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Morning Run"
        assert data["notes"] == "Good run"
        assert len(data["intervals"]) == 1
        assert data["intervals"][0]["distance_km"] == 5.0

    async def test_create_no_intervals(self, auth_client: AsyncClient):
        data = {**_WORKOUT_DATA, "intervals": []}
        response = await auth_client.post("/api/cardio/", json=data)
        assert response.status_code == 422

    async def test_create_unauthorized(self, client: AsyncClient):
        response = await client.post("/api/cardio/", json=_WORKOUT_DATA)
        assert response.status_code == 401


@pytest.mark.asyncio
class TestListCardio:
    async def test_list_empty(self, auth_client: AsyncClient):
        response = await auth_client.get("/api/cardio/")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_with_data(self, auth_client: AsyncClient):
        await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        response = await auth_client.get("/api/cardio/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Morning Run"


@pytest.mark.asyncio
class TestGetCardio:
    async def test_get_success(self, auth_client: AsyncClient):
        post_resp = await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await auth_client.get(f"/api/cardio/{workout_id}")
        assert response.status_code == 200
        assert response.json()["id"] == workout_id

    async def test_get_not_found(self, auth_client: AsyncClient):
        response = await auth_client.get("/api/cardio/99999")
        assert response.status_code == 404

    async def test_get_unauthorized(self, client: AsyncClient):
        response = await client.get("/api/cardio/1")
        assert response.status_code == 401


@pytest.mark.asyncio
class TestUpdateCardio:
    async def test_update_success(self, auth_client: AsyncClient):
        post_resp = await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await auth_client.put(
            f"/api/cardio/{workout_id}",
            json={
                "name": "Evening Run",
                "notes": "Updated notes",
                "intervals": [
                    {
                        "duration_minutes": 20.0,
                        "distance_km": 3.0,
                    }
                ],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Evening Run"
        assert data["notes"] == "Updated notes"
        assert len(data["intervals"]) == 1
        assert data["intervals"][0]["distance_km"] == 3.0

    async def test_update_partial(self, auth_client: AsyncClient):
        post_resp = await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await auth_client.put(
            f"/api/cardio/{workout_id}",
            json={"notes": "Just notes update"},
        )
        assert response.status_code == 200
        assert response.json()["notes"] == "Just notes update"


@pytest.mark.asyncio
class TestDeleteCardio:
    async def test_delete_success(self, auth_client: AsyncClient):
        post_resp = await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await auth_client.delete(f"/api/cardio/{workout_id}")
        assert response.status_code == 204

    async def test_delete_not_found(self, auth_client: AsyncClient):
        response = await auth_client.delete("/api/cardio/99999")
        assert response.status_code == 404
