#!/bin/bash
# Phase 5 Part B Deployment Script

set -e

echo "🚀 Starting Phase 5 Part B Deployment..."

# 1. Infrastructure Setup
echo "🔨 Setting up infrastructure..."
kubectl create namespace kafka || true
kubectl create namespace todo-app || true

# 2. Deploy Kafka (if not already running)
if ! kubectl get pods -n kafka | grep -q "kafka"; then
    echo "📦 Deploying Kafka..."
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm repo update
    helm install kafka bitnami/kafka --version 30.x --namespace kafka \
        --set replicaCount=1 --set zookeeper.replicaCount=1 \
        --set image.registry=public.ecr.aws --set image.repository=bitnami/kafka --set image.tag=3.8.1 \
        --set zookeeper.image.registry=public.ecr.aws --set zookeeper.image.repository=bitnami/zookeeper --set zookeeper.image.tag=3.9.1 \
        --set auth.clientProtocol=plaintext --set auth.interBrokerProtocol=plaintext \
        --set persistence.enabled=false --set zookeeper.persistence.enabled=false \
        --set service.type=ClusterIP
fi

# 3. Apply Dapr Components and Secrets
echo "🧩 Applying Dapr components and secrets..."
kubectl apply -f ./deploy/03-config/neon-db-secret.yaml -n todo-app
kubectl apply -f ./dapr/components -n todo-app

# 4. Build Docker Images
echo "🐳 Building Docker images..."
eval $(minikube -p minikube docker-env --shell bash)

echo "  Building backend..."
docker build -t todo-backend:latest ./backend

echo "  Building notification service..."
docker build -t todo-notification-service:latest -f ./backend/Dockerfile.notification .

echo "  Building recurring service..."
docker build -t todo-recurring-task-service:latest -f ./backend/Dockerfile.recurring .

echo "  Building frontend..."
docker build -t todo-frontend:latest \
    --build-arg DATABASE_URL="postgresql://neondb_owner:npg_zuUPO0C6YqLn@ep-aged-thunder-ah49616e-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require" \
    --build-arg BETTER_AUTH_SECRET="1f7f6ff432c42d122e986e869d2067f92957b135" \
    --build-arg BETTER_AUTH_URL="http://localhost:3000" \
    --build-arg NEXT_PUBLIC_API_URL="" \
    --build-arg NEXT_PUBLIC_BASE_URL="http://localhost:3000" \
    ./frontend

# 5. Deploy App with Helm
echo "⛵ Deploying application with Helm..."
helm upgrade --install todo-app ./helm-charts/todo-app -n todo-app --values ./helm-charts/todo-app/values-dev.yaml

echo "✅ Phase 5 Part B Deployment initiated!"
echo "Check pods status: kubectl get pods -n todo-app"
