"""Test configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_user_data() -> dict:
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.fixture
def sample_post_data() -> dict:
    """Sample post data for testing."""
    return {
        "title": "Test Post",
        "content": "This is a test post",
        "published": False,
        "author_id": "test-author-id",
    }
