# Monitoring Examples

These examples demonstrate how to instrument Python applications with Prometheus metrics. All services run inside Kubernetes.

## Architecture

The examples include:
- **order-service.py** - Flask API exposing Prometheus metrics
- **rabbitmq-consumer-monitored.py** - RabbitMQ consumer with metrics
- **load-generator.py** - Traffic generator (for local testing only)

## Deployment

All example services are automatically deployed when you run:

```bash
cd ..
./install.sh
```

This will:
1. Deploy Prometheus, Grafana, and RabbitMQ
2. Deploy example services (order-service and rabbitmq-consumer)
3. Uses pre-built images from Docker Hub (`johan/order-service`, `johan/rabbitmq-consumer`)

**To use your own modified images**, see "Rebuild and redeploy" section below.

**All image names are configured in** `values.yaml` for easy customization.

## Verify Deployment

```bash
kubectl get pods -n monitoring
```

Expected output:
```
NAME                                 READY   STATUS    RESTARTS   AGE
grafana-xxx                          1/1     Running   0          1m
order-service-xxx                    1/1     Running   0          1m
prometheus-xxx                       1/1     Running   0          1m
rabbitmq-consumer-xxx                1/1     Running   0          1m
rabbitmq-xxx                         1/1     Running   0          1m
```

## Example 1: Order Service (Flask API with Metrics)

The order-service is a Flask API that demonstrates HTTP request instrumentation.

**Metrics exposed:**
- `http_requests_total` - Total HTTP requests (Counter)
- `http_request_duration_seconds` - Request latency (Histogram)
- `orders_created_total` - Total orders created (Counter)
- `active_orders` - Current active orders (Gauge)

**Test the API from within the cluster:**
```bash
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl http://order-service.monitoring.svc:8001/api/orders
```

**View metrics:**
```bash
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl http://order-service.monitoring.svc:8001/metrics
```

**Or port-forward to access locally:**
```bash
kubectl port-forward -n monitoring svc/order-service 8001:8001
# Then: curl http://localhost:8001/metrics
```

## Example 2: RabbitMQ Consumer with Metrics

The rabbitmq-consumer demonstrates message queue monitoring with Prometheus.

**Metrics exposed:**
- `rabbitmq_messages_received_total` - Messages received (Counter)
- `rabbitmq_messages_processed_total` - Successfully processed (Counter)
- `rabbitmq_messages_failed_total` - Failed processing (Counter)
- `rabbitmq_message_processing_seconds` - Processing time (Histogram)
- `rabbitmq_consumer_queue_depth` - Current queue depth (Gauge)

**View consumer logs:**
```bash
kubectl logs -n monitoring -l app=rabbitmq-consumer -f
```

**View consumer metrics:**
```bash
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl http://rabbitmq-consumer.monitoring.svc:8000/metrics
```

## Generating Test Traffic

The example services generate some internal traffic automatically, but you can generate more to see real-time metrics in action.

### Option 1: Quick Test from Kubernetes (Recommended)

Generate single requests from within the cluster:

```bash
# Create a new order
kubectl run -it --rm test-client --image=curlimages/curl --restart=Never -- \
  curl -X POST http://order-service.monitoring.svc:8001/api/orders \
  -H "Content-Type: application/json" \
  -d '{"customer": "Alice", "items": ["laptop", "mouse"]}'

# Get all orders
kubectl run -it --rm test-client --image=curlimages/curl --restart=Never -- \
  curl http://order-service.monitoring.svc:8001/api/orders
```

### Option 2: Continuous Load from Kubernetes

Run a load generator pod inside the cluster:

```bash
# Start continuous load generator
kubectl run load-generator -n monitoring --image=curlimages/curl -- \
  sh -c "while true; do curl http://order-service.monitoring.svc:8001/api/orders; sleep 2; done"

# Watch the traffic in logs
kubectl logs -n monitoring load-generator -f

# Delete when done
kubectl delete pod -n monitoring load-generator
```

### Option 3: Local Load Generator (Advanced)

For more sophisticated load testing with RabbitMQ integration, run the load-generator script locally.

**Step 1: Port-forward the services**

Open two terminal windows and run:

```bash
# Terminal 1: Port-forward order-service
kubectl port-forward -n monitoring svc/order-service 8001:8001

# Terminal 2: Port-forward RabbitMQ
kubectl port-forward -n monitoring svc/rabbitmq 5672:5672
```

Keep these terminals running. You should see:
```
Forwarding from 127.0.0.1:8001 -> 8001
Forwarding from [::1]:8001 -> 8001
```

**Step 2: Verify connectivity**

In a new terminal, test the connections:

```bash
# Test order-service
curl http://localhost:8001/api/orders

# Test order-service metrics endpoint
curl http://localhost:8001/metrics
```

**Step 3: Install Python dependencies**

```bash
cd examples
pip install -r requirements.txt
```

This installs: `requests`, `pika` (RabbitMQ client), `flask`, `prometheus-client`

**Step 4: Run the load generator**

```bash
export ORDER_SERVICE_URL=http://localhost:8001
export RABBITMQ_HOST=localhost
python load-generator.py
```

**Expected output:**
```
[Load Generator] Starting HTTP traffic generation...
[Load Generator] Starting RabbitMQ traffic generation...
[HTTP] GET /api/orders -> 200
[RabbitMQ] Published message to email_notifications queue
[HTTP] POST /api/orders -> 201
[HTTP] GET /api/orders/1 -> 200
...
```

