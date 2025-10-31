#!/bin/bash

# Uninstallation script for Keycloak tutorial

echo "Keycloak Uninstallation Script"
echo "=============================="
echo ""
echo "This will remove Keycloak and its database."
read -p "Are you sure? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Uninstallation cancelled."
    exit 0
fi

echo ""
echo "Step 1: Uninstalling Keycloak..."
helm uninstall keycloak -n keycloak 2>/dev/null || echo "Keycloak release not found"

echo ""
echo "Step 2: Uninstalling PostgreSQL..."
helm uninstall keycloak-db -n keycloak-db 2>/dev/null || echo "Database release not found"

echo ""
echo "Step 3: Deleting namespaces..."
kubectl delete namespace keycloak 2>/dev/null || echo "Keycloak namespace not found"
kubectl delete namespace keycloak-db 2>/dev/null || echo "Database namespace not found"

echo ""
read -p "Delete persistent data? This will remove all database data (yes/no): " DELETE_DATA

if [ "$DELETE_DATA" = "yes" ]; then
    echo "Deleting persistent volume claims..."
    kubectl delete pvc -n keycloak-db --all 2>/dev/null
    echo "Data deleted."
else
    echo "Persistent data retained."
fi

echo ""
echo "=============================="
echo "Uninstallation complete!"
echo "=============================="
