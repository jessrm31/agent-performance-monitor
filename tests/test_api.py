"""API endpoint tests."""

import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"


def test_log_execution(client: TestClient, sample_execution_data: dict):
    """Test logging an execution."""
    response = client.post("/api/v1/executions", json=sample_execution_data)
    assert response.status_code == 200
    data = response.json()
    assert data["agent_name"] == "test-agent"
    assert data["status"] == "success"
    assert "id" in data
    assert "created_at" in data


def test_log_execution_invalid_status(client: TestClient, sample_execution_data: dict):
    """Test logging with invalid status."""
    sample_execution_data["status"] = "invalid"
    response = client.post("/api/v1/executions", json=sample_execution_data)
    assert response.status_code == 422  # Validation error


def test_log_execution_missing_required_field(client: TestClient):
    """Test logging without required field."""
    data = {
        "agent_name": "test-agent",
        # Missing required fields
    }
    response = client.post("/api/v1/executions", json=data)
    assert response.status_code == 422  # Validation error


def test_get_metrics(client: TestClient, sample_execution_data: dict):
    """Test getting metrics."""
    # Log some executions
    for i in range(5):
        client.post("/api/v1/executions", json=sample_execution_data)
    
    # Get metrics
    response = client.get("/api/v1/metrics/test-agent?time_range=24h")
    assert response.status_code == 200
    data = response.json()
    assert data["agent_name"] == "test-agent"
    assert data["execution_count"] == 5
    assert data["success_count"] == 5
    assert data["success_rate"] == 100.0


def test_get_metrics_nonexistent_agent(client: TestClient):
    """Test getting metrics for nonexistent agent."""
    response = client.get("/api/v1/metrics/nonexistent")
    assert response.status_code == 404


def test_get_agents(client: TestClient, sample_execution_data: dict):
    """Test getting list of agents."""
    # Log execution
    client.post("/api/v1/executions", json=sample_execution_data)
    
    # Get agents
    response = client.get("/api/v1/agents")
    assert response.status_code == 200
    data = response.json()
    assert "test-agent" in data


def test_get_tools(client: TestClient, sample_execution_data: dict):
    """Test getting list of tools."""
    # Log execution
    client.post("/api/v1/executions", json=sample_execution_data)
    
    # Get tools
    response = client.get("/api/v1/tools")
    assert response.status_code == 200
    data = response.json()
    assert "test-tool" in data
