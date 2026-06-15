"""Test fixtures and utilities."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import get_db
from backend.api.main import app
from backend.models.schemas import Base
from fastapi.testclient import TestClient


@pytest.fixture
def test_db():
    """Create a test database."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal()
    
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_db):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_execution_data():
    """Sample execution data for testing."""
    return {
        "agent_name": "test-agent",
        "tool_name": "test-tool",
        "inference_time_ms": 1000.0,
        "tokens_input": 100,
        "tokens_output": 50,
        "status": "success",
        "model": "gpt-4",
    }
