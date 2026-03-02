"""Unified error format and exception handlers."""

from typing import Any

from fastapi import HTTPException, Request
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Unified error response."""

    code: str
    message: str
    request_id: str | None = None


def get_request_id(request: Request) -> str | None:
    """Get request_id from request.state."""
    return getattr(request.state, "request_id", None)


class AuthError(HTTPException):
    """401 auth error."""

    def __init__(self, message: str = "Invalid initData") -> None:
        super().__init__(status_code=401, detail=message)


class RateLimitError(HTTPException):
    """429 rate limit exceeded."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(status_code=429, detail=message)


class ForbiddenError(HTTPException):
    """403 forbidden (RBAC)."""

    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(status_code=403, detail=message)


class NotFoundError(HTTPException):
    """404 not found."""

    def __init__(self, message: str = "Not found") -> None:
        super().__init__(status_code=404, detail=message)


def error_response(
    code: str,
    message: str,
    request_id: str | None = None,
) -> dict[str, Any]:
    """Build unified error dict."""
    return {"code": code, "message": message, "request_id": request_id}
