"""Rate limiter interface."""

from abc import ABC, abstractmethod


class Limiter(ABC):
    """Abstract rate limiter."""

    @abstractmethod
    async def is_allowed(self, key: str, limit: int, window_sec: int) -> bool:
        """Check if request is allowed. Returns False if rate exceeded."""
        ...
