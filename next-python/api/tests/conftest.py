"""
Shared test fixtures and configuration for FastAPI pytest tests.

This module provides:
- TestClient for API testing
- Async test fixtures
- Mock Prisma client
- GraphQL test utilities
- Database setup/teardown
"""

import os
from typing import AsyncGenerator
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock

from main import app


# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

@pytest.fixture(scope="session")
def test_env():
    """Set up test environment variables."""
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "postgresql://test:test@localhost:5432/test_db")
    os.environ["JWT_SECRET"] = os.getenv("JWT_SECRET", "test-secret-key-for-testing-only")
    os.environ["JWT_ALGORITHM"] = "HS256"
    yield
    # Cleanup (optional)


# ============================================================================
# API CLIENT FIXTURES
# ============================================================================

@pytest.fixture
def client(test_env) -> TestClient:
    """
    Provide a TestClient for synchronous API testing.
    
    Usage:
        def test_get_items(client):
            response = client.get("/api/items")
            assert response.status_code == 200
    """
    return TestClient(app)


@pytest.fixture
async def async_client(test_env) -> AsyncGenerator:
    """
    Provide an AsyncClient for asynchronous API testing.
    
    Usage:
        async def test_get_items_async(async_client):
            async with async_client as client:
                response = await client.get("/api/items")
                assert response.status_code == 200
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture
def mock_prisma_client():
    """
    Provide a mocked Prisma client for testing database operations.
    
    Usage:
        def test_repository(mock_prisma_client):
            mock_prisma_client.user.find_first.return_value = {"id": 1, "email": "test@example.com"}
            # Test code here
    """
    prisma_client = AsyncMock()
    prisma_client.user = MagicMock()
    prisma_client.post = MagicMock()
    prisma_client.comment = MagicMock()
    
    return prisma_client


@pytest.fixture
async def db_transaction():
    """
    Provide a database transaction context for tests.
    This fixture ensures each test is isolated and can be rolled back.
    
    Usage:
        async def test_create_user(db_transaction):
            async with db_transaction:
                # Database operations here
                pass
    """
    # This is a template - implement based on your database setup
    class TransactionContext:
        async def __aenter__(self):
            # Setup transaction
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            # Rollback transaction
            pass
    
    yield TransactionContext()


# ============================================================================
# DATA FIXTURES (Test Data Builders)
# ============================================================================

@pytest.fixture
def sample_user_data() -> dict:
    """Provide sample user data for tests."""
    return {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password_hash": "$2b$12$...",  # Hashed password
        "is_active": True,
        "created_at": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_post_data() -> dict:
    """Provide sample post data for tests."""
    return {
        "id": 1,
        "title": "Test Post",
        "content": "This is a test post",
        "author_id": 1,
        "published": True,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
    }


# ============================================================================
# GRAPHQL TEST FIXTURES
# ============================================================================

@pytest.fixture
def graphql_query():
    """
    Provide a helper function to construct GraphQL queries for testing.
    
    Usage:
        def test_graphql_query(client, graphql_query):
            query = graphql_query("query { users { id email } }")
            response = client.post("/graphql", json={"query": query})
            assert response.status_code == 200
    """
    def _graphql_query(query_string: str, variables: dict = None) -> dict:
        return {
            "query": query_string,
            "variables": variables or {},
        }
    
    return _graphql_query


@pytest.fixture
def mock_graphql_context():
    """
    Provide a mocked GraphQL context for resolver testing.
    
    Usage:
        async def test_user_resolver(mock_graphql_context):
            # GraphQL resolver test code
            pass
    """
    context = {
        "request": MagicMock(),
        "user": MagicMock(),
        "db": AsyncMock(),
    }
    return context


# ============================================================================
# AUTHENTICATION FIXTURES
# ============================================================================

@pytest.fixture
def auth_headers() -> dict:
    """
    Provide valid authentication headers for testing protected endpoints.
    
    Usage:
        def test_protected_endpoint(client, auth_headers):
            response = client.get("/api/protected", headers=auth_headers)
            assert response.status_code == 200
    """
    # Replace with actual JWT token generation for your app
    return {
        "Authorization": "Bearer test-token-12345",
        "Content-Type": "application/json",
    }


@pytest.fixture
def invalid_auth_headers() -> dict:
    """Provide invalid authentication headers for testing auth failures."""
    return {
        "Authorization": "Bearer invalid-token",
        "Content-Type": "application/json",
    }


# ============================================================================
# SERVICE MOCKING FIXTURES
# ============================================================================

@pytest.fixture
def mock_email_service():
    """
    Mock email service for testing email-related functionality.
    
    Usage:
        def test_send_email(mock_email_service):
            mock_email_service.send.return_value = True
            # Test code here
    """
    service = AsyncMock()
    service.send = AsyncMock(return_value=True)
    service.send_bulk = AsyncMock(return_value={"sent": 5})
    return service


@pytest.fixture
def mock_cache_service():
    """
    Mock cache service for testing caching functionality.
    
    Usage:
        def test_cache(mock_cache_service):
            mock_cache_service.get.return_value = None
            mock_cache_service.set.return_value = True
            # Test code here
    """
    service = AsyncMock()
    service.get = AsyncMock(return_value=None)
    service.set = AsyncMock(return_value=True)
    service.delete = AsyncMock(return_value=True)
    service.clear = AsyncMock(return_value=True)
    return service


# ============================================================================
# FIXTURE SCOPE MARKERS
# ============================================================================

def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line("markers", "asyncio: mark test as async")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "unit: mark test as unit test")
