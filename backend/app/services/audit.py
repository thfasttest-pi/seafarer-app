"""Audit logging service."""

from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_event import AuditEvent


async def log_event(
    db: AsyncSession,
    *,
    actor_user_id: UUID | None = None,
    action: str,
    target_type: str,
    target_id: str | None = None,
    request_id: str | None = None,
    before_json: dict | None = None,
    after_json: dict | None = None,
) -> None:
    """Log audit event."""
    event = AuditEvent(
        actor_user_id=actor_user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        request_id=request_id,
        before_json=before_json,
        after_json=after_json,
    )
    db.add(event)
    await db.flush()
