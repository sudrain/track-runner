import asyncio
import logging
import os
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from alembic.config import Config
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import delete, text
from sqlalchemy.exc import ProgrammingError

import app.models
from alembic import command
from app.config import AUTO_MIGRATE, CORS_ORIGINS, LOG_LEVEL
from app.database import AsyncSessionLocal, Base, engine
from app.models import RevokedRefreshToken
from app.routers import auth, cardio, exercise_templates, statistics, strength

logger = logging.getLogger("track-runner")
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def _run_alembic_upgrade():
    alembic_ini = os.path.join(os.path.dirname(__file__), "..", "alembic.ini")
    if not os.path.exists(alembic_ini):
        return False
    cfg = Config(alembic_ini)
    try:
        command.upgrade(cfg, "head")
    except ProgrammingError:
        logger.warning("Migration failed (fresh DB?), stamping head")
        command.stamp(cfg, "head")
    return True


_TOKEN_CLEANUP_INTERVAL = 3600


async def _cleanup_expired_tokens():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(
                delete(RevokedRefreshToken).where(
                    RevokedRefreshToken.expires_at < datetime.now(UTC)
                )
            )
            await session.commit()
    except Exception:
        logger.warning("Failed to cleanup expired tokens", exc_info=True)


async def _cleanup_loop():
    while True:
        await asyncio.sleep(_TOKEN_CLEANUP_INTERVAL)
        await _cleanup_expired_tokens()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if AUTO_MIGRATE:
        loop = asyncio.get_running_loop()
        migrated = await loop.run_in_executor(None, _run_alembic_upgrade)
        if not migrated:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
    await _cleanup_expired_tokens()
    cleanup_task = asyncio.create_task(_cleanup_loop())
    yield
    cleanup_task.cancel()
    await asyncio.gather(cleanup_task, return_exceptions=True)


app = FastAPI(title="Track Runner", lifespan=lifespan)

origins = [o.strip() for o in CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth.router)
app.include_router(cardio.router)
app.include_router(strength.router)
app.include_router(exercise_templates.router)
app.include_router(statistics.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=getattr(exc, "headers", None),
        )
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
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
        async with asyncio.timeout(5):
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        db_ok = True
    except TimeoutError:
        logger.warning("Health check DB timed out after 5s")
    except ProgrammingError:
        logger.exception("Health check DB query failed")
    except Exception:
        logger.warning("Health check DB connection failed", exc_info=True)
    status = "ok" if db_ok else "degraded"
    db_status = "ok" if db_ok else "error"
    return {"status": status, "database": db_status}
