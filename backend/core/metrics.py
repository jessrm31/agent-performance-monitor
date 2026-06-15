"""Performance metrics calculation and aggregation."""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import statistics


@dataclass
class PerformanceMetrics:
    """Performance metrics for agent executions."""
    
    agent_name: str
    tool_name: Optional[str] = None
    execution_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    avg_inference_time_ms: float = 0.0
    min_inference_time_ms: float = 0.0
    max_inference_time_ms: float = 0.0
    p50_inference_time_ms: float = 0.0
    p95_inference_time_ms: float = 0.0
    p99_inference_time_ms: float = 0.0
    total_tokens_input: int = 0
    total_tokens_output: int = 0
    total_tokens: int = 0
    avg_tokens_input: float = 0.0
    avg_tokens_output: float = 0.0
    avg_tokens_total: float = 0.0
    success_rate: float = 0.0
    timestamp: datetime = None
    time_window: str = "24h"

    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class MetricsCalculator:
    """Calculator for performance metrics."""

    @staticmethod
    def calculate_percentile(values: List[float], percentile: float) -> float:
        """Calculate percentile from list of values.
        
        Args:
            values: List of numeric values
            percentile: Percentile to calculate (0-100)
            
        Returns:
            Percentile value
        """
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = (percentile / 100) * (len(sorted_values) - 1)
        lower = int(index)
        upper = lower + 1
        
        if upper >= len(sorted_values):
            return sorted_values[-1]
        
        weight = index - lower
        return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight

    @staticmethod
    def aggregate_metrics(
        executions: List[Dict],
        time_window: str = "24h"
    ) -> PerformanceMetrics:
        """Aggregate execution data into metrics.
        
        Args:
            executions: List of execution records
            time_window: Time window for aggregation
            
        Returns:
            Aggregated performance metrics
        """
        if not executions:
            return PerformanceMetrics(
                agent_name="unknown",
                time_window=time_window
            )

        # Extract data
        inference_times = []
        tokens_inputs = []
        tokens_outputs = []
        success_count = 0
        failure_count = 0
        agent_name = executions[0].get("agent_name", "unknown")
        tool_name = executions[0].get("tool_name")

        for execution in executions:
            # Inference time
            if "inference_time_ms" in execution:
                inference_times.append(execution["inference_time_ms"])

            # Tokens
            if "tokens_input" in execution:
                tokens_inputs.append(execution["tokens_input"])
            if "tokens_output" in execution:
                tokens_outputs.append(execution["tokens_output"])

            # Status
            if execution.get("status") == "success":
                success_count += 1
            else:
                failure_count += 1

        # Calculate metrics
        execution_count = len(executions)
        total_tokens_input = sum(tokens_inputs)
        total_tokens_output = sum(tokens_outputs)
        total_tokens = total_tokens_input + total_tokens_output

        success_rate = (
            (success_count / execution_count * 100)
            if execution_count > 0
            else 0.0
        )

        avg_tokens_input = (
            total_tokens_input / execution_count if execution_count > 0 else 0.0
        )
        avg_tokens_output = (
            total_tokens_output / execution_count if execution_count > 0 else 0.0
        )
        avg_tokens_total = (
            total_tokens / execution_count if execution_count > 0 else 0.0
        )

        # Inference time statistics
        avg_inference_time_ms = (
            statistics.mean(inference_times) if inference_times else 0.0
        )
        min_inference_time_ms = min(inference_times) if inference_times else 0.0
        max_inference_time_ms = max(inference_times) if inference_times else 0.0
        p50_inference_time_ms = MetricsCalculator.calculate_percentile(
            inference_times, 50
        )
        p95_inference_time_ms = MetricsCalculator.calculate_percentile(
            inference_times, 95
        )
        p99_inference_time_ms = MetricsCalculator.calculate_percentile(
            inference_times, 99
        )

        return PerformanceMetrics(
            agent_name=agent_name,
            tool_name=tool_name,
            execution_count=execution_count,
            success_count=success_count,
            failure_count=failure_count,
            avg_inference_time_ms=avg_inference_time_ms,
            min_inference_time_ms=min_inference_time_ms,
            max_inference_time_ms=max_inference_time_ms,
            p50_inference_time_ms=p50_inference_time_ms,
            p95_inference_time_ms=p95_inference_time_ms,
            p99_inference_time_ms=p99_inference_time_ms,
            total_tokens_input=total_tokens_input,
            total_tokens_output=total_tokens_output,
            total_tokens=total_tokens,
            avg_tokens_input=avg_tokens_input,
            avg_tokens_output=avg_tokens_output,
            avg_tokens_total=avg_tokens_total,
            success_rate=success_rate,
            time_window=time_window,
        )

    @staticmethod
    def estimate_cost(
        tokens_input: int,
        tokens_output: int,
        model: str = "gpt-4"
    ) -> float:
        """Estimate cost of API call based on tokens.
        
        Args:
            tokens_input: Number of input tokens
            tokens_output: Number of output tokens
            model: Model name for pricing lookup
            
        Returns:
            Estimated cost in USD
        """
        # Pricing as of June 2024 (in USD per 1M tokens)
        pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
            "claude-3-opus": {"input": 0.015, "output": 0.075},
            "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        }

        model_pricing = pricing.get(model.lower(), pricing["gpt-4"])

        input_cost = (tokens_input / 1_000_000) * model_pricing["input"]
        output_cost = (tokens_output / 1_000_000) * model_pricing["output"]

        return round(input_cost + output_cost, 6)
