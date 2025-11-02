#!/bin/bash

# Install Prometheus, Grafana, RabbitMQ monitoring stack with example services
#
# Prerequisites:
#   - kubectl configured
#   - Helm installed
#
# Usage:
#   ./install.sh
#
# Note: Uses pre-built images from Docker Hub (johan/*)
# To use your own images, see values.yaml for instructions

set -e

namespace="monitoring"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║       Installing Monitoring Stack                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Namespace: ${namespace}"
echo ""

# Install Helm chart
echo "Deploying monitoring stack..."
helm install monitoring -n ${namespace} --create-namespace .

echo ""
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=prometheus -n ${namespace} --timeout=120s
kubectl wait --for=condition=ready pod -l app=grafana -n ${namespace} --timeout=120s
kubectl wait --for=condition=ready pod -l app=rabbitmq -n ${namespace} --timeout=120s
kubectl wait --for=condition=ready pod -l app=order-service -n ${namespace} --timeout=120s
kubectl wait --for=condition=ready pod -l app=rabbitmq-consumer -n ${namespace} --timeout=120s

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║       Monitoring Stack Installed Successfully!            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Components deployed:"
echo "  ✅ Prometheus (metrics storage)"
echo "  ✅ Grafana (dashboards)"
echo "  ✅ RabbitMQ (message queue)"
echo "  ✅ Order Service (example API)"
echo "  ✅ RabbitMQ Consumer (example consumer)"
echo ""
echo "All services are running in Kubernetes!"
echo ""
echo "Access Grafana:"
echo "  kubectl port-forward -n ${namespace} svc/grafana 3000:3000"
echo "  Then open: http://localhost:3000"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Access Prometheus:"
echo "  kubectl port-forward -n ${namespace} svc/prometheus 9090:9090"
echo "  Then open: http://localhost:9090"
echo ""
echo "View Dashboards:"
echo "  1. Open Grafana (http://localhost:3000)"
echo "  2. Go to Dashboards → Browse"
echo "  3. Open 'Microservices Health Dashboard'"
echo "  4. Watch real-time metrics from the example services!"
echo ""
echo "Generate Test Traffic:"
echo "  kubectl run -it --rm test-client --image=curlimages/curl --restart=Never -- \\"
echo "    curl -X POST http://order-service.${namespace}.svc:8001/api/orders \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"customer\": \"Alice\", \"items\": [\"laptop\", \"mouse\"]}'"
echo ""
