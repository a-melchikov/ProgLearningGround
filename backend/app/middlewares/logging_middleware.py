import logging
import time
from typing import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging messages.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.perf_counter()
        logger.info(f"Incoming request: {request.method} {request.url}")
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        logger.info(f"Response status: {response.status_code} in {process_time:.4f}s")
        return response
