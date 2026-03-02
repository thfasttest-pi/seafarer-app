"""Structured logging configuration."""

import logging
import sys
from typing import Any

from app.core.settings import settings


def setup_logging() -> None:
    """Configure structured logging."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        stream=sys.stdout,
        format="%(message)s" if settings.LOG_JSON else "%(levelname)s: %(message)s",
    )
