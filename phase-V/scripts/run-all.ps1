$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting Phase 4 Setup (Robust Mode)..." -ForegroundColor Cyan

# 1. Start Minikube (Fast Check)
Write-Host "`n1. Checking Minikube..." -ForegroundColor Yellow
$status = minikube status --format "{{.Host}}" 2>$null
if ($status -ne "Running") {
    Write-Host "Minikube is not running. Starting..." -ForegroundColor Cyan
    minikube start --driver=docker --image-repository=auto
} else {
    Write-Host "✅ Minikube is already running." -ForegroundColor Green
}
minikube update-context

# 2. Point Docker to Minikube & Create Namespace
Write-Host "`n2. Setting Docker environment & Namespace..." -ForegroundColor Yellow
$dockerEnv = minikube docker-env --shell powershell | Out-String
if ($dockerEnv) { $dockerEnv | Invoke-Expression }
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

# 3. Build images
Write-Host "`n3. Building images..." -ForegroundColor Yellow
$dbUrl = "postgresql://neondb_owner:npg_y2AxfnYdLmk7@ep-young-union-ahyord23-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"

docker build -t todo-frontend:v1 ./frontend `
    --build-arg DATABASE_URL="$dbUrl" `
    --build-arg NEXT_PUBLIC_API_URL="http://localhost:8000" `
    --build-arg NEXT_PUBLIC_BASE_URL="http://localhost:3000"
docker build -t todo-backend:v1 ./backend

# 4. Deploy via Helm
Write-Host "`n4. Upgrading Helm deployment..." -ForegroundColor Yellow
helm upgrade --install todo-app ./helm-charts/todo-app --namespace todo-app --values ./helm-charts/todo-app/values-dev.yaml

# 5. Wait for Rollout
Write-Host "`n5. Waiting for pods to be ready..." -ForegroundColor Yellow
kubectl rollout status deployment todo-app-frontend -n todo-app --timeout=180s
kubectl rollout status deployment todo-app-backend -n todo-app --timeout=180s

# 6. Start Tunnels
Write-Host "`n6. Starting Port Forwarding Tunnels..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k", "kubectl port-forward -n todo-app service/todo-app-frontend 3000:80"
Start-Process cmd -ArgumentList "/k", "kubectl port-forward -n todo-app service/todo-app-backend 8000:80"

Write-Host "`n✅ Setup Complete!" -ForegroundColor Cyan
Write-Host "Visit: http://localhost:3000" -ForegroundColor Green
pause
