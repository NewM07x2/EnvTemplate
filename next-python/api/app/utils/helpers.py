"""Utility functions for the application."""

import logging
from datetime import datetime, timezone
from typing import Any, Optional


def get_utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def setup_logging(log_level: str = "INFO") -> None:
    """
    Setup application logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def sanitize_dict(data: dict[str, Any], remove_keys: Optional[list[str]] = None) -> dict[str, Any]:
    """
    Remove sensitive keys from dictionary.
    
    Args:
        data: Dictionary to sanitize
        remove_keys: List of keys to remove (default: ["password"])
        
    Returns:
        Sanitized dictionary
    """
    if remove_keys is None:
        remove_keys = ["password"]
    
    return {k: v for k, v in data.items() if k not in remove_keys}
