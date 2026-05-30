import pytest
from httpx import AsyncClient

_WORKOUT_DATA = {
    "name": "Morning Run",
    "datetime": "2026-05-20T06:00:00Z",
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

    async def test_create_without_optional_fields(self, auth_client: AsyncClient):
        data = {
            "name": "Minimal",
            "datetime": "2026-05-20T06:00:00Z",
            "notes": "",
            "intervals": [
                {"duration_minutes": 25.0, "distance_km": 4.0},
            ],
        }
        response = await auth_client.post("/api/cardio/", json=data)
        assert response.status_code == 201
        assert response.json()["intervals"][0]["tempo_min_per_km"] == 6.25
        assert response.json()["intervals"][0]["avg_heart_rate"] is None

    async def test_create_multiple_intervals(self, auth_client: AsyncClient):
        data = {
            "name": "Intervals",
            "datetime": "2026-05-20T06:00:00Z",
            "notes": "",
            "intervals": [
                {"duration_minutes": 10.0, "distance_km": 2.0},
                {"duration_minutes": 20.0, "distance_km": 4.0},
            ],
        }
        response = await auth_client.post("/api/cardio/", json=data)
        assert response.status_code == 201
        assert len(response.json()["intervals"]) == 2

    async def test_create_unauthorized(self, client: AsyncClient):
        response = await client.post("/api/cardio/", json=_WORKOUT_DATA)
        assert response.status_code == 401


@pytest.mark.asyncio
class TestListCardio:
    async def test_list_empty(self, auth_client: AsyncClient):
        response = await auth_client.get("/api/cardio/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    async def test_list_with_data(self, auth_client: AsyncClient):
        await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        response = await auth_client.get("/api/cardio/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Morning Run"

    async def test_list_ordered_by_date_desc(self, auth_client: AsyncClient):
        days = ["2026-05-18T06:00:00Z", "2026-05-20T06:00:00Z", "2026-05-19T06:00:00Z"]
        for i, day in enumerate(days):
            w = {**_WORKOUT_DATA, "name": f"Run {i}", "datetime": day}
            await auth_client.post("/api/cardio/", json=w)
        response = await auth_client.get("/api/cardio/")
        names = [item["name"] for item in response.json()["items"]]
        assert names == ["Run 1", "Run 2", "Run 0"]

    async def test_list_pagination(self, auth_client: AsyncClient):
        for i in range(3):
            w = {**_WORKOUT_DATA, "name": f"Run {i}"}
            await auth_client.post("/api/cardio/", json=w)
        full = await auth_client.get("/api/cardio/")
        assert full.json()["total"] == 3
        assert len(full.json()["items"]) == 3
        limited = await auth_client.get("/api/cardio/?offset=0&limit=2")
        assert len(limited.json()["items"]) == 2
        assert limited.json()["total"] == 3
        skipped = await auth_client.get("/api/cardio/?offset=2&limit=10")
        assert len(skipped.json()["items"]) == 1
        assert skipped.json()["total"] == 3


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

    async def test_get_other_users_workout(
        self, auth_client: AsyncClient, second_auth_client: AsyncClient
    ):
        post_resp = await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await second_auth_client.get(f"/api/cardio/{workout_id}")
        assert response.status_code == 404


@pytest.mark.asyncio
class TestUpdateCardio:
    async def test_update_success(self, auth_client: AsyncClient):
        post_resp = await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await auth_client.patch(
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
        response = await auth_client.patch(
            f"/api/cardio/{workout_id}",
            json={"notes": "Just notes update"},
        )
        assert response.status_code == 200
        assert response.json()["notes"] == "Just notes update"

    async def test_update_not_found(self, auth_client: AsyncClient):
        response = await auth_client.patch(
            "/api/cardio/99999",
            json={"name": "Doesn't matter"},
        )
        assert response.status_code == 404

    async def test_update_unauthorized(self, client: AsyncClient):
        response = await client.patch(
            "/api/cardio/1",
            json={"name": "Hacked"},
        )
        assert response.status_code == 401

    async def test_update_other_users_workout(
        self, auth_client: AsyncClient, second_auth_client: AsyncClient
    ):
        post_resp = await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await second_auth_client.patch(
            f"/api/cardio/{workout_id}",
            json={"name": "Stolen"},
        )
        assert response.status_code == 404


@pytest.mark.asyncio
class TestPatchCardio:
    async def test_patch_success(self, auth_client: AsyncClient):
        post_resp = await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await auth_client.patch(
            f"/api/cardio/{workout_id}",
            json={
                "name": "Evening Run",
                "notes": "Patched notes",
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
        assert data["notes"] == "Patched notes"
        assert len(data["intervals"]) == 1
        assert data["intervals"][0]["distance_km"] == 3.0

    async def test_patch_partial(self, auth_client: AsyncClient):
        post_resp = await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await auth_client.patch(
            f"/api/cardio/{workout_id}",
            json={"notes": "Just notes patch"},
        )
        assert response.status_code == 200
        assert response.json()["notes"] == "Just notes patch"

    async def test_patch_preserves_intervals(self, auth_client: AsyncClient):
        post_resp = await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        orig_id = post_resp.json()["intervals"][0]["id"]
        response = await auth_client.patch(
            f"/api/cardio/{workout_id}",
            json={"notes": "Only notes changed"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["intervals"]) == 1
        assert data["intervals"][0]["id"] == orig_id
        assert data["intervals"][0]["distance_km"] == 5.0

    async def test_patch_not_found(self, auth_client: AsyncClient):
        response = await auth_client.patch(
            "/api/cardio/99999",
            json={"name": "Doesn't matter"},
        )
        assert response.status_code == 404

    async def test_patch_unauthorized(self, client: AsyncClient):
        response = await client.patch(
            "/api/cardio/1",
            json={"name": "Hacked"},
        )
        assert response.status_code == 401

    async def test_patch_other_users_workout(
        self, auth_client: AsyncClient, second_auth_client: AsyncClient
    ):
        post_resp = await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await second_auth_client.patch(
            f"/api/cardio/{workout_id}",
            json={"name": "Stolen"},
        )
        assert response.status_code == 404


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

    async def test_delete_unauthorized(self, client: AsyncClient):
        response = await client.delete("/api/cardio/1")
        assert response.status_code == 401

    async def test_delete_other_users_workout(
        self, auth_client: AsyncClient, second_auth_client: AsyncClient
    ):
        post_resp = await auth_client.post("/api/cardio/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await second_auth_client.delete(f"/api/cardio/{workout_id}")
        assert response.status_code == 404
