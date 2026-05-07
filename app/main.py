from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import app.models
from app.database import Base, engine
from app.routers import auth, cardio, strength

app = FastAPI(title="Track Runner")

# Монтируем статику
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth.router)
app.include_router(cardio.router)
app.include_router(strength.router)


@app.on_event("startup")
async def init_db():
    # Создаём таблицы (для разработки, в проде используем миграции)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Track Runner API"}
