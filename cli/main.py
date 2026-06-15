"""CLI interface for Agent Performance Monitor."""

import click
from sdk.python import PerformanceMonitor
import json
from tabulate import tabulate


@click.group()
@click.option(
    "--api-url",
    default="http://localhost:8000",
    help="Base URL of the APM API",
)
@click.option(
    "--api-key",
    default=None,
    help="API key for authentication",
)
@click.pass_context
def cli(ctx, api_url, api_key):
    """Agent Performance Monitor CLI."""
    ctx.ensure_object(dict)
    ctx.obj["monitor"] = PerformanceMonitor(api_url=api_url, api_key=api_key)


@cli.command()
@click.pass_context
def status(ctx):
    """Check API health status."""
    monitor = ctx.obj["monitor"]
    try:
        health = monitor.health_check()
        click.echo(f"✓ Status: {health['status']}")
        click.echo(f"✓ Version: {health['version']}")
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)


@cli.command()
@click.argument("agent_name")
@click.option(
    "--time-range",
    default="24h",
    help="Time range for metrics (24h, 7d, 30d)",
)
@click.pass_context
def metrics(ctx, agent_name, time_range):
    """Get metrics for an agent."""
    monitor = ctx.obj["monitor"]
    try:
        metrics = monitor.get_metrics(agent_name, time_range=time_range)
        
        data = [
            ["Executions", metrics.execution_count],
            ["Success", metrics.success_count],
            ["Failures", metrics.failure_count],
            ["Success Rate", f"{metrics.success_rate:.1f}%"],
            ["Avg Inference Time", f"{metrics.avg_inference_time_ms:.2f}ms"],
            ["Total Tokens", metrics.total_tokens],
        ]
        
        click.echo(f"\n📊 Metrics for {agent_name} ({time_range})\n")
        click.echo(tabulate(data, headers=["Metric", "Value"], tablefmt="grid"))
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)


@cli.command()
@click.pass_context
def agents(ctx):
    """List all agents."""
    monitor = ctx.obj["monitor"]
    try:
        agent_list = monitor.get_agents()
        click.echo("\n🤖 Registered Agents:\n")
        for agent in agent_list:
            click.echo(f"  • {agent}")
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)


@cli.command()
@click.pass_context
def tools(ctx):
    """List all tools."""
    monitor = ctx.obj["monitor"]
    try:
        tool_list = monitor.get_tools()
        click.echo("\n🔧 Available Tools:\n")
        for tool in tool_list:
            click.echo(f"  • {tool}")
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)


@cli.command()
@click.option(
    "--agent-name",
    prompt="Agent name",
    help="Name of the agent",
)
@click.option(
    "--tool-name",
    default=None,
    help="Name of the tool",
)
@click.option(
    "--inference-time",
    type=float,
    prompt="Inference time (ms)",
    help="Inference time in milliseconds",
)
@click.option(
    "--tokens-input",
    type=int,
    prompt="Input tokens",
    help="Number of input tokens",
)
@click.option(
    "--tokens-output",
    type=int,
    prompt="Output tokens",
    help="Number of output tokens",
)
@click.option(
    "--status",
    type=click.Choice(["success", "error", "timeout"]),
    default="success",
    help="Execution status",
)
@click.pass_context
def log(ctx, agent_name, tool_name, inference_time, tokens_input, tokens_output, status):
    """Log an execution."""
    monitor = ctx.obj["monitor"]
    try:
        result = monitor.log_execution(
            agent_name=agent_name,
            tool_name=tool_name,
            inference_time_ms=inference_time,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            status=status,
        )
        click.echo(f"\n✓ Execution logged with ID: {result['id']}\n")
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)


if __name__ == "__main__":
    cli(obj={})
