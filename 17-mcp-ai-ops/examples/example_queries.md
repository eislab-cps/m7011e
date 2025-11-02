# Example Queries for MCP Servers

Once you have configured your MCP servers in Claude Code, you can ask natural language questions and Claude will automatically use the appropriate tools.

## PostgreSQL MCP Examples

### Basic Queries

**"What tables are in my database?"**
- Uses: `list_tables` tool
- Returns: List of all tables in the public schema

**"Show me the schema of the todos table"**
- Uses: `describe_table` tool with `table_name="todos"`
- Returns: Column names, data types, and nullability

**"How many todos are in the database?"**
- Uses: `query_database` tool with `sql="SELECT COUNT(*) FROM todos"`
- Returns: Total count

### Data Analysis

**"Show me all incomplete todos"**
- Uses: `query_database` with `sql="SELECT * FROM todos WHERE completed = false"`
- Returns: All uncompleted todos

**"Which user has the most todos?"**
- Uses: `query_database` with SQL joining todos and users
- Returns: User with highest todo count

**"What percentage of todos are completed?"**
- Uses: `query_database` with SQL calculating completion rate
- Returns: Percentage calculation

### Advanced Queries

**"Find all todos created in the last 7 days"**
- Uses: `query_database` with date filtering
- Returns: Recent todos

**"Show me users who have no todos"**
- Uses: `query_database` with LEFT JOIN
- Returns: Users without any todos

**"What's the average number of todos per user?"**
- Uses: `query_database` with aggregation
- Returns: Average calculation

## Prometheus MCP Examples

### Service Health

**"Is the user-service healthy?"**
- Uses: `check_service_health` with `service="user-service"`
- Returns: ✅ UP or ❌ DOWN

**"What services are currently running?"**
- Uses: `query_metrics` with `query="up"`
- Returns: All services with their up/down status

**"Are there any services down?"**
- Uses: `query_metrics` with `query="up == 0"`
- Returns: List of down services

### Performance Metrics

**"What's the request rate for the API?"**
- Uses: `query_metrics` with `query="rate(http_requests_total[5m])"`
- Returns: Requests per second

**"What's the error rate for the user-service?"**
- Uses: `get_error_rate` with `service="user-service"`
- Returns: Errors per second

**"Show me CPU usage for all pods"**
- Uses: `query_metrics` with `query="container_cpu_usage_seconds_total"`
- Returns: CPU metrics

### Historical Analysis

**"How has traffic changed over the last hour?"**
- Uses: `query_metrics_range` with `query="rate(http_requests_total[5m])"` and `duration="1h"`
- Returns: Time series data showing traffic trends

**"What was the p95 latency over the last 24 hours?"**
- Uses: `query_metrics_range` with histogram_quantile query and `duration="24h"`
- Returns: 95th percentile latency over time

### Troubleshooting

**"Why is the recommendation-service slow?"**
- Claude will:
  1. Check service health
  2. Query latency metrics
  3. Check error rate
  4. Look for resource constraints
- Returns: Diagnostic summary

## Kubernetes MCP Examples

### Pod Management

**"What pods are running?"**
- Uses: `get_pods` with `namespace="default"`
- Returns: List of all pods with status

**"Are there any failing pods?"**
- Uses: `get_pods` and filters for non-Running status
- Returns: Failed/pending pods

**"Show me pods in the monitoring namespace"**
- Uses: `get_pods` with `namespace="monitoring"`
- Returns: Monitoring pods

### Logs

**"Show me the last 100 lines of logs from the postgres pod"**
- Uses: `get_pod_logs` with `pod_name="postgres-xxx"` and `tail=100`
- Returns: Recent log entries

**"What errors are in the user-service logs?"**
- Uses: `get_pod_logs` then filters for ERROR level
- Returns: Error log entries

### Service Discovery

**"What services are available?"**
- Uses: `get_services` with `namespace="default"`
- Returns: All services with ClusterIP and ports

**"What deployments do we have?"**
- Uses: `get_deployments` with `namespace="default"`
- Returns: All deployments with replica counts

### Debugging

