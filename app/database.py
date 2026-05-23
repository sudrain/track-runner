from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import DATABASE_URL, DB_ECHO

engine = create_async_engine(DATABASE_URL, echo=DB_ECHO)
# expire_on_commit=True (default): ORM-объекты устаревают после commit.
# Все post-commit access явно используют refresh() или re-fetch.
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession)


class Base(DeclarativeBase):
    pass
