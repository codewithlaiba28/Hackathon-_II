#!/bin/bash

# Script: deploy.sh
# Description: Deploy the todo application to Minikube using Helm

set -e  # Exit on any error

echo "Starting deployment to Minikube..."

# Check if Helm is available
if ! command -v helm &> /dev/null; then
    echo "Error: Helm is not installed"
    exit 1
fi

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed"
    exit 1
fi

# Create namespace if it doesn't exist
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

# Install or upgrade the Helm release
HELM_VALUES_FILE="${HELM_VALUES_FILE:-./helm-charts/todo-app/values-dev.yaml}"

if [ -f "$HELM_VALUES_FILE" ]; then
    echo "Installing/upgrading Helm release with values file: $HELM_VALUES_FILE"
    helm upgrade --install todo-app ./helm-charts/todo-app \
        --namespace todo-app \
        --values "$HELM_VALUES_FILE" \
        --create-namespace
else
    echo "Values file not found: $HELM_VALUES_FILE"
    echo "Installing/upgrading Helm release with default values"
    helm upgrade --install todo-app ./helm-charts/todo-app \
        --namespace todo-app \
        --create-namespace
fi

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=Ready pods -l app=todo-frontend -n todo-app --timeout=300s
kubectl wait --for=condition=Ready pods -l app=todo-backend -n todo-app --timeout=300s

echo "Deployment completed successfully!"
echo ""
echo "Services:"
echo "  Frontend: kubectl port-forward svc/todo-app-frontend 3000:80 -n todo-app"
echo "  Backend:  kubectl port-forward svc/todo-app-backend 8000:80 -n todo-app"
echo ""
echo "Or access via Ingress if configured: http://todo.local"