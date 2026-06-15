"""API models and schemas."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ExecutionRequest(BaseModel):
    """Request model for logging execution."""

    agent_name: str = Field(..., min_length=1, max_length=255)
    tool_name: Optional[str] = Field(None, max_length=255)
    inference_time_ms: float = Field(..., gt=0)
    tokens_input: int = Field(..., ge=0)
    tokens_output: int = Field(..., ge=0)
    status: str = Field("success", regex="^(success|error|timeout)$")
    error_message: Optional[str] = Field(None, max_length=1000)
    model: Optional[str] = Field(None, max_length=255)
    metadata: Optional[Dict[str, Any]] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "agent_name": "github-copilot-python",
                "tool_name": "code_generation",
                "inference_time_ms": 1250.5,
                "tokens_input": 450,
                "tokens_output": 320,
                "status": "success",
                "model": "gpt-4",
                "metadata": {"temperature": 0.7, "top_p": 0.9},
            }
        }


class ExecutionResponse(BaseModel):
    """Response model for execution."""

    id: int
    agent_name: str
    tool_name: Optional[str]
    inference_time_ms: float
    tokens_input: int
    tokens_output: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class MetricsResponse(BaseModel):
    """Response model for metrics."""

    agent_name: str
    tool_name: Optional[str]
    execution_count: int
    success_count: int
    failure_count: int
    success_rate: float
    avg_inference_time_ms: float
    min_inference_time_ms: float
    max_inference_time_ms: float
    p50_inference_time_ms: float
    p95_inference_time_ms: float
    p99_inference_time_ms: float
    total_tokens_input: int
    total_tokens_output: int
    total_tokens: int
    avg_tokens_input: float
    avg_tokens_output: float
    avg_tokens_total: float
    time_window: str
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "agent_name": "github-copilot-python",
                "tool_name": "code_generation",
                "execution_count": 100,
                "success_count": 98,
                "failure_count": 2,
                "success_rate": 98.0,
                "avg_inference_time_ms": 1250.5,
                "min_inference_time_ms": 800.0,
                "max_inference_time_ms": 2500.0,
                "p50_inference_time_ms": 1200.0,
                "p95_inference_time_ms": 2000.0,
                "p99_inference_time_ms": 2400.0,
                "total_tokens_input": 45000,
                "total_tokens_output": 32000,
                "total_tokens": 77000,
                "avg_tokens_input": 450.0,
                "avg_tokens_output": 320.0,
                "avg_tokens_total": 770.0,
                "time_window": "24h",
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str
    version: str
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "0.1.0",
                "timestamp": "2024-06-15T10:30:00Z",
            }
        }
