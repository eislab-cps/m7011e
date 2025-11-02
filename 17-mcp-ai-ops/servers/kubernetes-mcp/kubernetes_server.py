#!/usr/bin/env python3
"""
Kubernetes MCP Server - Manage K8s resources with AI

This MCP server allows Claude to query Kubernetes resources,
check pod status, view logs, and more.
"""

import asyncio
import subprocess
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("kubernetes-mcp")

def run_kubectl(args: list[str]):
    """Execute kubectl command"""
    try:
        cmd = ['kubectl'] + args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return {
                "success": True,
                "output": result.stdout
            }
        else:
            return {
                "success": False,
                "error": result.stderr
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
            name="get_pods",
            description="List all pods in a namespace",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {
                        "type": "string",
                        "description": "Namespace (default: default)",
                        "default": "default"
                    }
                }
            }
        ),
        Tool(
            name="get_pod_logs",
            description="Get logs from a specific pod",
            inputSchema={
                "type": "object",
                "properties": {
                    "pod_name": {
                        "type": "string",
                        "description": "Name of the pod"
                    },
                    "namespace": {
                        "type": "string",
                        "description": "Namespace (default: default)",
                        "default": "default"
                    },
                    "tail": {
                        "type": "integer",
                        "description": "Number of lines to show (default: 50)",
                        "default": 50
                    }
                },
                "required": ["pod_name"]
            }
        ),
        Tool(
            name="describe_pod",
            description="Get detailed information about a pod",
            inputSchema={
                "type": "object",
                "properties": {
                    "pod_name": {
                        "type": "string",
                        "description": "Name of the pod"
                    },
                    "namespace": {
                        "type": "string",
                        "description": "Namespace (default: default)",
                        "default": "default"
                    }
                },
                "required": ["pod_name"]
            }
        ),
        Tool(
            name="get_services",
            description="List all services in a namespace",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {
                        "type": "string",
                        "description": "Namespace (default: default)",
                        "default": "default"
                    }
                }
            }
        ),
        Tool(
            name="get_deployments",
            description="List all deployments in a namespace",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {
                        "type": "string",
                        "description": "Namespace (default: default)",
                        "default": "default"
                    }
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""

    if name == "get_pods":
        namespace = arguments.get("namespace", "default")
        result = run_kubectl(['get', 'pods', '-n', namespace, '-o', 'wide'])

        if result.get('success'):
            output = f"Pods in namespace '{namespace}':\n{result.get('output')}"
        else:
            output = f"Error: {result.get('error')}"

        return [TextContent(type="text", text=output)]

    elif name == "get_pod_logs":
        pod_name = arguments.get("pod_name", "")
        namespace = arguments.get("namespace", "default")
        tail = arguments.get("tail", 50)

        result = run_kubectl([
            'logs',
            pod_name,
            '-n', namespace,
            '--tail', str(tail)
        ])

        if result.get('success'):
            output = f"Logs for pod '{pod_name}':\n{result.get('output')}"
        else:
            output = f"Error: {result.get('error')}"

        return [TextContent(type="text", text=output)]

    elif name == "describe_pod":
        pod_name = arguments.get("pod_name", "")
        namespace = arguments.get("namespace", "default")

        result = run_kubectl(['describe', 'pod', pod_name, '-n', namespace])

        if result.get('success'):
            output = f"Description of pod '{pod_name}':\n{result.get('output')}"
        else:
            output = f"Error: {result.get('error')}"

        return [TextContent(type="text", text=output)]

    elif name == "get_services":
        namespace = arguments.get("namespace", "default")
        result = run_kubectl(['get', 'services', '-n', namespace, '-o', 'wide'])

        if result.get('success'):
            output = f"Services in namespace '{namespace}':\n{result.get('output')}"
        else:
            output = f"Error: {result.get('error')}"

        return [TextContent(type="text", text=output)]

    elif name == "get_deployments":
        namespace = arguments.get("namespace", "default")
        result = run_kubectl(['get', 'deployments', '-n', namespace, '-o', 'wide'])

        if result.get('success'):
            output = f"Deployments in namespace '{namespace}':\n{result.get('output')}"
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
