"""Tests for chat endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test health check endpoint.

    Args:
        client: FastAPI test client
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_readiness_check(client: TestClient):
    """Test readiness check endpoint.

    Args:
        client: FastAPI test client
    """
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


# TODO: Add more comprehensive tests for chat endpoints
# These will require mocking Supabase, AI providers, etc.
