"""API v1 router configuration."""

from fastapi import APIRouter

from app.api.v1 import health, sample_endpoints

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="", tags=["health"])
api_router.include_router(sample_endpoints.router, prefix="", tags=["sample"])
