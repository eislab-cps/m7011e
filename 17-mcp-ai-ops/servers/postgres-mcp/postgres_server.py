#!/usr/bin/env python3
"""
PostgreSQL MCP Server - Query your database with AI

This MCP server allows Claude to execute read-only SQL queries
against your PostgreSQL database from Tutorial 8.
"""

import asyncio
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import psycopg2
from psycopg2.extras import RealDictCursor

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'tododb'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

# Create MCP server instance
app = Server("postgres-mcp")

def execute_query(sql: str):
    """Execute a read-only SQL query"""
    # Security: only allow SELECT statements
    sql_upper = sql.strip().upper()
    if not sql_upper.startswith('SELECT'):
        return {"error": "Only SELECT queries are allowed"}

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute(sql)
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return {
            "success": True,
            "rows": len(results),
            "data": [dict(row) for row in results]
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
            name="query_database",
            description="Execute a read-only SQL query against PostgreSQL. Only SELECT statements are allowed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "SQL SELECT query to execute"
                    }
                },
                "required": ["sql"]
            }
        ),
        Tool(
            name="list_tables",
            description="List all tables in the database",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="describe_table",
            description="Show the schema of a specific table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table to describe"
                    }
                },
                "required": ["table_name"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""

    if name == "query_database":
        sql = arguments.get("sql", "")
        result = execute_query(sql)
        return [TextContent(
            type="text",
            text=f"Query Results:\n{result}"
        )]

    elif name == "list_tables":
        sql = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """
        result = execute_query(sql)
        tables = [row['table_name'] for row in result.get('data', [])]
        return [TextContent(
            type="text",
            text=f"Tables in database:\n" + "\n".join(f"  - {t}" for t in tables)
        )]

    elif name == "describe_table":
        table_name = arguments.get("table_name", "")
        sql = f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """
        result = execute_query(sql)
        if result.get('success'):
            schema = "\n".join(
                f"  {row['column_name']}: {row['data_type']} ({'NULL' if row['is_nullable'] == 'YES' else 'NOT NULL'})"
                for row in result.get('data', [])
            )
            return [TextContent(
                type="text",
                text=f"Schema for table '{table_name}':\n{schema}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Error: {result.get('error')}"
            )]

    return [TextContent(
        type="text",
        text=f"Unknown tool: {name}"
    )]

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
