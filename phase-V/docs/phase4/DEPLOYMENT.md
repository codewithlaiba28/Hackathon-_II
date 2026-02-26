# Deployment Guide for Todo Application

## Prerequisites

- Docker Desktop with Kubernetes enabled OR Minikube installed
- Helm 3.12+ installed
- kubectl installed and configured
- kubectl-ai installed (optional, for AI-assisted operations)

## Setup Minikube (if using Minikube instead of Docker Desktop Kubernetes)

```bash
# Start Minikube with Docker driver
minikube start --driver=docker --cpus=4 --memory=8192

# Enable ingress addon
minikube addons enable ingress

# Enable metrics-server addon
minikube addons enable metrics-server

# Verify Minikube is running
minikube status
```

## Build Container Images

```bash
# If using Minikube, configure Docker to use Minikube's registry
eval $(minikube docker-env)

# Build frontend image
cd frontend
docker build -t todo-frontend:v1 .

# Build backend image
cd ../backend
docker build -t todo-backend:v1 .
```

## Prepare Helm Values

Update `helm-charts/todo-app/values-dev.yaml` with your specific configuration:

```yaml
# Database configuration (Neon PostgreSQL)
database:
  url: "your-neon-database-url-here"

# Backend secrets
backend:
  openaiApiKey: "your-openai-api-key-here"
  authSecret: "your-better-auth-secret-here"
```

## Deploy Application with Helm

```bash
# Navigate to deployment scripts
cd scripts

# Run the deployment script
./deploy.sh
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
# Check all pods are running
kubectl get pods -n todo-app

# Check services are accessible
kubectl get svc -n todo-app

# Check ingress is configured
kubectl get ingress -n todo-app

# Check application logs
kubectl logs -n todo-app -l app=todo-frontend
kubectl logs -n todo-app -l app=todo-backend

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
# Run cleanup script
./cleanup.sh
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