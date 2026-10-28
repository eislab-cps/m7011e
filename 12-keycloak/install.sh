#!/bin/bash
set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

# Installation script for Keycloak tutorial
# Self-contained deployment with PostgreSQL and Keycloak

NAMESPACE="keycloak"

echo "Keycloak Installation Script"
echo "============================"
echo ""

# Deploy both components; PostgreSQL initializes the configured database.
helm upgrade --install keycloak --create-namespace -n "$NAMESPACE" ./keycloak-chart

echo ""
echo "Waiting for PostgreSQL to be ready..."
kubectl rollout status statefulset/postgres-statefulset -n "$NAMESPACE" --timeout=180s

echo ""
echo "Waiting for Keycloak to be ready..."
kubectl rollout status deployment/keycloak -n "$NAMESPACE" --timeout=300s

echo ""
echo "============================"
echo "Installation complete!"
echo "============================"
echo ""
echo "Monitor the deployment with:"
echo "  kubectl get pods -n $NAMESPACE"
echo ""
echo "Once running, access Keycloak at the domain configured in keycloak-chart/values.yaml"
echo ""
echo "To get admin password:"
echo "  grep adminPassword keycloak-chart/values.yaml"
echo ""
