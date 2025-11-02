# Quick Start - MCP

Get your first MCP server running with Claude Code in 5 minutes.

## Step 1: Install MCP SDK

```bash
pip install mcp
```

## Step 2: Create PostgreSQL MCP Server

```bash
cd servers/postgres-mcp

# Create requirements.txt
cat > requirements.txt << EOF
mcp>=0.9.0
psycopg2-binary>=2.9.9
EOF

# Install dependencies
pip install -r requirements.txt
```

Copy the `postgres_server.py` from the README Part 1, or use the provided file.

## Step 3: Configure Claude Code

Create or edit `~/.config/claude-code/mcp_settings.json`:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "python3",
      "args": [
        "/Users/YOUR_USERNAME/Development/github/eislab-cps/m7011e/16-mcp/servers/postgres-mcp/postgres_server.py"
      ],
      "env": {
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "tododb",
        "DB_USER": "postgres",
        "DB_PASSWORD": "postgres"
      }
    }
  }
}
```

**Important:**
- Replace `/Users/YOUR_USERNAME/...` with your actual absolute path
- Update database credentials to match your setup from Tutorial 8
- Use `python3` (or `python` depending on your system)

## Step 4: Port-Forward PostgreSQL (if on Kubernetes)

If your PostgreSQL is running on Kubernetes from Tutorial 8:

```bash
kubectl port-forward svc/postgres 5432:5432
```

Leave this running in a separate terminal.

## Step 5: Restart Claude Code

Close and reopen Claude Code to load the MCP configuration.

## Step 6: Test with Claude

Open Claude Code and try these prompts:

**Basic queries:**
- "What tables are in my database?"
- "Show me the schema of the todos table"
- "How many todos are in the database?"

**Data analysis:**
- "Show me all todos"
- "Which users have the most todos?"
- "Are there any incomplete todos?"

**Advanced:**
- "What's the average number of todos per user?"
- "Show me todos created in the last 24 hours"

Claude will automatically use the MCP server to query your database!

## Expected Output

When you ask "What tables are in my database?", you should see:

```
Tables in database:
  - todos
  - users
  - [other tables...]
```

## Troubleshooting

### "MCP server not found"

- Check that the path in `mcp_settings.json` is absolute (starts with `/`)
- Verify the file exists: `ls -la /path/to/postgres_server.py`
- Try running the server manually: `python3 /path/to/postgres_server.py`

### "Database connection failed"

```bash
# Test database connection
psql -h localhost -U postgres -d tododb

# If that fails, check PostgreSQL is running
kubectl get pods -l app=postgres

# Port-forward if needed
kubectl port-forward svc/postgres 5432:5432
```

### "Only SELECT queries are allowed"

This is expected! The MCP server only allows read-only queries for security.

### Claude doesn't use the MCP tools

- Make sure you restarted Claude Code after editing `mcp_settings.json`
- Try being more explicit: "Use the postgres MCP server to show me all tables"
- Check Claude Code logs for errors

## Next Steps

Once the PostgreSQL MCP server is working:

1. **Add Prometheus MCP** (Part 3 of README)
   - Query metrics with natural language
   - Check service health
   - Analyze performance

2. **Add Kubernetes MCP** (Part 4 of README)
   - List pods and services
   - View logs
   - Check deployment status

3. **Combine them all**
   - Ask complex questions that span multiple systems
   - "Why is the user-service slow?" (checks Prometheus + K8s + Database)

## Example Workflows

### Debugging a slow query

**You:** "Why are my database queries slow?"

**Claude (using MCP):**
1. Lists tables to understand the schema
2. Queries for table sizes
3. Checks for missing indexes
4. Provides recommendations

### Finding data inconsistencies

**You:** "Are there any orphaned todos (todos without a user)?"

**Claude:**
1. Describes the tables
2. Runs a JOIN query to find orphans
3. Shows the results

### Generating reports

**You:** "Create a summary report of todo completion rates"

**Claude:**
1. Counts total todos
2. Counts completed todos
3. Calculates percentage
4. Breaks down by user

## Configuration Tips

### Multiple Databases

You can configure multiple PostgreSQL MCP servers:

```json
{
  "mcpServers": {
    "postgres-prod": {
      "command": "python3",
      "args": ["/path/to/postgres_server.py"],
      "env": {
        "DB_HOST": "prod-db.example.com",
        "DB_NAME": "production"
      }
    },
    "postgres-staging": {
      "command": "python3",
      "args": ["/path/to/postgres_server.py"],
      "env": {
        "DB_HOST": "staging-db.example.com",
        "DB_NAME": "staging"
      }
    }
  }
}
```

### Security

For production:

1. **Use read-only credentials**:
   ```sql
   CREATE USER mcp_readonly WITH PASSWORD 'secure_password';
   GRANT CONNECT ON DATABASE tododb TO mcp_readonly;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO mcp_readonly;
   ```

2. **Update MCP config**:
   ```json
   "env": {
     "DB_USER": "mcp_readonly",
     "DB_PASSWORD": "secure_password"
   }
   ```

3. **Store secrets securely**:
   - Don't commit `mcp_settings.json` with passwords
   - Use environment variables or secret managers

## Performance Tips

### Connection Pooling

For high-volume usage, implement connection pooling:

```python
from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **DB_CONFIG
)

def execute_query(sql: str):
    conn = connection_pool.getconn()
    try:
        # ... execute query
    finally:
        connection_pool.putconn(conn)
```

### Query Timeout

Add timeouts to prevent long-running queries:

```python
cursor.execute("SET statement_timeout = 5000")  # 5 seconds
cursor.execute(sql)
```

### Caching

Cache frequently accessed data:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_table_schema(table_name: str):
    # ... query schema
```

## Getting Help

If you're stuck:

1. Check the full README.md for detailed explanations
2. Review MCP documentation: https://modelcontextprotocol.io/
3. Test the server manually: `python3 postgres_server.py`
4. Check Claude Code logs for error messages

Happy MCP coding! 🚀
