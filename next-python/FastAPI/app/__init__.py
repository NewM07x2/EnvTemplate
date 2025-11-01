"""Application package initialization."""

from app.core.config import settings

__version__ = settings.APP_VERSION
__all__ = ["settings"]
