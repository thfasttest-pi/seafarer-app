"""User schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MeResponse(BaseModel):
    """Current user (GET /api/v1/me)."""

    id: UUID
    telegram_id: int | None = None
    role: str
    created_at: datetime
