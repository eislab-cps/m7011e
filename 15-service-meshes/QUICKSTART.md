# Istio Service Mesh - Quick Start Guide

Get started with Istio in 5 steps.

**⚡ Super Quick Start:** Want to see it working in under 2 minutes? Check out [examples/README.md](./examples/README.md) - just copy-paste 4 commands!

## Step 1: Install Istio

```bash
./install-istio.sh
```

This installs:
- Istio control plane (istiod)
- Ingress/Egress gateways
- Kiali (service mesh dashboard)
- Jaeger (distributed tracing)
- Prometheus & Grafana

## Step 2: Deploy Sample Application

```bash
# Deploy backend v1
kubectl apply -f backend-deployment.yaml

# Deploy frontend
kubectl apply -f frontend-deployment.yaml

# Verify sidecars were injected (2/2 containers per pod)
kubectl get pods
```

Expected output:
```
NAME                         READY   STATUS    RESTARTS   AGE
backend-v1-xxx               2/2     Running   0          1m
frontend-xxx                 2/2     Running   0          1m
```

## Step 3: Test Basic Connectivity

```bash
# Get frontend pod name
FRONTEND_POD=$(kubectl get pod -l app=frontend -o jsonpath='{.items[0].metadata.name}')

# Test backend from frontend
kubectl exec $FRONTEND_POD -- curl http://backend:5678
```

Expected: `Backend v1 response`

## Step 4: Apply Traffic Management

### Enable Retries and Timeouts

```bash
kubectl apply -f traffic-management/02-retries-timeouts.yaml
```

### Deploy Canary (v2)

```bash
# Deploy v2
kubectl apply -f backend-v2-deployment.yaml

# Configure 90% v1, 10% v2
kubectl apply -f traffic-management/04-canary-deployment.yaml

# Test traffic split
./test-traffic.sh 100
```

## Step 5: View Observability

### Kiali (Service Graph)

```bash
kubectl port-forward -n istio-system svc/kiali 20001:20001
```

Open: http://localhost:20001

### Jaeger (Distributed Tracing)

```bash
kubectl port-forward -n istio-system svc/tracing 16686:80
```

Open: http://localhost:16686

### Grafana (Metrics)

```bash
kubectl port-forward -n istio-system svc/grafana 3000:3000
```

Open: http://localhost:3000

---

## Common Operations

### Check mTLS Status

```bash
istioctl authn tls-check $FRONTEND_POD backend.default.svc.cluster.local
```

### View Istio Configuration

```bash
istioctl proxy-config routes $FRONTEND_POD
istioctl proxy-config clusters $FRONTEND_POD
```

### Enable Strict mTLS

```bash
kubectl apply -f security/mtls-strict.yaml
```

### Inject Faults for Testing

```bash
# 50% of requests get 5s delay
kubectl apply -f fault-injection/delay-injection.yaml

# 10% of requests get HTTP 500
kubectl apply -f fault-injection/error-injection.yaml
```

### Clean Up

```bash
# Remove all Istio resources
istioctl uninstall --purge -y

# Remove namespace label
kubectl label namespace default istio-injection-
```

---

## Troubleshooting

### Sidecar not injected

```bash
# Check namespace label
kubectl get namespace -L istio-injection

# If missing or you want to ensure it's set, add it:
kubectl label namespace default istio-injection=enabled --overwrite
```

**Note:** If you see "namespace/default not labeled", it means the label is already set!

### Traffic not routing correctly

```bash
# Check VirtualService
kubectl get virtualservice

# Describe VirtualService
kubectl describe virtualservice backend

# Check Envoy configuration
istioctl proxy-config routes $FRONTEND_POD
```

### High latency

```bash
# Check if it's sidecar overhead
kubectl logs $FRONTEND_POD -c istio-proxy

# View metrics
kubectl port-forward -n istio-system svc/grafana 3000:3000
# Then open Istio dashboards
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Control Plane                         │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  Pilot   │  │ Citadel  │  │  Galley  │             │
│  │ (Routes) │  │  (Certs) │  │ (Config) │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│         ▲             ▲             ▲                   │
└─────────┼─────────────┼─────────────┼───────────────────┘
          │             │             │
          └─────────────┴─────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌──────────────┐              ┌──────────────┐
│   Pod A      │              │   Pod B      │
│ ┌──────────┐ │   mTLS       │ ┌──────────┐ │
│ │   App    │ │  ◄─────►     │ │   App    │ │
│ └──────────┘ │              │ └──────────┘ │
│ ┌──────────┐ │              │ ┌──────────┐ │
│ │  Envoy   │ │──────────────│►│  Envoy   │ │
│ │  Proxy   │ │              │ │  Proxy   │ │
│ └──────────┘ │              │ └──────────┘ │
└──────────────┘              └──────────────┘
```

---

## Next Steps

1. Read the full [README.md](./README.md) for detailed explanations
2. Experiment with different traffic splits
3. Try fault injection scenarios
4. Explore Kiali service graph
5. Analyze traces in Jaeger
6. Set up authorization policies
7. Integrate with existing monitoring from Tutorial 13
