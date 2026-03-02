"""Cursor pagination schemas. MAX_LIMIT=50 used everywhere."""

from typing import Generic, TypeVar

from pydantic import BaseModel

from app.core.constants import MAX_LIMIT

T = TypeVar("T")
__all__ = ["Page", "MAX_LIMIT"]


class Page(BaseModel, Generic[T]):
    """Cursor-paginated response. next_cursor is null when no more items."""

    items: list[T]
    next_cursor: str | None = None
