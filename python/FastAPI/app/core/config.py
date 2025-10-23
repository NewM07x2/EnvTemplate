"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import Any
import json

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = Field(default="FastAPI Template", description="Application name")
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    APP_ENV: str = Field(default="development", description="Application environment")
    DEBUG: bool = Field(default=True, description="Debug mode")

    # Server
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")

    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./app.db",
        description="Database connection URL",
    )

    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT encoding",
    )
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time in minutes",
    )

    # CORS
    ALLOWED_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed origins for CORS",
    )
    ALLOWED_METHODS: list[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "PATCH"],
        description="Allowed methods for CORS",
    )
    ALLOWED_HEADERS: list[str] = Field(
        default=["*"],
        description="Allowed headers for CORS",
    )

    # Redis (Optional)
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL",
    )

    # Celery (Optional)
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Celery broker URL",
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/0",
        description="Celery result backend URL",
    )

    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Parse CORS origins from string or list."""
        # Accept None -> return empty list (no origins)
        if v is None:
            return []

        # Already a list (e.g., set via environment in some systems)
        if isinstance(v, (list, tuple)):
            return [str(x).strip() for x in v]

        # If it's a string, try several common formats
        if isinstance(v, str):
            raw = v.strip()
            if raw == "":
                return []
            # JSON array: ["http://...","http://..."]
            if raw.startswith("[") and raw.endswith("]"):
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, list):
                        return [str(x).strip() for x in parsed]
                except Exception:
                    # fallthrough to comma-split
                    pass
            # Comma-separated
            return [origin.strip() for origin in raw.split(",") if origin.strip()]

        # Fallback: cast to string and split
        try:
            return [origin.strip() for origin in str(v).split(",") if origin is not None]
        except Exception:
            return []

    @field_validator("ALLOWED_METHODS", mode="before")
    @classmethod
    def parse_cors_methods(cls, v: Any) -> list[str]:
        """Parse CORS methods from string or list."""
        if v is None:
            return []
        if isinstance(v, (list, tuple)):
            return [str(x).strip() for x in v]
        if isinstance(v, str):
            raw = v.strip()
            if raw == "":
                return []
            return [method.strip() for method in raw.split(",") if method.strip()]
        try:
            return [m.strip() for m in str(v).split(",")]
        except Exception:
            return []

    @field_validator("ALLOWED_HEADERS", mode="before")
    @classmethod
    def parse_cors_headers(cls, v: Any) -> list[str]:
        """Parse CORS headers from string or list."""
        if v is None:
            return []
        if isinstance(v, (list, tuple)):
            return [str(x).strip() for x in v]
        if isinstance(v, str):
            raw = v.strip()
            if raw == "":
                return []
            return [header.strip() for header in raw.split(",") if header.strip()]
        try:
            return [h.strip() for h in str(v).split(",")]
        except Exception:
            return []


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
