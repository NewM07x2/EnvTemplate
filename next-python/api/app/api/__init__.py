"""API package initialization.

This module constructs the main API router by including all endpoint modules.
Routes are exposed under `/api/...` without versioning.
"""

from fastapi import APIRouter

from app.api import health, sample_endpoints

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="", tags=["health"])
api_router.include_router(sample_endpoints.router, prefix="", tags=["sample"])

__all__ = ["api_router"]
