"""Main FastAPI application."""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import os
from dotenv import load_dotenv

from backend.database import get_db, init_db
from backend.models.schemas import AgentExecution
from backend.models.api_models import (
    ExecutionRequest,
    ExecutionResponse,
    MetricsResponse,
    HealthResponse,
)
from backend.core.metrics import MetricsCalculator

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Agent Performance Monitor",
    description="Monitor and analyze AI agent performance metrics",
    version="0.1.0",
)

# CORS configuration
cors_origins = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.utcnow(),
    )


@app.post("/api/v1/executions", response_model=ExecutionResponse)
async def log_execution(
    execution: ExecutionRequest,
    db: Session = Depends(get_db),
):
    """Log agent execution.
    
    Args:
        execution: Execution data
        db: Database session
        
    Returns:
        Created execution record
    """
    # Create execution record
    db_execution = AgentExecution(
        agent_name=execution.agent_name,
        tool_name=execution.tool_name,
        inference_time_ms=execution.inference_time_ms,
        tokens_input=execution.tokens_input,
        tokens_output=execution.tokens_output,
        status=execution.status,
        error_message=execution.error_message,
        model=execution.model,
        metadata=execution.metadata,
    )
    
    db.add(db_execution)
    db.commit()
    db.refresh(db_execution)
    
    return db_execution


@app.get("/api/v1/metrics/{agent_name}", response_model=MetricsResponse)
async def get_metrics(
    agent_name: str,
    tool_name: Optional[str] = None,
    time_range: str = "24h",
    db: Session = Depends(get_db),
):
    """Get performance metrics for an agent.
    
    Args:
        agent_name: Name of the agent
        tool_name: Optional tool name filter
        time_range: Time range for metrics (24h, 7d, 30d)
        db: Database session
        
    Returns:
        Aggregated performance metrics
        
    Raises:
        HTTPException: If no executions found
    """
    # Parse time range
    hours_map = {"24h": 24, "7d": 168, "30d": 720}
    hours = hours_map.get(time_range, 24)
    since = datetime.utcnow() - timedelta(hours=hours)
    
    # Query executions
    query = db.query(AgentExecution).filter(
        AgentExecution.agent_name == agent_name,
        AgentExecution.created_at >= since,
    )
    
    if tool_name:
        query = query.filter(AgentExecution.tool_name == tool_name)
    
    executions = query.all()
    
    if not executions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No executions found for agent: {agent_name}",
        )
    
    # Convert to dict for aggregation
    execution_dicts = [
        {
            "agent_name": e.agent_name,
            "tool_name": e.tool_name,
            "inference_time_ms": e.inference_time_ms,
            "tokens_input": e.tokens_input,
            "tokens_output": e.tokens_output,
            "status": e.status,
        }
        for e in executions
    ]
    
    # Calculate metrics
    metrics = MetricsCalculator.aggregate_metrics(execution_dicts, time_range)
    
    return MetricsResponse(
        agent_name=metrics.agent_name,
        tool_name=metrics.tool_name,
        execution_count=metrics.execution_count,
        success_count=metrics.success_count,
        failure_count=metrics.failure_count,
        success_rate=metrics.success_rate,
        avg_inference_time_ms=metrics.avg_inference_time_ms,
        min_inference_time_ms=metrics.min_inference_time_ms,
        max_inference_time_ms=metrics.max_inference_time_ms,
        p50_inference_time_ms=metrics.p50_inference_time_ms,
        p95_inference_time_ms=metrics.p95_inference_time_ms,
        p99_inference_time_ms=metrics.p99_inference_time_ms,
        total_tokens_input=metrics.total_tokens_input,
        total_tokens_output=metrics.total_tokens_output,
        total_tokens=metrics.total_tokens,
        avg_tokens_input=metrics.avg_tokens_input,
        avg_tokens_output=metrics.avg_tokens_output,
        avg_tokens_total=metrics.avg_tokens_total,
        time_window=metrics.time_window,
        timestamp=metrics.timestamp,
    )


@app.get("/api/v1/agents", response_model=List[str])
async def get_agents(db: Session = Depends(get_db)):
    """Get list of all agents with executions.
    
    Args:
        db: Database session
        
    Returns:
        List of agent names
    """
    agents = db.query(AgentExecution.agent_name).distinct().all()
    return [agent[0] for agent in agents]


@app.get("/api/v1/tools", response_model=List[str])
async def get_tools(db: Session = Depends(get_db)):
    """Get list of all tools used.
    
    Args:
        db: Database session
        
    Returns:
        List of tool names
    """
    tools = db.query(AgentExecution.tool_name).distinct().filter(
        AgentExecution.tool_name.isnot(None)
    ).all()
    return [tool[0] for tool in tools]


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        workers=int(os.getenv("API_WORKERS", 4)),
    )
