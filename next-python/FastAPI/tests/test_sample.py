"""Sample test file.

This file contains sample tests that can be copied and modified
for your own test cases.
"""

import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_root_endpoint() -> None:
    """Test root endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "version" in response.json()


@pytest.mark.asyncio
async def test_health_check() -> None:
    """Test health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_api_health_check() -> None:
    """Test API health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_ping() -> None:
    """Test ping endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/ping")
        assert response.status_code == 200
        assert response.json()["message"] == "pong"
