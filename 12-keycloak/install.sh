#!/bin/bash

# Installation script for Keycloak tutorial
# Self-contained deployment with PostgreSQL and Keycloak

NAMESPACE="keycloak"

echo "Keycloak Installation Script"
echo "============================"
echo ""

# Step 1: Create namespace
echo "Step 1: Creating namespace..."
kubectl create namespace $NAMESPACE 2>/dev/null || echo "Namespace $NAMESPACE already exists"

# Step 2: Deploy PostgreSQL and Keycloak
echo ""
echo "Step 2: Deploying PostgreSQL and Keycloak..."
helm install keycloak \
    -n $NAMESPACE \
    ./keycloak-chart

echo ""
echo "Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n $NAMESPACE --timeout=180s

# Step 3: Create Keycloak database
echo ""
echo "Step 3: Creating Keycloak database..."
kubectl exec -n $NAMESPACE postgres-statefulset-0 -- \
    psql -U keycloak -d postgres -c "CREATE DATABASE keycloak;" 2>/dev/null || echo "Database already exists (this is fine)"

echo ""
echo "Waiting for Keycloak to be ready..."
kubectl wait --for=condition=ready pod -l app=keycloak -n $NAMESPACE --timeout=300s

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
