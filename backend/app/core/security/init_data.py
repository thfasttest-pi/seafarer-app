"""Telegram initData validation (HMAC-SHA256)."""

import hashlib
import hmac
import json
import time
import urllib.parse
from dataclasses import dataclass
from typing import Any

from app.core.settings import settings


@dataclass
class Claims:
    """Parsed initData claims."""

    user_id: int
    auth_date: int
    user: dict[str, Any] | None = None


def verify_init_data(init_data: str) -> Claims:
    """
    Verify initData via HMAC-SHA256.
    Raises ValueError on invalid/expired data.
    """
    if not init_data or not init_data.strip():
        raise ValueError("initData is empty")

    params = urllib.parse.parse_qsl(init_data, keep_blank_values=True)
    params_dict = dict(params)

    hash_val = params_dict.pop("hash", None)
    if not hash_val:
        raise ValueError("hash missing in initData")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(params_dict.items(), key=lambda x: x[0])
    )
    secret_key = hashlib.sha256(settings.BOT_TOKEN.encode()).digest()
    computed = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(computed, hash_val):
        raise ValueError("Invalid initData signature")

    auth_date = int(params_dict.get("auth_date", 0))
    max_age_sec = settings.INIT_DATA_MAX_AGE_MINUTES * 60
    if time.time() - auth_date > max_age_sec:
        raise ValueError("initData expired")

    user_raw = params_dict.get("user")
    user_id = 0
    user_obj: dict[str, Any] | None = None
    if user_raw:
        try:
            user_obj = json.loads(user_raw)
            user_id = int(user_obj.get("id", 0))
        except (json.JSONDecodeError, (TypeError, ValueError)):
            pass

    if not user_id:
        raise ValueError("user_id not found in initData")

    return Claims(user_id=user_id, auth_date=auth_date, user=user_obj)
