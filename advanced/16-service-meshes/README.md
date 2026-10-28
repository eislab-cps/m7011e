# Tutorial 16: Service Meshes with Istio

Learn how to implement advanced traffic management, security, and observability with Istio service mesh.

## Why This Tutorial Matters

In Tutorial 15, you learned to monitor microservices with Prometheus and Grafana. But as your microservices architecture grows, you face new challenges:

**Without a service mesh:**
- ❌ Each service implements its own retry logic, timeouts, and circuit breakers
- ❌ Service-to-service communication is unencrypted (security risk)
- ❌ Difficult to implement canary deployments or A/B testing
- ❌ No visibility into service-to-service traffic patterns
- ❌ Hard to enforce access policies between services
- ❌ Distributed tracing requires instrumentation and propagation of trace context

**With a service mesh:**
- ✅ Configure retries, timeouts, and circuit breaking in mesh policies
- ✅ Automatic mTLS between participating mesh workloads; strict policies can require it
- ✅ Easy canary deployments and traffic splitting
- ✅ Proxy metrics and tracing when exporters, providers, and sampling are configured
- ✅ Fine-grained access control policies
- ✅ Advanced load balancing and traffic routing

## What is a Service Mesh?

A **service mesh** is a dedicated infrastructure layer that handles service-to-service communication. It provides:

1. **Traffic Management**: Intelligent routing, load balancing, retries, timeouts
2. **Security**: mTLS encryption, authentication, authorization
3. **Observability**: Distributed tracing, metrics, logging

### How It Works

```mermaid
graph LR
    subgraph "Pod A"
        A[Service A]
        PA[Envoy Proxy<br/>Sidecar]
    end

    subgraph "Pod B"
        B[Service B]
        PB[Envoy Proxy<br/>Sidecar]
    end

    subgraph "Control Plane"
        Istiod[Istiod<br/>Configuration & Certs]
    end

    A -->|localhost| PA
    PA -->|mTLS| PB
    PB -->|localhost| B

    Istiod -.->|Configure| PA
    Istiod -.->|Configure| PB

    style PA fill:#e1f5ff
    style PB fill:#e1f5ff
    style Istiod fill:#ffe1f5
```

**Key Concept: Sidecar Pattern**
- New Pods in a namespace labeled for sidecar injection get an Envoy proxy
- All traffic goes through the sidecar proxy
- Proxies are configured by the Istio control plane
- Your application code doesn't change!

## Learning Objectives

By the end of this tutorial, you will understand:
- Service mesh architecture and the sidecar pattern
- Installing and configuring Istio on Kubernetes
- Automatic mTLS encryption between services
- Traffic management (routing rules, retries, timeouts, circuit breakers)
- Canary deployments and traffic splitting
- Distributed tracing with Jaeger
- Authorization policies and security
- Integrating Istio with existing monitoring (Prometheus/Grafana)

## Prerequisites

- Completed Tutorial 15 (Monitoring with Prometheus and Grafana)
- Kubernetes cluster access
- kubectl configured
- Basic understanding of Kubernetes Services and Deployments