**"Why is the postgres pod crashing?"**
- Claude will:
  1. Get pod status
  2. Describe the pod (check events)
  3. Get recent logs
- Returns: Diagnosis of the issue

**"Is the user-service deployment healthy?"**
- Uses: `describe_pod` to check deployment status
- Returns: Pod health details

## Multi-Service Queries

These queries combine multiple MCP servers to answer complex questions:

### Cross-System Debugging

**"Why is the user-service slow?"**
1. Kubernetes MCP: Check pod status and resource usage
2. Prometheus MCP: Check latency and error metrics
3. PostgreSQL MCP: Check database connection pool
- Returns: Comprehensive diagnosis

**"Are we having a database performance issue?"**
1. Prometheus MCP: Check database metrics (connection pool, query time)
2. PostgreSQL MCP: Query slow queries or locks
3. Kubernetes MCP: Check database pod resource usage
- Returns: Database health report

### Capacity Planning

**"How much has traffic grown this week?"**
1. Prometheus MCP: Query traffic metrics over 7 days
2. PostgreSQL MCP: Query user growth
- Returns: Traffic and user growth analysis

**"Do we need to scale up?"**
1. Prometheus MCP: Check CPU, memory, and request latency
2. Kubernetes MCP: Check current replica counts
3. PostgreSQL MCP: Check database size and query performance
- Returns: Scaling recommendation

### Data Consistency

**"Are there any orphaned records in the database?"**
1. PostgreSQL MCP: Query for foreign key violations
2. Kubernetes MCP: Check if related services are running
- Returns: Data consistency report

### Security Audit

**"Show me all failed authentication attempts in the last hour"**
1. Kubernetes MCP: Get logs from auth service
2. PostgreSQL MCP: Query auth_logs table
3. Prometheus MCP: Check auth_failures metric
- Returns: Security event summary

## Tips for Effective Prompts

### Be Specific
- ❌ "Check the database"
- ✅ "How many users are in the database?"

### Provide Context
- ❌ "Is it slow?"
- ✅ "Is the user-service API slow compared to yesterday?"

### Ask Follow-up Questions
- Start broad: "What's the status of all services?"
- Then drill down: "Show me logs for the failing service"

### Combine Multiple Sources
- "Check if high error rate in Prometheus correlates with database issues"
- Claude will query both systems and analyze

### Use Time Ranges
- "Show me metrics from the last 5 minutes"
- "What happened between 2pm and 3pm?"

### Request Summaries
- "Give me a health summary of the entire platform"
- "What issues need attention right now?"

## Advanced Use Cases

### Automated Troubleshooting

**"The API is returning 500 errors. What's wrong?"**

Claude will systematically:
1. Query Prometheus for error rate and affected endpoints
2. Check Kubernetes for pod health and recent restarts
3. Get logs from affected pods
4. Query database for connection issues
5. Provide diagnosis and recommendations

### Performance Analysis

**"Generate a performance report for the last 24 hours"**

Claude will:
1. Query Prometheus for key metrics (latency, throughput, errors)
2. Query database for query performance
3. Check Kubernetes for resource usage
4. Compile into readable report

### Compliance Checks

**"List all users who accessed the system yesterday"**

Claude will:
1. Query PostgreSQL for user activity
2. Check Kubernetes logs for access patterns
3. Summarize findings

## Common Patterns

### Health Checks
```
"Is everything healthy?"
"Are there any alerts firing?"
"What services are down?"
```

### Performance
```
"What's the slowest endpoint?"
"Is latency within SLA?"
"Are we hitting rate limits?"
```

### Capacity
```
"How much database space is left?"
"Are we close to pod limits?"
"Do we need to scale?"
```

### Debugging
```
"Why did the service crash?"
"What changed in the last hour?"
"Are there any error spikes?"
```

## Next Steps

Once comfortable with basic queries:

1. **Create custom MCP servers** for your specific services
2. **Add authentication** for production use
3. **Implement caching** for frequently accessed data
4. **Build composite tools** that combine multiple operations
5. **Set up monitoring** of MCP server usage
