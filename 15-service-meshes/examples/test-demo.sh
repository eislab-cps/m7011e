#!/bin/bash

# Test the simple Istio demo
# Usage: ./test-demo.sh [count]

set -e

COUNT=${1:-20}

echo "╔════════════════════════════════════════════════════════════╗"
echo "║       Testing Istio Traffic Split Demo                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if demo is deployed
if ! kubectl get deployment client &> /dev/null; then
    echo "❌ Error: Demo not deployed"
    echo ""
    echo "Please deploy first:"
    echo "  kubectl label namespace default istio-injection=enabled"
    echo "  kubectl apply -f simple-demo.yaml"
    exit 1
fi

# Wait for pods to be ready
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=client --timeout=60s
kubectl wait --for=condition=ready pod -l app=hello --timeout=60s

echo ""
echo "Generating $COUNT requests to hello service..."
echo ""

# Run test and count responses
RESULT=$(kubectl exec deploy/client -- sh -c "for i in \$(seq 1 $COUNT); do curl -s http://hello:8080; echo; done")

V1_COUNT=$(echo "$RESULT" | grep -c "v1" || true)
V2_COUNT=$(echo "$RESULT" | grep -c "v2" || true)

echo "$RESULT"
echo ""
echo "════════════════════════════════════════════════════════════"
echo "Results:"
echo "  Total requests:    $COUNT"
echo "  v1 responses:      $V1_COUNT ($(( V1_COUNT * 100 / COUNT ))%)"
echo "  v2 responses:      $V2_COUNT ($(( V2_COUNT * 100 / COUNT ))%)"
echo "════════════════════════════════════════════════════════════"
echo ""

# Calculate expected split (70/30)
EXPECTED_V1=$(( COUNT * 70 / 100 ))
EXPECTED_V2=$(( COUNT * 30 / 100 ))

echo "Expected (70/30 split):"
echo "  v1 responses:      ~$EXPECTED_V1 (70%)"
echo "  v2 responses:      ~$EXPECTED_V2 (30%)"
echo ""

# Check if within acceptable range (±15%)
DIFF_V1=$(( V1_COUNT - EXPECTED_V1 ))
DIFF_V1=${DIFF_V1#-}  # Absolute value

if [ $DIFF_V1 -lt $(( COUNT * 15 / 100 )) ]; then
    echo "✅ Traffic split working as expected!"
else
    echo "⚠️  Traffic split differs from expected (this is normal for small sample sizes)"
fi

echo ""
echo "View traffic in Kiali:"
echo "  kubectl port-forward -n istio-system svc/kiali 20001:20001"
echo "  Open: http://localhost:20001"
echo ""
echo "View traces in Jaeger:"
echo "  kubectl port-forward -n istio-system svc/tracing 16686:80"
echo "  Open: http://localhost:16686"
echo ""
