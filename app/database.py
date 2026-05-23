from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import DATABASE_URL, DB_ECHO

engine = create_async_engine(DATABASE_URL, echo=DB_ECHO)
# expire_on_commit=False: ORM-объекты НЕ устаревают после commit.
# Это нужно для сериализации ответов (Pydantic обращается к ORM-аттрибутам
# синхронно, без greenlet, поэтому lazy-load после commit падает с
# MissingGreenlet). Трейд-офф: теоретический stale read — приемлем для проекта.
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
