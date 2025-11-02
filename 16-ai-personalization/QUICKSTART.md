# Quick Start - AI Personalization

Get a working recommendation service running in 5 minutes.

## Option A: Using Make (Easiest)

If you have `make` installed, use these simple commands:

```bash
# Verify your setup
make verify

# Install dependencies and train model
make install-training
make train

# Test locally
make install-service
make test-local
```

For Kubernetes deployment:
```bash
# Build and push Docker image
export DOCKER_USERNAME=your-username
make build
make push

# Deploy to Kubernetes
make deploy

# Test on Kubernetes
make test-k8s
```

Run `make help` to see all available commands.

## Option B: Manual Steps

Follow these steps if you prefer to run commands manually or don't have `make` installed.

### Step 1: Train the Model Locally

```bash
cd training

# Install dependencies
pip install -r requirements.txt

# Train the model
python train_model.py
```

Expected output:
```
Loading training data...
Creating user-item matrix...
Matrix shape: (8, 5)
Users: 8, Items: 5

Training collaborative filtering model...
✅ Model trained!

Top 5 recommendations for User 1:
  1. Keyboard (ID: 103, Score: 0.892)
  2. Monitor 27" (ID: 104, Score: 0.845)
  3. USB-C Hub (ID: 105, Score: 0.823)
  ...
```

### Step 2: Test Service Locally

```bash
# Copy model files to service directory
cp *.pkl ../service/

cd ../service

# Install service dependencies
pip install -r requirements.txt

# Run the service
python recommendation_service.py
```

Test it in another terminal:
```bash
# Get recommendations
curl http://localhost:8080/api/recommendations/1

# Get popular items
curl http://localhost:8080/api/popular

# Check metrics
curl http://localhost:8080/metrics
```

### Step 3: Build Docker Image

```bash
cd service

# Build image
docker build -t your-username/recommendation-service:v1 .

# Test it
docker run -p 8080:8080 your-username/recommendation-service:v1

# Push to registry
docker push your-username/recommendation-service:v1
```

### Step 4: Deploy to Kubernetes

```bash
cd ..

# Deploy Redis
kubectl apply -f redis-deployment.yaml

# Update image name in recommendation-service.yaml
# Change: image: johan/recommendation-service:latest
# To:     image: your-username/recommendation-service:v1

# Deploy recommendation service
kubectl apply -f recommendation-service.yaml

# Check pods
kubectl get pods
```

### Step 5: Test on Kubernetes

```bash
# Get pod name
POD=$(kubectl get pod -l app=recommendation-service -o jsonpath='{.items[0].metadata.name}')

# Test API
kubectl exec -it $POD -- curl http://localhost:8080/api/recommendations/1

# Check metrics
kubectl exec -it $POD -- curl http://localhost:8080/metrics | grep recommendation
```

### Step 6: View in Grafana

If you have Tutorial 13 monitoring running:

```bash
# Port-forward Grafana
kubectl port-forward -n monitoring svc/grafana 3000:3000
```

Open http://localhost:3000 and add Prometheus queries:
- `rate(recommendation_requests_total[1m])`
- `rate(recommendation_cache_hits_total[1m])`
- `histogram_quantile(0.95, rate(recommendation_latency_seconds_bucket[5m]))`

## Troubleshooting

### Model training fails

```bash
# Check data file exists
ls -la training/sample_data.csv

# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Service won't start

```bash
# Check model files exist
ls -la service/*.pkl

# Run with debug
cd service
python recommendation_service.py
# Look for error messages
```

### Redis connection error

```bash
# Check Redis is running
kubectl get pods -l app=redis

# Check Redis service
kubectl get svc redis

# Test Redis connection
kubectl run -it --rm redis-test --image=redis:7-alpine --restart=Never -- redis-cli -h redis ping
# Should return: PONG
```

### No recommendations returned

```bash
# Check user ID exists in training data
# Valid user IDs from sample data: 1, 2, 3, 4, 5, 6, 7, 8

# Try a different user
curl http://localhost:8080/api/recommendations/2

# Check logs
kubectl logs -l app=recommendation-service
```

## Next Steps

1. Add your own purchase data to `sample_data.csv`
2. Retrain the model with more data
3. Set up A/B testing with Istio (Tutorial 14)
4. Create Grafana dashboard for monitoring
5. Implement automated retraining pipeline
