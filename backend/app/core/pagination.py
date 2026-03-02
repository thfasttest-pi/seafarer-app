"""Cursor-based (keyset) pagination. Cursor payload: created_at (ISO8601), id."""

import base64
import json
from datetime import datetime
from typing import Union

from app.core.constants import MAX_LIMIT


def encode_cursor(created_at: datetime, id: Union[str, int]) -> str:
    """Encode cursor as base64url JSON. id supports UUID string or int."""
    payload = {
        "created_at": created_at.isoformat(),
        "id": str(id),
    }
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def decode_cursor(cursor: str) -> tuple[datetime, str] | None:
    """
    Decode cursor from base64url JSON.
    Returns (created_at, id_str) or None if invalid.
    id_str can be parsed to UUID for Job model.
    """
    if not cursor or not cursor.strip():
        return None
    try:
        pad = 4 - len(cursor) % 4
        if pad != 4:
            cursor += "=" * pad
        raw = base64.urlsafe_b64decode(cursor.encode("ascii"))
        data = json.loads(raw.decode("utf-8"))
        created_at_str = data.get("created_at")
        id_val = data.get("id")
        if not created_at_str or id_val is None:
            return None
        dt = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
        return (dt, str(id_val))
    except (ValueError, json.JSONDecodeError):
        return None


def clamp_limit(limit: int | None, default: int = 20) -> int:
    """Clamp limit to [1, MAX_LIMIT]."""
    if limit is None:
        return default
    return min(max(1, int(limit)), MAX_LIMIT)
