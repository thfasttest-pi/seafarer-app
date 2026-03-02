"""Rate limit dependency."""

from enum import Enum
from typing import Annotated

from fastapi import Depends, Request

from app.core.errors import RateLimitError
from app.core.ratelimit.memory import MemoryLimiter
from app.core.settings import settings


class RateLimitTier(str, Enum):
    """Rate limit tier."""

    DEFAULT = "default"
    SEARCH = "search"
    APPLY = "apply"


_limiter = MemoryLimiter()


def _get_key(request: Request) -> str:
    """Key: tg_user_id if present, else client IP."""
    tg = getattr(request.state, "tg_user_id", None)
    if tg is not None:
        return f"tg:{tg}"
    host = request.client.host if request.client else "unknown"
    return f"ip:{host}"


def _get_limit(tier: RateLimitTier) -> int:
    if tier == RateLimitTier.SEARCH:
        return settings.RATE_LIMIT_SEARCH_REQUESTS
    if tier == RateLimitTier.APPLY:
        return settings.RATE_LIMIT_APPLY_REQUESTS
    return settings.RATE_LIMIT_REQUESTS


async def rate_limit(
    request: Request,
    tier: RateLimitTier = RateLimitTier.DEFAULT,
) -> None:
    """Dependency: raise 429 if rate exceeded."""
    key = _get_key(request)
    limit = _get_limit(tier)
    window = settings.RATE_LIMIT_WINDOW_SECONDS
    allowed = await _limiter.is_allowed(key, limit, window)
    if not allowed:
        raise RateLimitError("Rate limit exceeded")


def require_rate_limit(tier: RateLimitTier):
    """Factory for tier-specific rate limit deps."""

    async def dep(request: Request) -> None:
        await rate_limit(request, tier)

    return dep
