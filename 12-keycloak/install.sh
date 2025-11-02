#!/bin/bash

# Installation script for Keycloak tutorial

echo "Keycloak Installation Script"
echo "============================"
echo ""

# Step 1: Create database namespace
echo "Step 1: Creating database namespace..."
kubectl create namespace keycloak-db 2>/dev/null || echo "Namespace keycloak-db already exists"

# Step 2: Deploy PostgreSQL
echo ""
echo "Step 2: Deploying PostgreSQL database..."
if [ ! -d "../08-postgresql" ]; then
    echo "Error: PostgreSQL Helm chart not found. Please ensure Tutorial 8 exists."
    exit 1
fi

helm install keycloak-db \
    -f keycloak-db-values.yaml \
    -n keycloak-db \
    ../08-postgresql

echo "Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n keycloak-db --timeout=180s

# Step 3: Create Keycloak database
echo ""
echo "Step 3: Creating Keycloak database..."
echo "Starting port-forward in background..."
kubectl port-forward -n keycloak-db svc/postgres-service 5432:5432 &
PORT_FORWARD_PID=$!
sleep 5

PGPASSWORD=$(grep DBPassword keycloak-db-values.yaml | awk '{print $2}' | tr -d '"')
PGPASSWORD=$PGPASSWORD psql -h localhost -p 5432 -U keycloak -d postgres -c "CREATE DATABASE keycloak;" 2>/dev/null || echo "Database might already exist"

# Stop port-forward
kill $PORT_FORWARD_PID 2>/dev/null

# Step 4: Create Keycloak namespace
echo ""
echo "Step 4: Creating Keycloak namespace..."
kubectl create namespace keycloak 2>/dev/null || echo "Namespace keycloak already exists"

# Step 5: Install Keycloak
echo ""
echo "Step 5: Installing Keycloak..."
helm install keycloak \
    -f keycloak-chart/values.yaml \
    -n keycloak \
    ./keycloak-chart

echo ""
echo "============================"
echo "Installation in progress!"
echo "============================"
echo ""
echo "Monitor the deployment with:"
echo "  kubectl get pods -n keycloak-db"
echo "  kubectl get pods -n keycloak"
echo ""
echo "Once running, access Keycloak at the domain configured in keycloak-chart/values.yaml"
echo ""
echo "To get admin password:"
echo "  grep adminPassword keycloak-chart/values.yaml"
echo ""
