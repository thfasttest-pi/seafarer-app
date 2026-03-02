"""FastAPI application."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.v1.jobs import router as jobs_router
from app.api.v1.me import router as me_router
from app.core.errors import (
    AuthError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    error_response,
    get_request_id,
)
from app.core.middleware.request_id import RequestIDMiddleware
from app.core.settings import settings

app = FastAPI(title="Seafarer API", version="0.1.0")

app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _err_response(request: Request, code: str, message: str, status: int) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content=error_response(code, message, get_request_id(request)),
    )


@app.exception_handler(AuthError)
async def auth_exception_handler(request: Request, exc: AuthError) -> JSONResponse:
    return _err_response(request, "auth_error", exc.detail, 401)


@app.exception_handler(RateLimitError)
async def rate_limit_handler(request: Request, exc: RateLimitError) -> JSONResponse:
    return _err_response(request, "rate_limit_exceeded", exc.detail, 429)


@app.exception_handler(ForbiddenError)
async def forbidden_handler(request: Request, exc: ForbiddenError) -> JSONResponse:
    return _err_response(request, "forbidden", exc.detail, 403)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return _err_response(request, "not_found", exc.detail, 404)


@app.exception_handler(HTTPException)
async def http_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return _err_response(request, "http_error", str(exc.detail), exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return _err_response(
        request,
        "validation_error",
        "Invalid request",
        422,
    )


@app.exception_handler(Exception)
async def generic_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all: every error has request_id and unified format."""
    return _err_response(
        request,
        "internal_error",
        "An error occurred",
        500,
    )


app.include_router(jobs_router, prefix="/api/v1")
app.include_router(me_router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check (no auth)."""
    return {"status": "ok"}
