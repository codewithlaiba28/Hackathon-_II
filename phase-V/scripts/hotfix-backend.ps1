$ErrorActionPreference = "Stop"

Write-Host "Applying Backend Hotfix..." -ForegroundColor Cyan

# 1. Point Docker to Minikube
Write-Host "Setting Docker environment to Minikube..."
minikube docker-env --shell powershell | Invoke-Expression

# 2. Build Backend
Write-Host "Building todo-backend:v1..."
docker build -t todo-backend:v1 ./backend

# 3. Restart Deployment
Write-Host "Restarting todo-app-backend..."
kubectl rollout restart deployment todo-app-backend -n todo-app

# 4. Wait for Rollout
kubectl rollout status deployment todo-app-backend -n todo-app

Write-Host "Hotfix Applied!" -ForegroundColor Green
