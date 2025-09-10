"""Test API endpoints."""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from documcp.backend.main import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


def test_health_endpoint_without_model(client):
    """Test health endpoint when model is not loaded."""
    with patch("documcp.backend.api.generation.llm_service", None):
        response = client.get("/api/v1/health")
        assert response.status_code == 503


@pytest.mark.asyncio
async def test_generation_request_validation(client):
    """Test request validation for generation endpoint."""
    # Test empty input
    response = client.post("/api/v1/generate", json={"input_text": "", "document_types": ["prd"]})
    assert response.status_code == 400

    # Test too long input
    response = client.post("/api/v1/generate", json={"input_text": "x" * 20000, "document_types": ["prd"]})
    assert response.status_code == 400


def test_metrics_endpoint_without_model(client):
    """Test metrics endpoint when model is not loaded."""
    with patch("documcp.backend.api.generation.llm_service", None):
        response = client.get("/api/v1/metrics")
        assert response.status_code == 503
