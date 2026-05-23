import asyncio
import os
from contextlib import asynccontextmanager

from alembic.config import Config
from alembic import command
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError

import app.models
from app.config import CORS_ORIGINS
from app.database import Base, engine
from app.routers import auth, cardio, statistics, strength


def _run_alembic_upgrade():
    alembic_ini = os.path.join(os.path.dirname(__file__), "..", "alembic.ini")
    if not os.path.exists(alembic_ini):
        return False
    cfg = Config(alembic_ini)
    try:
        command.upgrade(cfg, "head")
    except ProgrammingError:
        command.stamp(cfg, "head")
    return True


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_running_loop()
    migrated = await loop.run_in_executor(None, _run_alembic_upgrade)
    if not migrated:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    # Проверка подключения к БД
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        pass
    yield


app = FastAPI(title="Track Runner", lifespan=lifespan)

origins = [o.strip() for o in CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth.router)
app.include_router(cardio.router)
app.include_router(strength.router)
app.include_router(statistics.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.detail}
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/")
async def root():
    return {"status": "ok", "message": "Track Runner API"}


@app.get("/health")
async def health():
    db_ok = False
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        pass
    return {"status": "ok" if db_ok else "degraded", "database": "ok" if db_ok else "error"}
