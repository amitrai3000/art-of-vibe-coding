"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client.

    Returns:
        FastAPI test client
    """
    return TestClient(app)


@pytest.fixture
def mock_user_id():
    """Mock user ID for testing.

    Returns:
        Mock UUID string
    """
    return "00000000-0000-0000-0000-000000000001"


@pytest.fixture
def mock_jwt_token():
    """Mock JWT token for testing.

    Returns:
        Mock JWT token string
    """
    # This should be a valid JWT for testing
    # In real tests, use a proper JWT library
    return "mock_jwt_token"
