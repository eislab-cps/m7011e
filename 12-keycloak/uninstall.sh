#!/bin/bash

# Uninstallation script for Keycloak tutorial
# Simplified single-namespace deployment

NAMESPACE="keycloak"

echo "Keycloak Uninstallation Script"
echo "=============================="
echo ""
echo "This will remove Keycloak and its database from namespace: $NAMESPACE"
read -p "Are you sure? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Uninstallation cancelled."
    exit 0
fi

echo ""
echo "Step 1: Uninstalling Keycloak (includes PostgreSQL)..."
helm uninstall keycloak -n $NAMESPACE 2>/dev/null || echo "Keycloak release not found"

echo ""
read -p "Delete persistent data? This will remove all database data (yes/no): " DELETE_DATA

if [ "$DELETE_DATA" = "yes" ]; then
    echo "Deleting persistent volume claims..."
    kubectl delete pvc postgresql-pvc -n "$NAMESPACE"
    echo "Data deleted."
fi

echo ""
if [ "$DELETE_DATA" = "yes" ]; then
    read -p "Also delete the dedicated namespace? (yes/no): " DELETE_NAMESPACE
    if [ "$DELETE_NAMESPACE" = "yes" ]; then
        kubectl delete namespace "$NAMESPACE"
    fi
else
    echo "Database PVC and namespace retained."
fi

echo ""
echo "=============================="
echo "Uninstallation complete!"
echo "=============================="
