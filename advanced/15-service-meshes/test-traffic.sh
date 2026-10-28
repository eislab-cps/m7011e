#!/bin/bash

# Generate test traffic to see Istio features in action
#
# Usage:
#   ./test-traffic.sh [count]
#
# Example:
#   ./test-traffic.sh 100

set -e

COUNT=${1:-50}

# Find frontend pod
FRONTEND_POD=$(kubectl get pod -l app=frontend -o jsonpath='{.items[0].metadata.name}')

if [ -z "$FRONTEND_POD" ]; then
    echo "❌ Error: Frontend pod not found"
    echo "Make sure you've deployed frontend-deployment.yaml"
    exit 1
fi

echo "Generating $COUNT requests to backend service..."
echo ""

for i in $(seq 1 $COUNT); do
    echo -n "Request $i: "
    kubectl exec $FRONTEND_POD -- curl -s http://backend:5678
    sleep 0.1
done

echo ""
echo "✅ Generated $COUNT requests"
echo ""
echo "View traffic in Kiali:"
echo "  kubectl port-forward -n istio-system svc/kiali 20001:20001"
echo "  Open: http://localhost:20001"
echo ""
echo "View traces in Jaeger:"
echo "  kubectl port-forward -n istio-system svc/tracing 16686:80"
echo "  Open: http://localhost:16686"
echo ""
