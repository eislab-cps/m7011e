#!/bin/bash

# Build Docker images for the example services
# These will be used by Kubernetes deployments
#
# Note: Builds for linux/amd64 to ensure compatibility with most clusters

set -e

echo "Building example service images for linux/amd64..."

# Build order-service image
echo "  → Building order-service..."
docker build --platform linux/amd64 -t order-service:latest -f Dockerfile .

# Build rabbitmq-consumer image (same Dockerfile, different CMD)
echo "  → Building rabbitmq-consumer..."
docker build --platform linux/amd64 -t rabbitmq-consumer:latest -f Dockerfile .

echo "✅ Images built successfully!"
