import os
import tempfile
from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Set test env BEFORE any app imports
_db_file = tempfile.mktemp(suffix=".db")
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{_db_file}"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["REFRESH_TOKEN_EXPIRE_DAYS"] = "7"

from app.database import Base
from app.dependencies import get_db
from app.main import app
from app.models import User
from app.utils.rate_limit import _store
from app.utils.security import get_password_hash

_user_counter = 0


@pytest_asyncio.fixture(scope="session")
async def engine():
    e = create_async_engine(os.environ["DATABASE_URL"], echo=False)
    async with e.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield e
    async with e.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await e.dispose()
    if os.path.exists(_db_file):
        os.remove(_db_file)


@pytest_asyncio.fixture
async def session(engine):
    session = async_sessionmaker(engine, expire_on_commit=False)()
    try:
        yield session
    finally:
        _store.clear()
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(delete(table))
        await session.commit()
        await session.close()


@pytest_asyncio.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(session: AsyncSession) -> dict:
    global _user_counter
    _user_counter += 1
    email = f"test{_user_counter}@example.com"
    password = "testpass123"
    user = User(
        email=email,
        hashed_password=get_password_hash(password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"id": user.id, "email": email, "password": password}


@pytest_asyncio.fixture
async def auth_client(
    client: AsyncClient, test_user: dict
) -> AsyncClient:
    response = await client.post(
        "/auth/login",
        json={"email": test_user["email"], "password": test_user["password"]},
    )
    assert response.status_code == 200
    return client


@pytest_asyncio.fixture
async def second_user(session: AsyncSession) -> dict:
    global _user_counter
    _user_counter += 1
    email = f"test{_user_counter}@example.com"
    password = "secondpass123"
    user = User(
        email=email,
        hashed_password=get_password_hash(password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"id": user.id, "email": email, "password": password}


@pytest_asyncio.fixture
async def second_auth_client(
    session: AsyncSession, second_user: dict
) -> AsyncClient:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/login",
            json={"email": second_user["email"], "password": second_user["password"]},
        )
        assert response.status_code == 200
        yield ac
    app.dependency_overrides.clear()
