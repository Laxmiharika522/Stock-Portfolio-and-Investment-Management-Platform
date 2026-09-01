"""
Custom Exception Classes & Global Error Handlers
Provides structured, consistent error responses across the entire API.
"""

from __future__ import annotations
from typing import Any
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


# ── Custom Exception Classes ──────────────────────────────────────────────────

class AppException(Exception):
    """Base exception for all application-specific errors."""

    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Any = None,
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(message)


class NotFoundException(AppException):
    """Resource not found."""

    def __init__(self, resource: str, identifier: Any = None):
        msg = f"{resource} not found"
        if identifier:
            msg = f"{resource} with id '{identifier}' not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            message=msg,
        )


class ForbiddenException(AppException):
    """Access denied — ownership or role check failed."""

    def __init__(self, message: str = "You do not have permission to access this resource"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
            message=message,
        )


class UnauthorizedException(AppException):
    """Authentication required."""

    def __init__(self, message: str = "Authentication credentials are invalid or expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
            message=message,
        )


class ConflictException(AppException):
    """Resource already exists or conflict in state."""

    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT",
            message=message,
        )


class BadRequestException(AppException):
    """Invalid request — business rule violated."""

    def __init__(self, message: str, details: Any = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="BAD_REQUEST",
            message=message,
            details=details,
        )


class InsufficientSharesException(AppException):
    """Raised when user tries to sell more shares than they own."""

    def __init__(self, symbol: str, owned: float, requested: float):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="INSUFFICIENT_SHARES",
            message=f"Cannot sell {requested} shares of {symbol}. You only own {owned} shares.",
            details={"symbol": symbol, "owned_quantity": owned, "requested_quantity": requested},
        )


class AdminRequiredException(AppException):
    """Endpoint requires admin privileges."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="ADMIN_REQUIRED",
            message="This endpoint requires administrator privileges",
        )


# ── Error Response Builder ────────────────────────────────────────────────────

def _error_response(
    status_code: int,
    error_code: str,
    message: str,
    details: Any = None,
) -> JSONResponse:
    """Build a consistent JSON error response body."""
    content: dict[str, Any] = {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
        },
    }
    if details is not None:
        content["error"]["details"] = details
    return JSONResponse(status_code=status_code, content=content)


# ── Exception Handlers ────────────────────────────────────────────────────────

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle all custom AppException subclasses."""
    logger.warning(
        "AppException: %s %s → %s [%s]",
        request.method,
        request.url.path,
        exc.error_code,
        exc.message,
    )
    return _error_response(
        status_code=exc.status_code,
        error_code=exc.error_code,
        message=exc.message,
        details=exc.details,
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handle standard HTTP exceptions (raised by FastAPI internally)."""
    logger.warning(
        "HTTPException: %s %s → %s",
        request.method,
        request.url.path,
        exc.status_code,
    )
    error_code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        422: "VALIDATION_ERROR",
        429: "RATE_LIMIT_EXCEEDED",
        500: "INTERNAL_SERVER_ERROR",
    }
    error_code = error_code_map.get(exc.status_code, "HTTP_ERROR")
    return _error_response(
        status_code=exc.status_code,
        error_code=error_code,
        message=str(exc.detail),
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic v2 request validation errors with field-level details."""
    logger.warning(
        "ValidationError: %s %s → %d field error(s)",
        request.method,
        request.url.path,
        len(exc.errors()),
    )
    field_errors = []
    for error in exc.errors():
        field_path = " → ".join(str(loc) for loc in error["loc"] if loc != "body")
        field_errors.append({
            "field": field_path or "body",
            "message": error["msg"],
            "type": error["type"],
        })
    return _error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_code="VALIDATION_ERROR",
        message=f"Request validation failed with {len(field_errors)} error(s)",
        details=field_errors,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unexpected server errors."""
    logger.exception(
        "Unhandled exception: %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )
    return _error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred. Please try again later.",
    )


# ── Registration Helper ───────────────────────────────────────────────────────

def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI app."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
