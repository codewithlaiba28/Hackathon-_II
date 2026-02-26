#!/bin/bash

# Script: build-images.sh
# Description: Build Docker images for frontend and backend

set -e  # Exit on any error

IMAGE_TAG=${1:-"v1"}

echo "Building Docker images with tag: $IMAGE_TAG"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not running"
    exit 1
fi

# Build frontend image
echo "Building frontend image..."
docker build -t todo-frontend:$IMAGE_TAG ./frontend

# Build backend image
echo "Building backend image..."
docker build -t todo-backend:$IMAGE_TAG ./backend

echo "Docker images built successfully:"
echo "  todo-frontend:$IMAGE_TAG"
echo "  todo-backend:$IMAGE_TAG"

# Show image sizes
echo ""
echo "Image sizes:"
docker images | grep "todo-" | grep "$IMAGE_TAG"