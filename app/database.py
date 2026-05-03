from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import DATABASE_URL

# Асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True для отладки

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Базовый класс для моделей
class Base(DeclarativeBase):
    pass
