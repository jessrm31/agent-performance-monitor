"""Metrics calculation tests."""

import pytest
from backend.core.metrics import MetricsCalculator, PerformanceMetrics


def test_calculate_percentile():
    """Test percentile calculation."""
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    p50 = MetricsCalculator.calculate_percentile(values, 50)
    assert 5 <= p50 <= 6  # Median
    
    p95 = MetricsCalculator.calculate_percentile(values, 95)
    assert 9 <= p95 <= 10
    
    p99 = MetricsCalculator.calculate_percentile(values, 99)
    assert 9.9 <= p99 <= 10


def test_calculate_percentile_empty():
    """Test percentile with empty list."""
    result = MetricsCalculator.calculate_percentile([], 50)
    assert result == 0.0


def test_aggregate_metrics():
    """Test metrics aggregation."""
    executions = [
        {
            "agent_name": "test-agent",
            "tool_name": "test-tool",
            "inference_time_ms": 1000.0,
            "tokens_input": 100,
            "tokens_output": 50,
            "status": "success",
        },
        {
            "agent_name": "test-agent",
            "tool_name": "test-tool",
            "inference_time_ms": 1500.0,
            "tokens_input": 150,
            "tokens_output": 75,
            "status": "success",
        },
        {
            "agent_name": "test-agent",
            "tool_name": "test-tool",
            "inference_time_ms": 500.0,
            "tokens_input": 50,
            "tokens_output": 25,
            "status": "error",
        },
    ]
    
    metrics = MetricsCalculator.aggregate_metrics(executions)
    
    assert metrics.agent_name == "test-agent"
    assert metrics.execution_count == 3
    assert metrics.success_count == 2
    assert metrics.failure_count == 1
    assert metrics.success_rate == pytest.approx(66.67, 0.1)
    assert metrics.total_tokens_input == 300
    assert metrics.total_tokens_output == 150
    assert metrics.total_tokens == 450
    assert metrics.avg_tokens_input == pytest.approx(100.0)
    assert metrics.avg_tokens_output == pytest.approx(50.0)


def test_aggregate_metrics_empty():
    """Test aggregation with empty list."""
    metrics = MetricsCalculator.aggregate_metrics([])
    
    assert metrics.agent_name == "unknown"
    assert metrics.execution_count == 0
    assert metrics.success_count == 0
    assert metrics.failure_count == 0


def test_estimate_cost():
    """Test cost estimation."""
    # GPT-4: input $0.03/1M, output $0.06/1M
    cost = MetricsCalculator.estimate_cost(1000, 1000, "gpt-4")
    assert cost > 0
    assert cost == pytest.approx(0.000090, abs=0.000001)


def test_estimate_cost_different_models():
    """Test cost estimation for different models."""
    cost_gpt4 = MetricsCalculator.estimate_cost(1000, 1000, "gpt-4")
    cost_gpt35 = MetricsCalculator.estimate_cost(1000, 1000, "gpt-3.5-turbo")
    
    # GPT-3.5 should be cheaper
    assert cost_gpt35 < cost_gpt4
