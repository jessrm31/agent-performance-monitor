"""Python SDK for Agent Performance Monitor."""

import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class MetricsData:
    """Metrics data container."""
    agent_name: str
    execution_count: int
    success_count: int
    failure_count: int
    success_rate: float
    avg_inference_time_ms: float
    total_tokens_input: int
    total_tokens_output: int
    total_tokens: int
    time_window: str


class PerformanceMonitor:
    """Client for Agent Performance Monitor.
    
    Example:
        >>> monitor = PerformanceMonitor()
        >>> monitor.log_execution(
        ...     agent_name="github-copilot-python",
        ...     tool_name="code_generation",
        ...     inference_time_ms=1250,
        ...     tokens_input=450,
        ...     tokens_output=320,
        ...     status="success"
        ... )
        >>> metrics = monitor.get_metrics("github-copilot-python")
        >>> print(f"Success rate: {metrics.success_rate}%")
    """

    def __init__(
        self,
        api_url: str = "http://localhost:8000",
        api_key: Optional[str] = None,
    ):
        """Initialize performance monitor.
        
        Args:
            api_url: Base URL of the APM API
            api_key: Optional API key for authentication
        """
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def log_execution(
        self,
        agent_name: str,
        tool_name: Optional[str] = None,
        inference_time_ms: float = 0.0,
        tokens_input: int = 0,
        tokens_output: int = 0,
        status: str = "success",
        error_message: Optional[str] = None,
        model: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Log an agent execution.
        
        Args:
            agent_name: Name of the agent
            tool_name: Name of the tool used
            inference_time_ms: Inference time in milliseconds
            tokens_input: Number of input tokens
            tokens_output: Number of output tokens
            status: Execution status (success, error, timeout)
            error_message: Error message if failed
            model: Model name used
            metadata: Additional metadata
            
        Returns:
            Response data
            
        Raises:
            requests.RequestException: If API call fails
        """
        payload = {
            "agent_name": agent_name,
            "tool_name": tool_name,
            "inference_time_ms": inference_time_ms,
            "tokens_input": tokens_input,
            "tokens_output": tokens_output,
            "status": status,
            "error_message": error_message,
            "model": model,
            "metadata": metadata,
        }
        
        response = self.session.post(
            f"{self.api_url}/api/v1/executions",
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    def get_metrics(
        self,
        agent_name: str,
        tool_name: Optional[str] = None,
        time_range: str = "24h",
    ) -> MetricsData:
        """Get performance metrics for an agent.
        
        Args:
            agent_name: Name of the agent
            tool_name: Optional tool name filter
            time_range: Time range for metrics (24h, 7d, 30d)
            
        Returns:
            Metrics data
            
        Raises:
            requests.RequestException: If API call fails
        """
        params = {"time_range": time_range}
        if tool_name:
            params["tool_name"] = tool_name
        
        response = self.session.get(
            f"{self.api_url}/api/v1/metrics/{agent_name}",
            params=params,
        )
        response.raise_for_status()
        data = response.json()
        
        return MetricsData(
            agent_name=data["agent_name"],
            execution_count=data["execution_count"],
            success_count=data["success_count"],
            failure_count=data["failure_count"],
            success_rate=data["success_rate"],
            avg_inference_time_ms=data["avg_inference_time_ms"],
            total_tokens_input=data["total_tokens_input"],
            total_tokens_output=data["total_tokens_output"],
            total_tokens=data["total_tokens"],
            time_window=data["time_window"],
        )

    def get_agents(self) -> list[str]:
        """Get list of all agents.
        
        Returns:
            List of agent names
            
        Raises:
            requests.RequestException: If API call fails
        """
        response = self.session.get(f"{self.api_url}/api/v1/agents")
        response.raise_for_status()
        return response.json()

    def get_tools(self) -> list[str]:
        """Get list of all tools.
        
        Returns:
            List of tool names
            
        Raises:
            requests.RequestException: If API call fails
        """
        response = self.session.get(f"{self.api_url}/api/v1/tools")
        response.raise_for_status()
        return response.json()

    def health_check(self) -> Dict[str, Any]:
        """Check API health.
        
        Returns:
            Health status
            
        Raises:
            requests.RequestException: If API call fails
        """
        response = self.session.get(f"{self.api_url}/health")
        response.raise_for_status()
        return response.json()
