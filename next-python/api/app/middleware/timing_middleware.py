"""Timing middleware to add processing time header."""

import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware to add X-Process-Time header to responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and add timing header."""
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
