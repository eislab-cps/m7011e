# Monitoring Stack Deployment Guide

Quick guide to deploy Prometheus and Grafana monitoring for your microservices.

## Understand the Commands and Their Evidence

`./install.sh` deploys the chart and sample services into `monitoring`; it does not generate application load. `kubectl get pods` inspects workload state, while `kubectl describe` provides details and events when a workload is not ready.

The two port forwards have different destinations: `3000:3000` opens Grafana and `9090:9090` opens Prometheus. They remain running in their terminals. Use Prometheus target status to establish whether data is being collected before interpreting a Grafana graph. `helm upgrade` changes cluster configuration; inspect the resulting resources and measurements after each change.

**Observe:** Send a known number of requests to the sample API and compare the raw `/metrics` values with a Prometheus query after the next scrape. A reachable dashboard, a reachable exporter, and a successful scrape are separate checks. See [the main command explanations](./README.md#read-the-monitoring-commands-as-an-experiment) and [command guide](../../COMMANDS.md).

## Prerequisites

- Kubernetes cluster running
- kubectl configured
- Helm installed
- Python 3.10+ (for running examples locally)

**Note:** This tutorial is self-contained. RabbitMQ is included and will be deployed automatically.

Before installation, build and push the example images as described in [examples/README.md](./examples/README.md) and update `values.yaml` to run this checkout's code. The default `johan/*` image tags may contain older examples.

## Step 1: Deploy Monitoring Stack

```bash
# Navigate to this directory
cd advanced/15-monitoring

# Deploy using install script
./install.sh

# Or manually:
kubectl create namespace monitoring
helm install monitoring -n monitoring .
```

## Step 2: Verify Deployment

```bash
# Check pods
kubectl get pods -n monitoring

# Expected output:
# NAME                           READY   STATUS    RESTARTS   AGE
# prometheus-xxxxx               1/1     Running   0          30s
# grafana-xxxxx                  1/1     Running   0          30s
# rabbitmq-xxxxx                 1/1     Running   0          30s

# Check services
kubectl get svc -n monitoring

# Expected output:
# NAME                 TYPE       PORT(S)
# prometheus           NodePort   9090:30090/TCP
# grafana              NodePort   3000:30300/TCP
# rabbitmq             ClusterIP  5672/TCP,15672/TCP,15692/TCP
```

## Step 3: Access Grafana

### Option A: kubectl port-forward (Recommended for local testing)

```bash
kubectl port-forward -n monitoring svc/grafana 3000:3000
```

Open browser: **http://localhost:3000**
- Username: `admin`
- Password: `admin123`

### Option B: NodePort (External access)

```bash
# Get node IP
kubectl get nodes -o wide

# Access via NodePort
# Grafana: http://<NODE_IP>:30300
```

## Step 4: Access Prometheus

### kubectl port-forward

```bash
kubectl port-forward -n monitoring svc/prometheus 9090:9090
```

Open browser: **http://localhost:9090**

### NodePort

Access via: http://<NODE_IP>:30090

## Step 5: Configure Services for Monitoring

### Add Prometheus Annotations to Your Services

For Prometheus to scrape your service, add these annotations:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: your-service
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8001"      # Port where /metrics is exposed
    prometheus.io/path: "/metrics"
spec:
  selector:
    app: your-service
  ports:
  - port: 8001
```

### Deploy Instrumented Services

See `examples/` directory for sample services with metrics:
- `order-service.py` - Flask API with Prometheus metrics
- `rabbitmq-consumer-monitored.py` - RabbitMQ consumer with metrics

## Step 6: View Dashboards

1. Open Grafana: http://localhost:3000
2. Login with admin/admin123
3. Go to **Dashboards** → **Browse**
4. You should see:
   - **Microservices Health Dashboard**
   - **RabbitMQ Monitoring Dashboard**

## Configuration

### Change Grafana Password

Edit `values.yaml`:
```yaml
grafana:
  adminUser: admin
  adminPassword: your-secure-password
```

Then upgrade:
```bash
helm upgrade monitoring -n monitoring .
```

### Adjust Prometheus Retention

Edit `values.yaml`:
```yaml
prometheus:
  retention: 30d  # Keep 30 days of data
```

Then upgrade:
```bash
helm upgrade monitoring -n monitoring .
```

### Change Scrape Interval

Edit `values.yaml`:
```yaml
prometheus:
  scrapeInterval: 60s  # Scrape every 60 seconds
```

Then upgrade:
```bash
helm upgrade monitoring -n monitoring .
```

## Testing the Setup

### Deploy Example Services

The example services are deployed automatically when using `install.sh`:

```bash
./install.sh --set images.orderService.repository=your-dockerhub-username/order-service \
  --set images.rabbitmqConsumer.repository=your-dockerhub-username/rabbitmq-consumer
```

This deploys:
- Order Service (Flask API with metrics)
- RabbitMQ Consumer (consumer with metrics)

### Verify Deployment

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

### Verify Metrics in Prometheus

1. Port-forward Prometheus:
   ```bash
   kubectl port-forward -n monitoring svc/prometheus 9090:9090
   ```

2. Open Prometheus: http://localhost:9090
3. Go to **Status** → **Targets**
4. You should see `order-service` and `rabbitmq-consumer` targets (may take up to 30 seconds)
5. Try queries:
   ```promql
   http_requests_total
   rabbitmq_messages_processed_total
   rabbitmq_queue_messages
   ```

### View in Grafana

1. Open Grafana: http://localhost:3000
2. Go to **Dashboards**
3. Open **Microservices Health Dashboard**
4. You should see metrics updating in real-time

## Viewing Alerts

### In Prometheus

1. Open http://localhost:9090
2. Go to **Alerts** tab
3. View configured alert rules and their current state

### Notifications

Prometheus evaluates the included rules. To send notifications, deploy or connect Alertmanager and set `prometheus.alertmanagerTarget`. Grafana alert rules and contact points are configured separately; they are not created by this chart.

## Cleanup

```bash
# Uninstall monitoring stack
./uninstall.sh

# Or manually:
helm uninstall monitoring -n monitoring

# Delete namespace (optional)
kubectl delete namespace monitoring
```

## Troubleshooting

### Prometheus Not Scraping Services

**Check service annotations:**
```bash
kubectl get svc your-service -n monitoring -o yaml | grep prometheus
```

**Check Prometheus targets:**
1. Open http://localhost:9090
2. Go to **Status** → **Targets**
3. Find your service - should be **UP**

**Check metrics endpoint:**
```bash
# Test locally
curl http://localhost:8001/metrics

# Test from within cluster
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl http://your-service:8001/metrics
```

### Grafana Shows "No Data"

**Check Prometheus data source:**
1. Grafana → **Configuration** → **Data Sources**
2. Click **Prometheus**
3. URL should be: `http://prometheus:9090`
4. Click **Save & Test** - should be green

**Verify query in Prometheus first:**
1. Open http://localhost:9090
2. Test your query
3. If it works in Prometheus but not Grafana, check time range

### Pod Not Starting

**Check logs:**
```bash
kubectl logs -n monitoring prometheus-xxxxx
kubectl logs -n monitoring grafana-xxxxx
```

**Check events:**
```bash
kubectl get events -n monitoring --sort-by='.lastTimestamp'
```

**Check resource limits:**
```bash
kubectl describe pod -n monitoring prometheus-xxxxx
```

### High Memory Usage

**Check current usage:**
```bash
kubectl top pods -n monitoring
```

**Reduce retention:**
Edit `values.yaml`:
```yaml
prometheus:
  retention: 7d  # Reduce from 15d
```

**Increase resource limits:**
Edit `templates/prometheus-deployment.yaml`:
```yaml
resources:
  limits:
    memory: 2Gi  # Increase if needed
```

## Default Credentials

**Grafana:**
- Username: `admin`
- Password: `admin123` (change in values.yaml)

**Prometheus:**
- No authentication by default
- Add authentication if exposing externally

## Port Reference

| Service | Port | NodePort | Purpose |
|---------|------|----------|---------|
| Grafana | 3000 | 30300 | Web UI |
| Prometheus | 9090 | 30090 | Web UI & API |
| Order Service | 8001 | - | Metrics endpoint |
| Consumer | 8000 | - | Metrics endpoint |
| RabbitMQ Management | 15672 | - | Management UI (port-forward) |
| RabbitMQ Prometheus | 15692 | - | Broker metrics endpoint |

## Next Steps

- Add monitoring to your own services
- Create custom dashboards
- Configure alert notifications
- Set up long-term storage (Thanos, Cortex)
- Implement distributed tracing ([Tutorial 16](../16-service-meshes/README.md))
