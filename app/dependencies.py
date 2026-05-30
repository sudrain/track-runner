from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models import User
from app.utils.security import decode_token


class PaginatedParams:
    def __init__(
        self,
        offset: int = Query(default=0, ge=0, description="Смещение"),
        limit: int = Query(default=50, ge=1, le=200, description="Лимит"),
    ):
        self.offset = offset
        self.limit = limit


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Создаёт сессию БД для каждого запроса и закрывает после."""
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    request: Request, db: AsyncSession = Depends(get_db)
) -> User:
    """Извлекает пользователя из JWT в куке."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    payload = decode_token(token, expected_type="access")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user
