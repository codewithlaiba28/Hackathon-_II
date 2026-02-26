# run-perfect-deployment.ps1
# This script automates the entire Phase 5 Part B deployment on Minikube.

$ErrorActionPreference = "Stop"

Write-Host "--- Starting Simplified Deployment ---" -ForegroundColor Cyan

# 1. Start Minikube if not running
Write-Host "`nStep 1: Ensuring Minikube is running (3.5GB RAM, 2 CPUs)..." -ForegroundColor Yellow
try {
    # Fix: minikube status doesn't take --driver flag
    $status = minikube status --output json | ConvertFrom-Json
    if ($status.Host -ne "Running") {
        minikube start --driver=docker --memory 3584 --cpus 2 --wait=all
    } else {
        Write-Host "Minikube is already running." -ForegroundColor Green
    }
} catch {
    Write-Host "Minikube not started yet. Starting now..." -ForegroundColor Gray
    minikube start --driver=docker --memory 3584 --cpus 2 --wait=all
}

# 1b. Cleanup existing namespaces to reclaim memory
Write-Host "`nStep 1b: Cleaning up existing deployments..." -ForegroundColor Yellow
kubectl delete ns todo-app kafka --ignore-not-found --grace-period=0 --force

# 2. Check and Initialize Dapr
Write-Host "`nStep 2: Initializing Dapr on Kubernetes..." -ForegroundColor Yellow
# Use --wait to ensure control plane is ready
dapr init -k --wait

# 3. Setup Kafka (Singleton)
Write-Host "`nStep 3: Deploying Kafka (Small/Stable Singleton)..." -ForegroundColor Yellow
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
# Optimized for Minikube 3.5GB memory - Single Combined Controller/Broker Node
helm upgrade --install kafka bitnami/kafka --version 29.3.14 --namespace kafka `
    --set controller.replicaCount=1 `
    --set image.registry=public.ecr.aws `
    --set image.repository=bitnami/kafka `
    --set image.tag=3.7.1 `
    --set listeners.client.protocol=PLAINTEXT `
    --set listeners.controller.protocol=PLAINTEXT `
    --set listeners.interbroker.protocol=PLAINTEXT `
    --set auth.clientProtocol=plaintext `
    --set auth.interBrokerProtocol=plaintext `
    --set auth.controllerProtocol=plaintext `
    --set controller.persistence.enabled=false `
    --set controller.resources.requests.memory=256Mi `
    --set controller.resources.limits.memory=512Mi `
    --wait --timeout 600s

# 4. Apply Secrets, Redis, and Dapr Components
Write-Host "`nStep 4: Applying Redis, Dapr components, and secrets..." -ForegroundColor Yellow
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f infrastructure/k8s/redis.yaml -n todo-app
Write-Host "  - Waiting for Redis to be ready..."
kubectl wait --for=condition=available deployment/redis -n todo-app --timeout=120s
kubectl apply -f deploy/03-config/neon-db-secret.yaml -n todo-app
kubectl apply -f dapr/components/ -n todo-app

# 5. Build Images in Minikube Docker Env
Write-Host "`nStep 5: Building application images (This may take a few minutes)..." -ForegroundColor Yellow
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

Write-Host "  - Building Backend..."
docker build -t todo-backend:latest ./backend
Write-Host "  - Building Notification Service..."
docker build -t todo-notification-service:latest -f ./backend/Dockerfile.notification_service ./backend
Write-Host "  - Building Recurring Service..."
docker build -t todo-recurring-task-service:latest -f ./backend/Dockerfile.recurring_task_service ./backend
Write-Host "  - Building Frontend..."
docker build -t todo-frontend:latest `
    --build-arg NEXT_PUBLIC_API_URL="" `
    --build-arg BETTER_AUTH_URL=http://localhost:3000 `
    --build-arg BETTER_AUTH_SECRET=1f7f6ff432c42d122e986e869d2067f92957b135 `
    --build-arg DATABASE_URL="postgresql://neondb_owner:npg_y2AxfnYdLmk7@ep-young-union-ahyord23-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require" `
    ./frontend

# 6. Deploy with Helm
Write-Host "`nStep 6: Final Rollout with Helm..." -ForegroundColor Yellow
helm upgrade --install todo-app ./helm-charts/todo-app -n todo-app --values ./helm-charts/todo-app/values-dev.yaml

Write-Host "`n--- DEPLOYMENT COMPLETE ---" -ForegroundColor Green
Write-Host "To view your project, run these commands:" -ForegroundColor Yellow
Write-Host "  kubectl port-forward svc/todo-app-frontend 3000:80 -n todo-app" -ForegroundColor Cyan
Write-Host "  kubectl port-forward svc/todo-app-backend 8000:80 -n todo-app" -ForegroundColor Cyan
Write-Host "`nThen open http://localhost:3000 in your browser" -ForegroundColor Green
