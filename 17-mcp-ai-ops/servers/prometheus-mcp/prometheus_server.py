#!/usr/bin/env python3
"""
Prometheus MCP Server - Query metrics with AI

This MCP server allows Claude to query Prometheus metrics,
check service health, and analyze performance.
"""

import asyncio
import os
import requests
from datetime import datetime, timedelta
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Prometheus configuration
PROMETHEUS_URL = os.getenv('PROMETHEUS_URL', 'http://localhost:9090')

app = Server("prometheus-mcp")

def query_prometheus(query: str):
    """Execute a PromQL query"""
    try:
        url = f"{PROMETHEUS_URL}/api/v1/query"
        params = {'query': query}

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data['status'] == 'success':
            return {
                "success": True,
                "result": data['data']['result']
            }
        else:
            return {
                "success": False,
                "error": data.get('error', 'Unknown error')
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def query_prometheus_range(query: str, duration: str = "1h"):
    """Execute a PromQL range query"""
    try:
        url = f"{PROMETHEUS_URL}/api/v1/query_range"

        end = datetime.now()
        if duration.endswith('h'):
            hours = int(duration[:-1])
            start = end - timedelta(hours=hours)
        elif duration.endswith('m'):
            minutes = int(duration[:-1])
            start = end - timedelta(minutes=minutes)
        else:
            start = end - timedelta(hours=1)

        params = {
            'query': query,
            'start': start.timestamp(),
            'end': end.timestamp(),
            'step': '30s'
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data['status'] == 'success':
            return {
                "success": True,
                "result": data['data']['result']
            }
        else:
            return {
                "success": False,
                "error": data.get('error', 'Unknown error')
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="query_metrics",
            description="Execute a PromQL query to get current metric values",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "PromQL query (e.g., 'up', 'rate(http_requests_total[5m])')"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="query_metrics_range",
            description="Execute a PromQL range query to get metrics over time",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "PromQL query"
                    },
                    "duration": {
                        "type": "string",
                        "description": "Time range (e.g., '1h', '30m', '24h')",
                        "default": "1h"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="check_service_health",
            description="Check if a service is healthy (up metric = 1)",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "description": "Service name to check"
                    }
                },
                "required": ["service"]
            }
        ),
        Tool(
            name="get_error_rate",
            description="Get the error rate for a service over the last 5 minutes",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "description": "Service name"
                    }
                },
                "required": ["service"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""

    if name == "query_metrics":
        query = arguments.get("query", "")
        result = query_prometheus(query)

        if result.get('success'):
            metrics = result.get('result', [])
            if metrics:
                output = "Metrics:\n"
                for metric in metrics:
                    labels = metric.get('metric', {})
                    value = metric.get('value', [None, None])[1]
                    output += f"  {labels}: {value}\n"
            else:
                output = "No metrics found"
        else:
            output = f"Error: {result.get('error')}"

        return [TextContent(type="text", text=output)]

    elif name == "query_metrics_range":
        query = arguments.get("query", "")
        duration = arguments.get("duration", "1h")
        result = query_prometheus_range(query, duration)

        if result.get('success'):
            metrics = result.get('result', [])
            if metrics:
                output = f"Metrics over {duration}:\n"
                for metric in metrics:
                    labels = metric.get('metric', {})
                    values = metric.get('values', [])
                    output += f"  {labels}: {len(values)} data points\n"
                    if values:
                        latest = values[-1][1]
                        output += f"    Latest value: {latest}\n"
            else:
                output = "No metrics found"
        else:
            output = f"Error: {result.get('error')}"

        return [TextContent(type="text", text=output)]

    elif name == "check_service_health":
        service = arguments.get("service", "")
        query = f'up{{job="{service}"}}'
        result = query_prometheus(query)

        if result.get('success'):
            metrics = result.get('result', [])
            if metrics:
                value = metrics[0].get('value', [None, None])[1]
                if value == '1':
                    output = f"✅ Service '{service}' is UP"
                else:
                    output = f"❌ Service '{service}' is DOWN"
            else:
                output = f"⚠️ Service '{service}' not found"
        else:
            output = f"Error: {result.get('error')}"

        return [TextContent(type="text", text=output)]

    elif name == "get_error_rate":
        service = arguments.get("service", "")
        query = f'rate(http_requests_total{{job="{service}",status=~"5.."}}[5m])'
        result = query_prometheus(query)

        if result.get('success'):
            metrics = result.get('result', [])
            if metrics:
                value = float(metrics[0].get('value', [None, 0])[1])
                output = f"Error rate for '{service}': {value:.4f} errors/sec"
            else:
                output = f"No errors for '{service}' (or service not found)"
        else:
            output = f"Error: {result.get('error')}"

        return [TextContent(type="text", text=output)]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
