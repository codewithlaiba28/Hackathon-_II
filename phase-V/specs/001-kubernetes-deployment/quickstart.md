# Quickstart Guide: Phase 4 - Local Kubernetes Deployment

## Prerequisites

- Docker Desktop with Kubernetes enabled OR Minikube installed
- Helm 3.12+ installed
- kubectl installed and configured
- kubectl-ai installed (optional, for AI-assisted operations)
- kagent installed (optional, for Docker AI operations)

## Setup Minikube (if using Minikube instead of Docker Desktop Kubernetes)

```bash
# Start Minikube with Docker driver
minikube start --driver=docker

# Enable ingress addon
minikube addons enable ingress

# Verify Minikube is running
minikube status
```

## Build Container Images

```bash
# If using Minikube, configure Docker to use Minikube's registry
eval $(minikube docker-env)

# Build frontend image
cd frontend
docker build -t todo-frontend:latest .

# Build backend image
cd ../backend
docker build -t todo-backend:latest -f Dockerfile .
docker build -t todo-recurring-task-service:latest -f Dockerfile.recurring_task_service .
docker build -t todo-notification-service:latest -f Dockerfile.notification_service .
```

## Prepare Helm Values

The main Helm chart values are configured in `helm-charts/todo-app/values.yaml`. Review and update this file as needed for your deployment. Key sections include:

- `frontend`: Frontend service image, replicas, resources, and environment variables.
- `backend`: Backend service image, replicas, resources, and environment variables (including API keys and database URL from secrets).
- `recurringTaskService`: Recurring Task Service image, replicas, and resources.
- `notificationService`: Notification Service image, replicas, and resources.
- `ingress`: Ingress rules for external access.
- `database`: External PostgreSQL database connection details.

For local development with Minikube, you might not need to override many values, but ensure image tags (`latest`) and database connection strings are correct.

## Deploy Dapr Components

Before deploying the application, ensure Dapr components are applied to your Kubernetes cluster.

```bash
# Apply Dapr components for pubsub, statestore, and secrets
kubectl apply -f dapr/components/kafka-pubsub.yaml -n todo-app
kubectl apply -f dapr/components/statestore.yaml -n todo-app
kubectl apply -f dapr/components/kubernetes-secrets.yaml -n todo-app

# Verify Dapr components are listed
dapr components -k -n todo-app
```

## Deploy Application with Helm

```bash
# Navigate to helm-charts directory
cd helm-charts

# Install the chart
helm install todo-app ./todo-app \
  --namespace todo-app \
  --create-namespace

# Verify deployment
kubectl get pods -n todo-app
kubectl get services -n todo-app
kubectl get ingress -n todo-app
```

## Access the Application

If using Minikube with ingress:

```bash
# Get Minikube IP
minikube ip

# Add entry to /etc/hosts
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts

# Access the application
open http://todo.local  # Or visit in browser
```

Alternative access methods:

```bash
# Port forward for quick testing
kubectl port-forward -n todo-app svc/todo-app-frontend 3000:80
kubectl port-forward -n todo-app svc/todo-app-backend 8000:80

# Then visit:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## Verify Deployment

```bash
# Check all pods are running and Dapr sidecars are injected
kubectl get pods -n todo-app

# Check services are accessible
kubectl get svc -n todo-app

# Check ingress is configured
kubectl get ingress -n todo-app

# Check application logs
kubectl logs -n todo-app -l app.kubernetes.io/component=frontend
kubectl logs -n todo-app -l app.kubernetes.io/component=backend
kubectl logs -n todo-app -l app=recurring-task-service
kubectl logs -n todo-app -l app=notification-service

# Test application functionality
curl http://todo.local
```

## AI-Assisted Operations

If kubectl-ai is installed:

```bash
# Query cluster state with natural language
kubectl ai "show me the status of todo-app pods"

# Troubleshoot issues
kubectl ai "why are my backend pods failing?"

# Generate commands
kubectl ai "get pods in todo-app namespace sorted by restart count"
```

## Cleanup

```bash
# Uninstall Helm release
helm uninstall todo-app -n todo-app

# Remove namespace (optional)
kubectl delete namespace todo-app

# Reset Docker env if needed
eval $(docker context show)
```

## Troubleshooting

### Common Issues

1. **Images not found**: Make sure you've run `eval $(minikube docker-env)` before building images
2. **Ingress not working**: Verify you've added todo.local to /etc/hosts with the correct Minikube IP
3. **Database connection failures**: Check that Neon database URL is correctly set in secrets
4. **Pods stuck in Pending state**: Check resource requests aren't exceeding Minikube capacity

### Helpful Commands

```bash
# Get detailed pod status
kubectl describe pods -n todo-app

# Tail logs from all pods
kubectl logs -f -n todo-app -l app=todo-frontend
kubectl logs -f -n todo-app -l app=todo-backend

# Scale deployments
kubectl scale -n todo-app deployment/todo-app-frontend --replicas=3
kubectl scale -n todo-app deployment/todo-app-backend --replicas=3
```