**What the load generator does:**
- Sends HTTP requests to Order Service:
  - 60% GET /api/orders (list all orders)
  - 30% POST /api/orders (create new order)
  - 10% GET /api/orders/{id} (get specific order)
- Publishes messages to RabbitMQ 'email_notifications' queue
- Adds random delays between requests (0.1-2 seconds)
- Runs continuously until you press Ctrl+C

**Step 5: Stop the load generator**

Press `Ctrl+C` to stop. Then stop the port-forwards in the other terminals.

### Verify Metrics are Updating

After generating traffic, check the metrics:

**In Grafana** (http://localhost:3000):
- Open **Microservices Health Dashboard**
- Watch **Request Rate** increase
- See **Response Time** graphs update
- Monitor **Total Requests** counter

**In Prometheus** (http://localhost:9090):
```promql
rate(http_requests_total[1m])
sum(http_requests_total) by (endpoint)
rate(rabbitmq_messages_processed_total[1m])
```

## View Metrics

**Port-forward Grafana and Prometheus:**
```bash
kubectl port-forward -n monitoring svc/grafana 3000:3000
kubectl port-forward -n monitoring svc/prometheus 9090:9090
```

### Prometheus (http://localhost:9090)

Try these queries:

**Request rate:**
```promql
sum(rate(http_requests_total[1m])) by (service)
```

**Error rate:**
```promql
sum(rate(http_requests_total{status=~"5.."}[1m])) by (service)
/ sum(rate(http_requests_total[1m])) by (service) * 100
```

**Response time (p95):**
```promql
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
)
```

**RabbitMQ queue depth:**
```promql
rabbitmq_consumer_queue_depth
```

**Message processing rate:**
```promql
rate(rabbitmq_messages_processed_total[1m])
```

### Grafana (http://localhost:3000)

1. Login: admin / admin123
2. Go to **Dashboards** → **Browse**
3. Open **Microservices Health Dashboard**
4. Watch metrics update in real-time!

## File Descriptions

| File | Purpose |
|------|---------|
| `order-service.py` | Flask API with Prometheus metrics instrumentation |
| `rabbitmq-consumer-monitored.py` | RabbitMQ consumer exposing message processing metrics |
| `load-generator.py` | Traffic generator for testing monitoring setup |
| `requirements.txt` | Python dependencies (flask, prometheus-client, pika, requests) |

## Metrics Patterns

### Counter Example
```python
from prometheus_client import Counter

requests = Counter(
    'http_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

# Increment counter
requests.labels(method='GET', endpoint='/api/orders', status=200).inc()
```

### Histogram Example
```python
from prometheus_client import Histogram

duration = Histogram(
    'http_request_duration_seconds',
    'Request duration',
    ['method', 'endpoint']
)

# Observe value
import time
start = time.time()
# ... do work ...
duration.labels(method='GET', endpoint='/api/orders').observe(time.time() - start)
```

### Gauge Example
```python
from prometheus_client import Gauge

active = Gauge(
    'active_orders',
    'Current active orders'
)

# Set value
active.set(42)

# Increment/decrement
active.inc()
active.dec()
```

## Troubleshooting

### Pod not starting

**Check pod status:**
```bash
kubectl get pods -n monitoring
```

**View pod logs:**
```bash
kubectl logs -n monitoring -l app=order-service
kubectl logs -n monitoring -l app=rabbitmq-consumer
```

**Describe pod for events:**
```bash
kubectl describe pod -n monitoring -l app=order-service
```

### RabbitMQ Consumer CrashLoopBackOff

The consumer waits for RabbitMQ to be ready. Check:
```bash
kubectl logs -n monitoring -l app=rabbitmq-consumer
```

If RabbitMQ is slow to start, the consumer will retry automatically (up to 30 attempts).

### Metrics not appearing in Prometheus

**Wait 30 seconds** for Prometheus to scrape (default scrape interval)

**Check Prometheus targets:**
```bash
kubectl port-forward -n monitoring svc/prometheus 9090:9090
```
Then open http://localhost:9090 → **Status** → **Targets**

**Test metrics endpoint from cluster:**
```bash
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl http://order-service.monitoring.svc:8001/metrics
```

### Rebuild and redeploy after code changes

If you modify the example services and want to deploy your own version:

```bash
# 1. Build your images
cd examples
./build-images.sh

# 2. Push to your Docker Hub
./push-images.sh your-dockerhub-username

# 3. Update values.yaml
cd ..
# Edit values.yaml and change the image repositories:
#   images:
#     orderService:
#       repository: your-dockerhub-username/order-service
#     rabbitmqConsumer:
#       repository: your-dockerhub-username/rabbitmq-consumer

# 4. Upgrade deployment
helm upgrade monitoring -n monitoring .

# Or manually restart deployments if already using your images
kubectl rollout restart deployment/order-service -n monitoring
kubectl rollout restart deployment/rabbitmq-consumer -n monitoring
```

## Next Steps

- Modify the example services to add your own metrics
- Create custom Grafana dashboards
- Set up alert notifications (Slack, Email, PagerDuty)
- Add more instrumented services to the stack
- Explore PromQL queries in Prometheus
