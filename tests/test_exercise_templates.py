import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ExerciseTemplate


@pytest.mark.asyncio
class TestExerciseTemplates:
    @pytest.fixture(autouse=True)
    async def seed_templates(self, session: AsyncSession):
        templates = [
            ExerciseTemplate(name="Бег", type="cardio"),
            ExerciseTemplate(name="Плавание", type="cardio"),
            ExerciseTemplate(name="Жим", type="strength"),
            ExerciseTemplate(name="Присед", type="strength"),
        ]
        session.add_all(templates)
        await session.commit()

    async def test_list_all(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/exercise-templates/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 4

    async def test_filter_cardio(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/exercise-templates/?type=cardio")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert all(t["name"] in ["Бег", "Плавание"] for t in data)

    async def test_filter_strength(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/exercise-templates/?type=strength")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert all(t["name"] in ["Жим", "Присед"] for t in data)

    async def test_filter_no_match(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/exercise-templates/?type=invalid")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 0

    async def test_unauthorized(self, client: AsyncClient):
        resp = await client.get("/api/exercise-templates/")
        assert resp.status_code == 401
