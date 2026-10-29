# Tutorial 16: Service Meshes with Istio

Learn how to implement advanced traffic management, security, and observability with Istio service mesh.

## Why a Mesh When Applications Can Already Use HTTP and TLS?

Application libraries can implement TLS, retries, routing, and telemetry. In a system with many services and languages, repeating and updating those facilities consistently becomes operational work. A sidecar mesh puts selected transport behavior in managed proxies and distributes policy through a control plane. Istio's [architecture documentation](https://istio.io/latest/docs/ops/deployment/architecture/) describes those responsibilities.

That also adds proxies, configuration, resource use, and failure modes to understand. A smaller system may be better served by its existing libraries and ingress configuration. The mesh does not understand whether Alice owns a todo or whether retrying a payment is safe: application identity, authorization, idempotency, and data correctness remain explicit responsibilities. This tutorial uses sidecars to make the distinction between transport policy and business behavior observable.

## Why This Tutorial Matters

In Tutorial 15, you learned to monitor microservices with Prometheus and Grafana. But as your microservices architecture grows, you face new challenges:

**Responsibilities that need an implementation, with or without a mesh:**
- Connection timeouts, retries, and limits must be chosen for the operation.
- Transport encryption and workload authentication need a suitable TLS configuration.
- Version routing needs a mechanism to select destinations.
- Telemetry needs collection, export, and interpretation.
- Access policies need an identity and an enforcement point.
- Distributed traces need compatible instrumentation and propagated context.

**Facilities a mesh can centralize when configured:**
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

![A sidecar mesh intercepts eligible workload traffic. Read the request path top to bottom; the control plane configures it but does not carry the payload.](./images/mesh-sidecar-data-path.svg)

Repeating transport policy in every application library is operational work. A sidecar mesh moves selected routing, connection security, and telemetry behavior into managed proxies. The application does not normally rewrite its URL to localhost to use the proxy; interception handles eligible traffic. Workload mTLS identifies and protects the proxy-to-proxy connection, not the end user's permission to modify an order.

**Check your reasoning:** Why can two workloads authenticate each other through mTLS while an API still needs Alice's access token and an ownership check?


**Key Concept: Sidecar Pattern**
- New Pods in a namespace labeled for sidecar injection get an Envoy proxy
- Configured eligible workload traffic is intercepted by the sidecar; exclusions and bypasses depend on the installation
- Proxies are configured by the Istio control plane
- Many transport policies can change without editing business handlers; tracing context and application authorization may still need application code

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

## Understand the Control Plane and Traffic Commands

The installer configures cluster infrastructure; the demo runs application traffic through sidecar proxies. Changing a routing policy changes how proxies handle requests, not the application's source code.

| Command below | Meaning and scope |
| --- | --- |
| `./install-istio.sh` | Downloads the pinned CLI if needed, installs Istio's demo control plane, configures the tracing provider, enables default-namespace injection, and installs the matching sample add-ons. These are real cluster changes. |
| `export PATH=...:$PATH` | Makes the downloaded `istioctl` available in this terminal. It does not install another control plane or change every terminal's environment. |
| `kubectl label namespace default istio-injection=enabled --overwrite` | Configures automatic sidecar injection for newly created eligible Pods. Existing Pods are not retroactively given a sidecar. `--overwrite` allows updating an existing label value. |
| `kubectl apply -f examples/simple-demo.yaml` from the tutorial root | Creates the demo workloads and traffic configuration. From inside `examples/`, use the shorter path shown below. Relative paths depend on the current directory. |
| `./test-demo.sh 20` from `examples/` | Waits for demo readiness, then sends 20 requests from the client workload and counts response versions. Twenty is a sample count, not a promised exact 70/30 split. |
| `kubectl exec ... -c client -- curl ...` | Starts curl inside the application container. `-c` matters because the Pod also contains a proxy container. |
| `istioctl proxy-config clusters ...` | Inspects the proxy's received configuration. This provides stronger evidence about transport settings than simply assuming that installed Istio implies encryption. |
| `kubectl apply -f security/mtls-strict.yaml` | Applies a policy requiring mTLS for its targeted traffic. Confirm what workloads and namespaces the policy selects. |
| `istioctl uninstall --purge -y` | Removes mesh installation resources; `-y` skips the confirmation prompt. Follow the cleanup section to remove demo resources and injection settings too. |

**Predict and test:** Why can an old Pod lack a sidecar after its namespace is labeled? Why will 20 weighted requests not necessarily produce exactly 14 v1 and 6 v2 responses? Distinguish the browser-facing TLS from Tutorial 7, workload-to-workload mTLS, and user authorization from Tutorial 12: each authenticates or protects a different boundary. See [the command guide](../../COMMANDS.md).

## Quick Start - Try It Now!

Use this small demo to connect each setup command to an observable routing result. Installation and image downloads may take several minutes:

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

![The control plane distributes policy; proxies carry traffic. Dashed arrows distribute configuration and credentials; solid arrows depict eligible proxy traffic.](./images/istio-control-and-data-planes.svg)

A control plane exists so many proxies can receive a consistent operating policy rather than being configured individually. In this sidecar deployment, istiod combines control-plane functions; names such as Pilot and Citadel describe responsibilities and history, not a requirement to install separate Pods for each label. Application requests flow through the data-plane proxies, while configuration and certificate operations involve the control plane.

**Check your reasoning:** If a routing rule is accepted but a proxy has not received it, which configuration would you inspect before blaming the backend code?


**Components:**

1. **Data Plane (Envoy Proxies)**
   - Lightweight proxies deployed as sidecars
   - Handle eligible intercepted workload traffic
   - Enforce policies and collect telemetry

2. **Control Plane (istiod)**
   - **Configuration distribution**: istiod translates routing policy for proxies (historically associated with Pilot)
   - **Certificate functions**: istiod supports workload certificates for mTLS (historically associated with Citadel)
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

![The demo client and backend each have an application and proxy. Arrows trace a test request through the configured mesh to one backend instance.](./images/mesh-demo-request-path.svg)

The frontend in this exercise is a request-generating workload, not necessarily a human-facing web page. Its requests let you observe the proxy policies without changing backend application code. The mesh can choose versions according to weights or headers, but a short sample is not guaranteed to match the weights exactly. Browser-facing TLS and service-to-service mesh mTLS remain different connections.

**Check your reasoning:** Why should curl run in the named application container rather than assuming the proxy container contains your test tools?


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

![A VirtualService picks the route; a DestinationRule sets the policy. Read left to right as the client's sidecar handles one request to host backend.](./images/virtualservice-and-destinationrule.svg)

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

![The canary rules send beta users to v2 and a tenth of everyone else. Rules are checked top to bottom; the first match wins.](./images/canary-routing-rules.svg)

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

![mTLS proves who is calling; authorization decides if it may. Follow one call from frontend to backend; the checks happen in the backend's sidecar.](./images/mtls-identity-and-authorization.svg)

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
