"""In-memory rate limiter."""

import asyncio
import time
from collections import defaultdict

from app.core.ratelimit.base import Limiter


class MemoryLimiter(Limiter):
    """In-memory sliding window limiter."""

    def __init__(self) -> None:
        self._counts: dict[str, list[float]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def is_allowed(self, key: str, limit: int, window_sec: int) -> bool:
        async with self._lock:
            now = time.monotonic()
            cutoff = now - window_sec
            timestamps = self._counts[key]
            timestamps[:] = [t for t in timestamps if t > cutoff]
            if len(timestamps) >= limit:
                return False
            timestamps.append(now)
            return True
