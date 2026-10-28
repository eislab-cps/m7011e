#!/bin/bash

# Push images to Docker Hub
# Usage:
#   ./push-images.sh <dockerhub-username>
# Example:
#   ./push-images.sh johan

set -e

DOCKER_USERNAME="${1}"

if [ -z "$DOCKER_USERNAME" ]; then
    echo "❌ Error: Docker Hub username required"
    echo ""
    echo "Usage:"
    echo "  ./push-images.sh <dockerhub-username>"
    echo ""
    echo "Example:"
    echo "  ./push-images.sh johan"
    exit 1
fi

echo "Pushing images to Docker Hub: $DOCKER_USERNAME"
echo ""
echo "Note: Make sure you're logged in to Docker Hub:"
echo "  docker login"
echo ""

# Tag and push order-service
echo "Pushing order-service..."
docker tag order-service:latest $DOCKER_USERNAME/order-service:latest
docker push $DOCKER_USERNAME/order-service:latest

# Tag and push rabbitmq-consumer
echo "Pushing rabbitmq-consumer..."
docker tag rabbitmq-consumer:latest $DOCKER_USERNAME/rabbitmq-consumer:latest
docker push $DOCKER_USERNAME/rabbitmq-consumer:latest

echo ""
echo "✅ Images pushed successfully!"
echo ""
echo "Images available at:"
echo "  - $DOCKER_USERNAME/order-service:latest"
echo "  - $DOCKER_USERNAME/rabbitmq-consumer:latest"
echo ""
