import unicodedata
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import delete as sa_delete
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    COOKIE_SECURE,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from app.dependencies import get_current_user, get_db
from app.models import RevokedRefreshToken, User
from app.schemas import UserLogin, UserOut, UserRegister
from app.utils.rate_limit import rate_limit
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
async def register(
    data: UserRegister,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(rate_limit(max_requests=5, window_seconds=300)),
):
    email = unicodedata.normalize("NFKC", data.email).lower().strip()
    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    user = User(
        email=email, hashed_password=get_password_hash(data.password.get_secret_value())
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        ) from None
    await db.refresh(user)
    return user


@router.post("/login", response_model=UserOut)
async def login(
    data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(rate_limit(max_requests=10, window_seconds=300)),
):
    email = unicodedata.normalize("NFKC", data.email).lower().strip()
    user = await db.execute(select(User).where(User.email == email))
    user = user.scalar_one_or_none()
    if not user or not verify_password(
        data.password.get_secret_value(), user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    _set_auth_cookies(response, access_token, refresh_token)
    return user


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="strict",
        path="/api",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="strict",
        path="/api",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )


@router.post("/refresh")
async def refresh(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(rate_limit(max_requests=5, window_seconds=300)),
):
    raw_token = request.cookies.get("refresh_token")
    if not raw_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )
    payload = decode_token(raw_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    jti = payload.get("jti")
    user_id = payload.get("sub")

    # Atomically insert JTI — unique constraint prevents reuse race
    if jti:
        exp = payload.get("exp")
        try:
            db.add(
                RevokedRefreshToken(
                    user_id=user_id,
                    token_jti=jti,
                    expires_at=datetime.fromtimestamp(exp, tz=UTC),
                )
            )
            await db.flush()
        except IntegrityError:
            await db.rollback()
            # Token reuse detected — revoke all sessions for this user
            await db.execute(
                sa_delete(RevokedRefreshToken).where(
                    RevokedRefreshToken.user_id == user_id
                )
            )
            await db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
            ) from None

    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    new_access = create_access_token({"sub": user.id})
    new_refresh = create_refresh_token({"sub": user.id})

    _set_auth_cookies(response, new_access, new_refresh)
    await db.commit()
    return {"ok": True}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(rate_limit(max_requests=5, window_seconds=300)),
):
    raw_token = request.cookies.get("refresh_token")
    if raw_token:
        payload = decode_token(raw_token)
        if payload:
            jti = payload.get("jti")
            user_id = payload.get("sub")
            exp = payload.get("exp")
            if jti and user_id and exp:
                db.add(
                    RevokedRefreshToken(
                        user_id=user_id,
                        token_jti=jti,
                        expires_at=datetime.fromtimestamp(
                            exp, tz=UTC
                        ),
                    )
                )
                await db.commit()
    response.delete_cookie(key="access_token", path="/api")
    response.delete_cookie(key="refresh_token", path="/api")
    return None


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
