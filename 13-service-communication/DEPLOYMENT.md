# RabbitMQ Deployment Guide

Quick guide to deploy and access RabbitMQ on Kubernetes using kubectl port-forward.

## Prerequisites

- Kubernetes cluster running and kubectl configured
- Helm installed (optional - the chart uses templates directly)

## Step 1: Configure Credentials (Optional)

Before deploying, you can customize the RabbitMQ credentials by editing `values.yaml`:

```yaml
# RabbitMQ Credentials
RabbitMQUser: "admin"
RabbitMQPassword: "changeme123"  # Change this!
```

Or override during installation:

```bash
helm install rabbitmq -n rabbitmq . \
  --set RabbitMQUser="yourusername" \
  --set RabbitMQPassword="yoursecurepassword"
```

## Step 2: Deploy RabbitMQ

```bash
# Navigate to this directory
cd 12-service-communication

# Create namespace
kubectl create namespace rabbitmq

# Deploy using Helm (with default credentials from values.yaml)
helm install rabbitmq -n rabbitmq .

# Wait for pod to be ready
kubectl wait --for=condition=ready pod -l app=rabbitmq -n rabbitmq --timeout=60s
```

## Step 3: Verify Deployment

```bash
# Check pod status
kubectl get pods -n rabbitmq

# Expected output:
# NAME                                  READY   STATUS    RESTARTS   AGE
# rabbitmq-deployment-xxxxxxxxxx-xxxxx  1/1     Running   0          30s

# Check services
kubectl get svc -n rabbitmq

# Expected output:
# NAME                          TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)
# rabbitmq-service-api          NodePort   10.96.xxx.xxx   <none>        5672:30000/TCP
# rabbitmq-service-management   NodePort   10.96.xxx.xxx   <none>        15672:30001/TCP
```

## Step 4: Access RabbitMQ Locally

### Access Management UI (Web Interface)

```bash
# Forward management UI to localhost
kubectl port-forward -n rabbitmq svc/rabbitmq-service-management 15672:15672
```

Open browser: **http://localhost:15672**
- Username: `admin`
- Password: `changeme123`

### Access AMQP API (For Applications)

```bash
# Forward AMQP API to localhost
kubectl port-forward -n rabbitmq svc/rabbitmq-service-api 5672:5672
```

Now your applications can connect to `localhost:5672`

### Forward Both Ports

```bash
# Terminal 1: AMQP API
kubectl port-forward -n rabbitmq svc/rabbitmq-service-api 5672:5672

# Terminal 2: Management UI
kubectl port-forward -n rabbitmq svc/rabbitmq-service-management 15672:15672
```

## Step 5: Test the Deployment

```bash
# Install Python dependencies
cd examples
pip install -r requirements.txt

# Ensure port-forward is running (see Step 3)

# Terminal 1: Start consumer
python consumer_simple.py

# Terminal 2: Send messages
python producer_simple.py
```

## Quick Reference

### Service Names (Inside Kubernetes Cluster)

Use these hostnames when your applications run **inside** Kubernetes:

- AMQP API: `rabbitmq-service-api:5672`
- Management UI: `rabbitmq-service-management:15672`

Example in Python deployment:
```python
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq-service-api',  # Internal service name
        port=5672,
        credentials=pika.PlainCredentials('admin', 'changeme123')
    )
)
```

### External Access (NodePort)

If you need direct access without port-forward:

```bash
# Get node IP
kubectl get nodes -o wide

# Access via NodePort
# AMQP API: <NODE_IP>:30000
# Management UI: http://<NODE_IP>:30001
```

### Credentials

- **Username:** `admin`
- **Password:** `changeme123`

**⚠️ WARNING:** Change these credentials for production!

Edit `values.yaml`:
```yaml
RabbitMQUser: "admin"
RabbitMQPassword: "your-secure-password"
```

Then upgrade the deployment:
```bash
helm upgrade rabbitmq -n rabbitmq .
```

Or upgrade with command-line override:
```bash
helm upgrade rabbitmq -n rabbitmq . \
  --set RabbitMQPassword="your-secure-password"
```

## Cleanup

```bash
# Uninstall RabbitMQ
helm uninstall rabbitmq -n rabbitmq

# Delete namespace (optional)
kubectl delete namespace rabbitmq
```

## Troubleshooting

### Pod not starting

```bash
# Check pod logs
kubectl logs -n rabbitmq deployment/rabbitmq-deployment

# Describe pod for events
kubectl describe pod -n rabbitmq -l app=rabbitmq
```

### Port-forward connection refused

```bash
# Ensure pod is running
kubectl get pods -n rabbitmq

# Check if service exists
kubectl get svc -n rabbitmq

# Try port-forward with pod name directly
kubectl port-forward -n rabbitmq <pod-name> 5672:5672
```

### Cannot connect from Python script

```bash
# Verify port-forward is running in another terminal
# Check localhost:5672 is listening
lsof -i :5672

# Test with telnet
telnet localhost 5672
# Should connect (Ctrl+C to exit)
```

### Authentication failed

```bash
# Check credentials in configmap
kubectl get configmap rabbitmq-config -n rabbitmq -o yaml

# Restart pod to pick up new credentials
kubectl rollout restart deployment/rabbitmq-deployment -n rabbitmq
```

## Next Steps

- See `README.md` for complete tutorial on RabbitMQ and message acknowledgments
- See `examples/README.md` for runnable Python examples
- Try the crash recovery demo: `examples/consumer_crash_demo.py`
