import time
from collections import defaultdict

from fastapi import HTTPException, Request, status

_store: dict[str, list[float]] = defaultdict(list)
_MAX_STORE_KEYS = 10_000
_request_counter = 0


def _cleanup_store():
    now = time.time()
    cutoff = now - 7200
    stale = []
    for k, v in _store.items():
        v[:] = [t for t in v if t > cutoff]
        if not v:
            stale.append(k)
    for k in stale:
        del _store[k]


def _rate_limit_key(request: Request) -> str:
    from app.config import TRUSTED_PROXY

    if TRUSTED_PROXY:
        forwarded = request.headers.get("X-Forwarded-For", "")
        real_ip = request.headers.get("X-Real-IP", "")
        return (real_ip or forwarded.split(",")[0].strip()
                or (request.client.host if request.client else None)
                or "unknown")
    return request.client.host or "unknown"


def rate_limit(max_requests: int = 10, window_seconds: int = 60):
    def limiter(request: Request):
        global _request_counter
        key = _rate_limit_key(request)
        now = time.time()
        cutoff = now - window_seconds
        timestamps = _store[key]
        timestamps[:] = [t for t in timestamps if t > cutoff]
        if len(timestamps) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
            )
        timestamps.append(now)
        _request_counter += 1
        if _request_counter % 100 == 0 or len(_store) > _MAX_STORE_KEYS:
            _cleanup_store()

    return limiter
