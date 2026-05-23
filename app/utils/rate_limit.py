import time
from collections import defaultdict

from fastapi import HTTPException, Request, status

_store: dict[str, list[float]] = defaultdict(list)


def rate_limit(max_requests: int = 10, window_seconds: int = 60):
    def limiter(request: Request):
        key = request.client.host if request.client else "unknown"
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

    return limiter