The included installer pins Istio 1.31.3 and matching sample add-ons. Check [Istio/Kubernetes compatibility](https://istio.io/latest/docs/releases/supported-releases/) before changing versions. Run commands from `advanced/16-service-meshes/`. You need permissions to install cluster-wide Istio resources.

## Quick Start - Try It Now!

Want to see Istio in action immediately? Try our 5-minute demo:

```bash
# From advanced/16-service-meshes/
./install-istio.sh
export PATH="$PWD/.istio/istio-1.31.3/bin:$PATH"

# 2. Enable sidecar injection (use --overwrite if already labeled)
kubectl label namespace default istio-injection=enabled --overwrite

# 3. Deploy the demo
cd examples
kubectl apply -f simple-demo.yaml

# 4. Test traffic splitting (70% v1, 30% v2)
./test-demo.sh 20
```

You'll see Istio automatically:
- ✅ Inject Envoy sidecar proxies into your pods
- ✅ Split traffic 70% to v1, 30% to v2
- ✅ Use auto-mTLS between participating workloads
- ✅ Enable distributed tracing

See [examples/README.md](./examples/README.md) for the complete quick start guide with experiments!

---

## Part 1: Understanding Service Mesh Concepts

### The Sidecar Pattern

**Traditional Approach:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
  - name: app
    image: myapp:latest
```

**With Istio (Automatic Sidecar Injection):**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  containers:
  - name: app
    image: myapp:latest
  - name: istio-proxy  # ← Automatically injected!
    image: istio/proxyv2:1.31.3
```

### Istio Architecture

```mermaid
graph TB
    subgraph "Data Plane (Envoy Proxies)"
        P1[Pod 1<br/>App + Proxy]
        P2[Pod 2<br/>App + Proxy]
        P3[Pod 3<br/>App + Proxy]
    end

    subgraph "Control Plane (istiod)"
        Pilot[Pilot<br/>Traffic Management]
        Citadel[Citadel<br/>Certificate Authority]
        Config[Configuration<br/>Validation]
    end

    P1 <-->|mTLS| P2
    P2 <-->|mTLS| P3
    P1 <-->|mTLS| P3

    Pilot -.->|Configure Routes| P1
    Pilot -.->|Configure Routes| P2
    Pilot -.->|Configure Routes| P3

    Citadel -.->|Issue Certs| P1
    Citadel -.->|Issue Certs| P2
    Citadel -.->|Issue Certs| P3

    style P1 fill:#e1f5ff
    style P2 fill:#e1f5ff
    style P3 fill:#e1f5ff
    style Pilot fill:#ffe1f5
    style Citadel fill:#ffe1e1
    style Config fill:#e1ffe1
```

**Components:**

1. **Data Plane (Envoy Proxies)**
   - Lightweight proxies deployed as sidecars
   - Handle all network traffic
   - Enforce policies and collect telemetry

2. **Control Plane (istiod)**
   - **Pilot**: Distributes traffic rules to proxies
   - **Citadel**: Manages certificates for mTLS
   - **Configuration validation**: Handled within istiod; Galley is no longer a separate component

### Traffic Flow Example

```
User Request → Ingress Gateway → Service A Pod
                                  ↓
                         [Service A Container]
                                  ↓
                         [Envoy Sidecar Proxy]
                                  ↓
                         Apply: Retries, Timeouts,
                                Circuit Breaking,
                                Load Balancing
                                  ↓
                         [Envoy Sidecar Proxy] → Service B Container
```

---

## Part 2: Installing Istio

### Step 1: Download Istio

The helper script downloads Istio into `.istio/`, installs it, and configures the add-ons and tracing together:

```bash
./install-istio.sh
export PATH="$PWD/.istio/istio-1.31.3/bin:$PATH"
istioctl version
```

The following manual steps explain the underlying commands. Skip reinstalling if you used the helper. Use the add-ons bundled with the same version.

### Step 2: Install Istio on Kubernetes

**Install with the demo profile** (control plane and gateways; observability add-ons are installed separately):

```bash
istioctl install --set profile=demo -y
```

**Expected output:**
```
✔ Istio core installed
✔ Istiod installed
✔ Ingress gateways installed
✔ Egress gateways installed
✔ Installation complete
```

**Verify installation:**
```bash
kubectl get pods -n istio-system
```

**Expected pods:**
```
NAME                                    READY   STATUS    RESTARTS   AGE
istio-ingressgateway-xxx                1/1     Running   0          2m
istio-egressgateway-xxx                 1/1     Running   0          2m
istiod-xxx                              1/1     Running   0          2m
```

### Step 3: Enable Automatic Sidecar Injection

Label your namespace to automatically inject Envoy sidecars:

```bash
# Enable for default namespace
kubectl label namespace default istio-injection=enabled --overwrite

# Verify the label
kubectl get namespace -L istio-injection
```

Expected output:
```
NAME              STATUS   AGE   ISTIO-INJECTION
default           Active   10d   enabled
```

**Note:** If you see "namespace/default not labeled", the namespace is already labeled (that's fine!). The `--overwrite` flag ensures the label is set regardless.

**How it works:**
- When you deploy a pod in a labeled namespace, Istio automatically adds the Envoy sidecar
- No changes to your deployment YAML required!

---

## Part 3: Deploying Services with Istio

Let's deploy a simple multi-service application to demonstrate Istio features.

### Application Architecture

The `frontend` Pod is a shell-based test client, not a web server. It sends requests to the HTTP echo backend. This demo does not deploy a database or an external Gateway route.

```mermaid
graph LR
    Client["frontend test client + Envoy"] -->|"HTTP over mesh mTLS"| Backend["backend v1/v2 + Envoy"]
```

### Create Sample Application

**backend-deployment.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
  labels:
    app: backend
spec:
  ports:
  - port: 5678
    name: http
  selector:
    app: backend
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-v1
  labels:
    app: backend
    version: v1
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
      version: v1
  template:
    metadata:
      labels:
        app: backend
        version: v1
    spec:
      containers:
      - name: backend
        image: hashicorp/http-echo
        args:
        - "-text=Backend v1 response"
        - "-listen=:5678"
        ports:
        - containerPort: 5678
          name: http
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
          limits:
            cpu: 100m
            memory: 128Mi
```

**frontend-deployment.yaml:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: frontend
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  labels:
    app: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
        version: v1
    spec:
      serviceAccountName: frontend
      containers:
      - name: frontend
        image: nicolaka/netshoot
        command: ["/bin/sh"]
        args:
        - -c
        - |
          echo "Frontend service ready. Use this pod to test backend connectivity."
          echo "Example: curl http://backend:5678"
          sleep infinity
        resources:
          requests:
            cpu: 50m
            memory: 64Mi
          limits:
            cpu: 100m
            memory: 128Mi
```

**Deploy the application:**
```bash
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml

# Verify sidecars were injected
kubectl get pods
```

**You should see 2 containers per pod** (app + istio-proxy):
```
NAME                        READY   STATUS    RESTARTS   AGE
backend-xxx                 2/2     Running   0          1m
frontend-xxx                2/2     Running   0          1m
```

---

## Part 4: Traffic Management

These examples update the same `backend` VirtualService or DestinationRule. Applying a later file replaces the earlier file's fields; merge the policies into one manifest when combining canary routing, retries, and circuit breaking.

### Virtual Services and Destination Rules

**VirtualService** defines routing rules (where traffic goes)
**DestinationRule** defines policies (how traffic is handled)

### Example 1: Simple Routing

**backend-virtualservice.yaml:**
```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
        port:
          number: 5678
```

### Example 2: Retries and Timeouts

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend
spec:
  hosts:
  - backend
  http:
  - route:
    - destination:
        host: backend
    timeout: 5s
    retries:
      attempts: 3
      perTryTimeout: 2s
      retryOn: 5xx,reset,connect-failure
```

**What this does:**
- Total timeout: 5 seconds
- Retry up to 3 times on errors
- Each retry has 2-second timeout
- Retry on: HTTP 5xx, connection reset, connection failure

### Example 3: Circuit Breaking

**backend-destinationrule.yaml:**
```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: backend
spec:
  host: backend
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 10
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 60s
      maxEjectionPercent: 50
```

**What this does:**
- Max 100 TCP connections
- Max 10 pending HTTP requests
- After 5 consecutive 5xx failures, outlier detection can eject a backend; checks run at 30-second intervals and the base ejection duration is 60 seconds
- Never eject more than 50% of backends

---

## Part 5: Canary Deployments

Deploy a new version (v2) and gradually shift traffic.

### Deploy Backend v2

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-v2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
      version: v2
  template:
    metadata:
      labels:
        app: backend
        version: v2
    spec:
      containers:
      - name: backend
        image: hashicorp/http-echo
        args:
        - "-text=Backend v2 NEW FEATURE!"
        ports:
        - containerPort: 5678
```

### Traffic Splitting (90% v1, 10% v2)

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend
spec:
  hosts:
  - backend
  http:
  - match:
    - headers:
        x-beta-user:
          exact: "true"
    route:
    - destination:
        host: backend
        subset: v2
      weight: 100
  - route:
    - destination:
        host: backend
        subset: v1
      weight: 90
    - destination:
        host: backend
        subset: v2
      weight: 10
---
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: backend
spec:
  host: backend
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

**What this does:**
- Beta users (header `x-beta-user: true`) → 100% to v2
- Everyone else → 90% to v1, 10% to v2
- Gradually increase v2 weight as confidence grows

**Test it:**
```bash
# Regular user (90% v1, 10% v2)
kubectl exec frontend-xxx -c frontend -- curl backend:5678

# Beta user (100% v2)
kubectl exec frontend-xxx -c frontend -- curl -H "x-beta-user: true" backend:5678
```

---

## Part 6: Security with mTLS

### Enable Strict mTLS

Force all communication to use mutual TLS:

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: default
spec:
  mtls:
    mode: STRICT
```

**Apply it:**
```bash
kubectl apply -f security/mtls-strict.yaml
```

**Inspect the outbound TLS configuration:**
```bash
FRONTEND_POD=$(kubectl get pod -l app=frontend -o jsonpath='{.items[0].metadata.name}')
istioctl proxy-config clusters "$FRONTEND_POD" --fqdn backend.default.svc.cluster.local -o json
```

Look for `envoy.transport_sockets.tls` in the transport-socket configuration. After generating traffic, query `istio_requests_total{connection_security_policy="mutual_tls"}` in the add-on Prometheus instance to inspect observed mTLS traffic. The old `istioctl authn tls-check` command is no longer available.

### Authorization Policies

**Only allow frontend to call backend:**

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: backend-policy
  namespace: default
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/frontend"]
```

**What this does:**
- Only pods with `frontend` service account can call backend
- All other requests are denied (403 Forbidden)

---

## Part 7: Observability with Kiali and Jaeger

### Install Observability Add-ons

`install-istio.sh` applies the add-ons from `.istio/istio-1.31.3/samples/addons/`, registers Jaeger's OTLP collector as a mesh extension provider, and creates a Telemetry resource with 100% sampling for this demo. Installing the demo profile or Jaeger alone does not enable tracing. For production, choose suitable sampling and storage. See [Istio OpenTelemetry tracing](https://istio.io/latest/docs/tasks/observability/distributed-tracing/opentelemetry/).

For traces to join across several application hops, the application must forward trace-context headers. An injected proxy cannot reconstruct context that the application drops.

### Access Kiali (Service Mesh Dashboard)

```bash
kubectl port-forward -n istio-system svc/kiali 20001:20001
```

Open: http://localhost:20001

**Kiali provides:**
- Service topology graph
- Traffic flow visualization
- Health status
- Configuration validation
- Security policies overview

### Access Jaeger (Distributed Tracing)

```bash
kubectl port-forward -n istio-system svc/tracing 16686:80
```

Open: http://localhost:16686

**Jaeger shows:**
- Request traces across services
- Latency breakdown per service
- Error tracking
- Dependency analysis

### Generate Traffic for Tracing

```bash
# Generate requests
for i in {1..100}; do
  kubectl exec frontend-xxx -c frontend -- curl -s backend:5678
done
```

Then view traces in Jaeger to see:
- Frontend → Backend request flow
- Timing for each hop
- Sidecar proxy overhead

---

## Part 8: Fault Injection for Testing

Test your application's resilience by injecting faults.

### Inject HTTP Delays

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend
spec:
  hosts:
  - backend
  http:
  - fault:
      delay:
        percentage:
          value: 50
        fixedDelay: 5s
    route:
    - destination:
        host: backend
```

**What this does:**
- 50% of requests get a 5-second delay
- Tests timeout handling in frontend

### Inject HTTP Errors

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend
spec:
  hosts:
  - backend
  http:
  - fault:
      abort:
        percentage:
          value: 10
        httpStatus: 500
    route:
    - destination:
        host: backend
```

**What this does:**
- 10% of requests return HTTP 500
- Tests error handling and retry logic

---

## Part 9: Integration with Existing Monitoring

Istio integrates seamlessly with Tutorial 15's Prometheus/Grafana setup.

### Istio Metrics in Prometheus

Istio automatically exports metrics to Prometheus:

```promql
# Request rate by service
rate(istio_requests_total[1m])

# Request duration (p95)
histogram_quantile(0.95,
  sum(rate(istio_request_duration_milliseconds_bucket[1m])) by (le, destination_service)
)

# Error rate
sum(rate(istio_requests_total{response_code=~"5.."}[1m])) by (destination_service)
/ sum(rate(istio_requests_total[1m])) by (destination_service)
```

### Istio Dashboards in Grafana

Import Istio dashboards:

1. Open Grafana: http://localhost:3000
2. Go to **Dashboards** → **Import**
3. Use dashboard ID: **7645** (Istio Service Dashboard)
4. Select Prometheus data source
5. Click **Import**

---

## Part 10: Best Practices

### 1. Start with Permissive Mode

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: PERMISSIVE  # Allow both mTLS and plain text
```

Then migrate to STRICT once all services are working.

### 2. Use Namespace-Scoped Policies

```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: backend
  namespace: production  # Scoped to namespace
spec:
  hosts:
  - backend.production.svc.cluster.local
```

### 3. Set Resource Limits on Sidecars

Put sidecar resource annotations on the Deployment's **Pod template**, then recreate the Pods:

```yaml
spec:
  template:
    metadata:
      annotations:
        sidecar.istio.io/proxyCPU: "100m"
        sidecar.istio.io/proxyCPULimit: "200m"
        sidecar.istio.io/proxyMemory: "128Mi"
        sidecar.istio.io/proxyMemoryLimit: "256Mi"
```

### 4. Monitor Sidecar Overhead

```bash
# Check sidecar resource usage
kubectl top pods

# Compare with and without sidecar
```

**Expected overhead:**
- CPU: 50-100m per sidecar
- Memory: 50-100Mi per sidecar

---

## Summary

### What You Learned

- ✅ **Service mesh fundamentals**: Sidecar pattern, control/data plane architecture
- ✅ **Installing Istio**: istioctl, automatic sidecar injection
- ✅ **Traffic management**: VirtualServices, DestinationRules, retries, timeouts
- ✅ **Advanced deployments**: Canary releases, traffic splitting, A/B testing
- ✅ **Security**: Automatic mTLS, authorization policies
- ✅ **Observability**: Kiali service graph, Jaeger distributed tracing
- ✅ **Fault injection**: Testing resilience with delays and errors
- ✅ **Integration**: Connecting Istio with Prometheus/Grafana

### Key Takeaways

1. **Service mesh moves logic out of application code**
   - Retries, timeouts, circuit breaking → handled by sidecar
   - mTLS encryption → automatic
   - Distributed tracing → configure providers and propagate context in application calls

2. **Progressive rollouts made easy**
   - Limit rollout exposure and monitor the new version
   - Gradually shift traffic based on metrics
   - Rollback instantly if issues occur

3. **Identity-based security**
   - Auto-mTLS between participating mesh workloads
   - Strict mTLS and authorization policies must be configured to require authenticated callers

4. **Complete observability**
   - Kiali for topology and health
   - Jaeger for distributed traces
   - Prometheus/Grafana for metrics

### When to Use a Service Mesh

**Use Istio when:**
- You have many microservices (10+)
- You need advanced traffic management (canary, A/B testing)
- Security is critical (mTLS, zero-trust)
- You want proxy telemetry and can propagate trace context between application hops

**Don't use Istio when:**
- You have < 5 services (overhead not worth it)
- Simple architecture (Kubernetes Services are enough)
- Limited resources (sidecars consume CPU/memory)

---

## Further Reading

- [Istio Documentation](https://istio.io/latest/docs/)
- [Envoy Proxy Documentation](https://www.envoyproxy.io/docs/)
- [Service Mesh Patterns](https://www.oreilly.com/library/view/istio-up-and/9781492043775/)
- [Kiali Documentation](https://kiali.io/docs/)
- [Jaeger Tracing](https://www.jaegertracing.io/docs/)
