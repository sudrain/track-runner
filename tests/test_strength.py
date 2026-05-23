import pytest
from httpx import AsyncClient

_WORKOUT_DATA = {
    "datetime": "2026-05-20T10:00:00Z",
    "notes": "Leg day",
    "exercises": [
        {
            "name": "Squat",
            "sets": [
                {"weight_kg": 80.0, "repetitions": 10},
                {"weight_kg": 90.0, "repetitions": 8},
            ],
        },
        {
            "name": "Deadlift",
            "sets": [
                {"weight_kg": 100.0, "repetitions": 5},
            ],
        },
    ],
}


@pytest.mark.asyncio
class TestCreateStrength:
    async def test_create_success(self, auth_client: AsyncClient):
        response = await auth_client.post("/api/strength/", json=_WORKOUT_DATA)
        assert response.status_code == 201
        data = response.json()
        assert data["notes"] == "Leg day"
        assert len(data["exercises"]) == 2
        assert data["exercises"][0]["name"] == "Squat"
        assert len(data["exercises"][0]["sets"]) == 2
        assert data["exercises"][1]["name"] == "Deadlift"

    async def test_create_no_exercises(self, auth_client: AsyncClient):
        data = {**_WORKOUT_DATA, "exercises": []}
        response = await auth_client.post("/api/strength/", json=data)
        assert response.status_code == 422

    async def test_create_unauthorized(self, client: AsyncClient):
        response = await client.post("/api/strength/", json=_WORKOUT_DATA)
        assert response.status_code == 401


@pytest.mark.asyncio
class TestListStrength:
    async def test_list_empty(self, auth_client: AsyncClient):
        response = await auth_client.get("/api/strength/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    async def test_list_with_data(self, auth_client: AsyncClient):
        await auth_client.post("/api/strength/", json=_WORKOUT_DATA)
        response = await auth_client.get("/api/strength/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["notes"] == "Leg day"


@pytest.mark.asyncio
class TestGetStrength:
    async def test_get_success(self, auth_client: AsyncClient):
        post_resp = await auth_client.post("/api/strength/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await auth_client.get(f"/api/strength/{workout_id}")
        assert response.status_code == 200
        assert response.json()["id"] == workout_id

    async def test_get_not_found(self, auth_client: AsyncClient):
        response = await auth_client.get("/api/strength/99999")
        assert response.status_code == 404

    async def test_get_unauthorized(self, client: AsyncClient):
        response = await client.get("/api/strength/1")
        assert response.status_code == 401

    async def test_get_other_users_workout(
        self, auth_client: AsyncClient, second_auth_client: AsyncClient
    ):
        post_resp = await auth_client.post("/api/strength/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await second_auth_client.get(f"/api/strength/{workout_id}")
        assert response.status_code == 404


@pytest.mark.asyncio
class TestUpdateStrength:
    async def test_update_success(self, auth_client: AsyncClient):
        post_resp = await auth_client.post("/api/strength/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await auth_client.put(
            f"/api/strength/{workout_id}",
            json={
                "notes": "Updated leg day",
                "exercises": [
                    {
                        "name": "Leg Press",
                        "sets": [{"weight_kg": 120.0, "repetitions": 10}],
                    }
                ],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["notes"] == "Updated leg day"
        assert len(data["exercises"]) == 1
        assert data["exercises"][0]["name"] == "Leg Press"

    async def test_update_partial(self, auth_client: AsyncClient):
        post_resp = await auth_client.post("/api/strength/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await auth_client.put(
            f"/api/strength/{workout_id}",
            json={"notes": "Just notes"},
        )
        assert response.status_code == 200
        assert response.json()["notes"] == "Just notes"

    async def test_update_not_found(self, auth_client: AsyncClient):
        response = await auth_client.put(
            "/api/strength/99999",
            json={"notes": "Nope"},
        )
        assert response.status_code == 404

    async def test_update_unauthorized(self, client: AsyncClient):
        response = await client.put(
            "/api/strength/1",
            json={"notes": "Hacked"},
        )
        assert response.status_code == 401

    async def test_update_other_users_workout(
        self, auth_client: AsyncClient, second_auth_client: AsyncClient
    ):
        post_resp = await auth_client.post("/api/strength/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await second_auth_client.put(
            f"/api/strength/{workout_id}",
            json={"notes": "Stolen"},
        )
        assert response.status_code == 404


@pytest.mark.asyncio
class TestDeleteStrength:
    async def test_delete_success(self, auth_client: AsyncClient):
        post_resp = await auth_client.post("/api/strength/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await auth_client.delete(f"/api/strength/{workout_id}")
        assert response.status_code == 204

    async def test_delete_not_found(self, auth_client: AsyncClient):
        response = await auth_client.delete("/api/strength/99999")
        assert response.status_code == 404

    async def test_delete_unauthorized(self, client: AsyncClient):
        response = await client.delete("/api/strength/1")
        assert response.status_code == 401

    async def test_delete_other_users_workout(
        self, auth_client: AsyncClient, second_auth_client: AsyncClient
    ):
        post_resp = await auth_client.post("/api/strength/", json=_WORKOUT_DATA)
        workout_id = post_resp.json()["id"]
        response = await second_auth_client.delete(f"/api/strength/{workout_id}")
        assert response.status_code == 404
