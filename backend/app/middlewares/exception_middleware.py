from typing import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from app.errors.base import DatabaseConnectionError
from app.core.logger_setup import get_logger

logger = get_logger(__name__)


class ExceptionMiddleware(BaseHTTPMiddleware):
    """
    Middleware for exception handling.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            response = await call_next(request)
            return response
        except DatabaseConnectionError as e:
            logger.error(f"Database error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Database error.",
                    "error": str(e),
                },
            )
        except Exception as e:
            logger.exception("Unhandled exception occurred.")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "An internal server error occurred.",
                    "error": str(e),
                },
            )
