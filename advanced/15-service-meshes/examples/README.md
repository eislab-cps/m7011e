# Istio Simple Demo

A minimal example to see Istio service mesh in action in under 5 minutes.

## What This Demo Shows

- **Automatic sidecar injection** - Istio adds Envoy proxy to your pods
- **Traffic splitting** - Route 70% traffic to v1, 30% to v2
- **Observability** - View traffic in Kiali and Jaeger
- **Zero code changes** - Your apps don't know about Istio

## Quick Start

### Step 1: Install Istio

If you haven't installed Istio yet:

```bash
cd ..
./install-istio.sh
```

### Step 2: Enable Sidecar Injection

```bash
kubectl label namespace default istio-injection=enabled --overwrite
```

**Note:** If you see "namespace/default not labeled", it means the label is already set. That's fine!

Verify the label:
```bash
kubectl get namespace -L istio-injection
```

Expected output:
```
NAME              STATUS   AGE   ISTIO-INJECTION
default           Active   10d   enabled
```

If you see `enabled` under `ISTIO-INJECTION`, you're good to go!

### Step 3: Deploy the Demo

```bash
kubectl apply -f simple-demo.yaml
```

**What gets deployed:**
- `hello-v1` - Responds with "Hello from v1! 🟢"
- `hello-v2` - Responds with "Hello from v2! 🔵 NEW VERSION!"
- `client` - Test pod with curl
- VirtualService - Routes 70% to v1, 30% to v2
- DestinationRule - Defines v1 and v2 subsets

### Step 4: Verify Deployment

Check that pods are running with **2/2 containers** (app + istio-proxy):

```bash
kubectl get pods
```

Expected output:
```
NAME                        READY   STATUS    RESTARTS   AGE
client-xxx                  2/2     Running   0          1m
hello-v1-xxx                2/2     Running   0          1m
hello-v2-xxx                2/2     Running   0          1m
```

**2/2 means:** Your app (1) + Istio sidecar proxy (1) = 2 containers

### Step 5: Test Traffic Splitting

Generate 20 requests and see the 70/30 split:

```bash
kubectl exec deploy/client -- sh -c 'for i in $(seq 1 20); do curl -s http://hello:8080; done'
```

**Expected output:**
```
Hello from v1! 🟢
Hello from v1! 🟢
Hello from v2! 🔵 NEW VERSION!
Hello from v1! 🟢
Hello from v1! 🟢
Hello from v1! 🟢
Hello from v2! 🔵 NEW VERSION!
Hello from v1! 🟢
...
```

You should see roughly **14 responses from v1** and **6 responses from v2** (70/30 split).

### Step 6: View in Kiali

Open Kiali to see the traffic flow:

```bash
kubectl port-forward -n istio-system svc/kiali 20001:20001
```

Then open: http://localhost:20001

**In Kiali:**
1. Go to **Graph**
2. Select namespace: **default**
3. Click **Display** → Enable **Traffic Animation**
4. Generate more traffic (Step 5)
5. Watch the traffic flow from client → hello (70/30 split)

### Step 7: View Traces in Jaeger

Open Jaeger to see distributed traces:

```bash
kubectl port-forward -n istio-system svc/tracing 16686:80
```

Then open: http://localhost:16686

**In Jaeger:**
1. Select Service: **client.default**
2. Click **Find Traces**
3. Click on any trace to see:
   - Request flow: client → hello-v1 or hello-v2
   - Timing breakdown
   - Sidecar proxy overhead

## Experiment: Change Traffic Split

### Make it 50/50

```bash
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: hello
spec:
  hosts:
  - hello
  http:
  - route:
    - destination:
        host: hello
        subset: v1
      weight: 50
    - destination:
        host: hello
        subset: v2
      weight: 50
EOF
```

Test it:
```bash
kubectl exec deploy/client -- sh -c 'for i in $(seq 1 20); do curl -s http://hello:8080; done'
```

Now you should see ~10 v1 and ~10 v2 responses.

### Send All Traffic to v2 (Blue-Green Deployment)

```bash
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: hello
spec:
  hosts:
  - hello
  http:
  - route:
    - destination:
        host: hello
        subset: v2
      weight: 100
EOF
```

Test it:
```bash
kubectl exec deploy/client -- sh -c 'for i in $(seq 1 10); do curl -s http://hello:8080; done'
```

All responses should be from v2! 🔵

### Header-Based Routing (A/B Testing)

Route beta users to v2, everyone else to v1:

```bash
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: hello
spec:
  hosts:
  - hello
  http:
  - match:
    - headers:
        x-user-type:
          exact: "beta"
    route:
    - destination:
        host: hello
        subset: v2
  - route:
    - destination:
        host: hello
        subset: v1
EOF
```

Test as regular user:
```bash
kubectl exec deploy/client -- curl -s http://hello:8080
```
Output: `Hello from v1! 🟢`

Test as beta user:
```bash
kubectl exec deploy/client -- curl -s -H "x-user-type: beta" http://hello:8080
```
Output: `Hello from v2! 🔵 NEW VERSION!`

## Experiment: Fault Injection

### Inject Delays

Test how your system handles slow responses:

```bash
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: hello
spec:
  hosts:
  - hello
  http:
  - fault:
      delay:
        percentage:
          value: 50.0
        fixedDelay: 3s
    route:
    - destination:
        host: hello
EOF
```

Test it:
```bash
time kubectl exec deploy/client -- curl -s http://hello:8080
```

50% of requests will take 3+ seconds!

### Inject Errors

Test error handling:

```bash
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: hello
spec:
  hosts:
  - hello
  http:
  - fault:
      abort:
        percentage:
          value: 30.0
        httpStatus: 503
    route:
    - destination:
        host: hello
EOF
```

Test it:
```bash
kubectl exec deploy/client -- sh -c 'for i in $(seq 1 20); do curl -s -o /dev/null -w "%{http_code}\n" http://hello:8080; done'
```

You'll see ~30% HTTP 503 errors!

## Verify mTLS is Working

Check that traffic is encrypted with mutual TLS:

```bash
# Get client pod name
CLIENT_POD=$(kubectl get pod -l app=client -o jsonpath='{.items[0].metadata.name}')

# Check mTLS status
istioctl authn tls-check $CLIENT_POD hello.default.svc.cluster.local
```

Expected output:
```
HOST:PORT                              STATUS     SERVER     CLIENT     AUTHN POLICY
hello.default.svc.cluster.local:8080   OK         mTLS       mTLS       default/
```

**What this means:**
- ✅ All traffic is encrypted with mutual TLS
- ✅ Both client and server authenticate each other
- ✅ Zero code changes required!

## Clean Up

Remove the demo:

```bash
kubectl delete -f simple-demo.yaml
```

Remove Istio (if you want):

```bash
istioctl uninstall --purge -y
kubectl label namespace default istio-injection-
```

## What You Just Learned

✅ **Sidecar injection** - Istio automatically adds Envoy proxy to pods
✅ **Traffic splitting** - Route traffic by percentage (canary deployments)
✅ **Header-based routing** - A/B testing for different user groups
✅ **Fault injection** - Test resilience with delays and errors
✅ **Automatic mTLS** - All traffic encrypted without code changes
✅ **Observability** - Visualize traffic with Kiali, trace with Jaeger

## Next Steps

1. Read the full [Tutorial README](../README.md) for detailed explanations
2. Try the advanced examples in `../traffic-management/`
3. Explore security with `../security/mtls-strict.yaml`
4. Set up authorization policies
5. Integrate with your Tutorial 14 monitoring stack
