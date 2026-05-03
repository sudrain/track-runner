from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine

app = FastAPI(title="Track Runner")

# Монтируем статику
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def init_db():
    # Создаём таблицы (для разработки, в проде используем миграции)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Track Runner API"}
