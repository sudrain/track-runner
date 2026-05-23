from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import app.models
from app.database import Base, engine
from app.routers import auth, cardio, statistics, strength


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы (для разработки, в проде используем миграции)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Track Runner", lifespan=lifespan)

# Монтируем статику
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth.router)
app.include_router(cardio.router)
app.include_router(strength.router)
app.include_router(statistics.router)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Track Runner API"}
