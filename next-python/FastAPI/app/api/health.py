"""Health check endpoint."""

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
    }


@router.get("/ping", tags=["health"])
async def ping() -> dict[str, str]:
    """Simple ping endpoint."""
    return {"message": "pong"}
