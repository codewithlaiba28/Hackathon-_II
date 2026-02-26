$ErrorActionPreference = "Stop"

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Step {
    param([string]$Step, [string]$Message)
    Write-Host ""
    Write-Host "------------------------------" -ForegroundColor DarkGray
    Write-Host "  [$Step] $Message" -ForegroundColor Yellow
    Write-Host "------------------------------" -ForegroundColor DarkGray
}

# ==============================================
# Phase V Part B - Full Dapr Minikube Deploy
# ==============================================

Write-Host ""
Write-Host "Phase V Part B - Dapr Minikube Deployment" -ForegroundColor Magenta
Write-Host ""

# -- Step 1: Check Prerequisites --
Write-Step "1/7" "Checking Prerequisites"

# Check Minikube
Write-Info "Checking Minikube status..."
try {
    $minikubeStatus = minikube status --format='{{.Host}}' 2>$null
} catch {
    $minikubeStatus = ""
}

if ($minikubeStatus -ne "Running") {
    Write-Info "Minikube is not running. Starting with recommended resources..."
    minikube start --driver=docker --cpus=2 --memory=3584 --addons=ingress,dashboard
} else {
    Write-Success "Minikube is running."
}

# Check Dapr CLI
Write-Info "Checking Dapr CLI..."
try {
    $daprVersion = dapr --version 2>$null
    Write-Success "Dapr CLI found."
} catch {
    Write-ErrorMsg "Dapr CLI not found. Install it: https://docs.dapr.io/getting-started/install-dapr-cli/"
    exit 1
}

# -- Step 2: Install Dapr on Kubernetes --
Write-Step "2/7" "Installing Dapr on Kubernetes"

Write-Info "Checking if Dapr is already installed on the cluster..."
$daprNamespace = kubectl get namespaces -o jsonpath='{.items[*].metadata.name}' 2>$null | Select-String "dapr-system"
if ($daprNamespace) {
    $daprK8s = kubectl get pods -n dapr-system 2>$null | Select-String "dapr-operator"
    if ($daprK8s) {
        Write-Success "Dapr is already installed on the cluster."
    } else {
        Write-Info "Dapr namespace exists but operator not found. Initializing..."
        dapr init -k --wait
        Write-Success "Dapr initialized on Kubernetes."
    }
} else {
    Write-Info "Installing Dapr on Kubernetes (this may take a minute)..."
    dapr init -k --wait
    Write-Success "Dapr installed on Kubernetes."
}

# -- Step 3: Build Docker Images --
Write-Step "3/7" "Building Docker Images"

# Configure Docker to use Minikube's daemon
Write-Info "Configuring Docker to use Minikube daemon..."
& minikube docker-env --shell powershell | Invoke-Expression

Write-Info "Building Backend Image..."
docker build -t todo-backend:latest ./backend
Write-Success "Backend image built."

Write-Info "Building Frontend Image..."
docker build -t todo-frontend:latest `
    --build-arg DATABASE_URL="postgresql://neondb_owner:npg_zuUPO0C6YqLn@ep-aged-thunder-ah49616e-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require" `
    --build-arg BETTER_AUTH_SECRET="1f7f6ff432c42d122e986e869d2067f92957b135" `
    --build-arg BETTER_AUTH_URL="http://localhost:3000" `
    --build-arg NEXT_PUBLIC_API_URL="" `
    --build-arg NEXT_PUBLIC_BASE_URL="http://localhost:3000" `
    ./frontend
Write-Success "Frontend image built."

Write-Info "Building Notification Service Image..."
docker build -t todo-notification-service:latest -f ./backend/Dockerfile.notification_service ./backend
Write-Success "Notification service image built."

Write-Info "Building Recurring Task Service Image..."
docker build -t todo-recurring-task-service:latest -f ./backend/Dockerfile.recurring_task_service ./backend
Write-Success "Recurring task service image built."

# -- Step 4: Apply Kubernetes Manifests --
Write-Step "4/7" "Applying Kubernetes Manifests"

Write-Info "Creating namespace..."
kubectl apply -f deploy/01-namespace.yaml

Write-Info "Deploying infrastructure (Redis + Dapr components)..."
kubectl apply -f deploy/02-infrastructure/

Write-Info "Applying configuration (ConfigMap + Secrets)..."
kubectl apply -f deploy/03-config/

Write-Info "Deploying services..."
kubectl apply -f deploy/04-services/

# -- Step 5: Wait for Rollout --
Write-Step "5/7" "Waiting for Service Rollouts"

Write-Info "Waiting for Redis..."
kubectl -n todo-app rollout status deployment/redis --timeout=120s 2>$null

Write-Info "Waiting for Backend..."
kubectl -n todo-app rollout status deployment/backend --timeout=180s

Write-Info "Waiting for Frontend..."
kubectl -n todo-app rollout status deployment/frontend --timeout=180s

Write-Info "Waiting for Notification Service..."
kubectl -n todo-app rollout status deployment/notification-service --timeout=120s

Write-Info "Waiting for Recurring Task Service..."
kubectl -n todo-app rollout status deployment/recurring-task-service --timeout=120s

# -- Step 6: Verify Dapr --
Write-Step "6/7" "Verifying Dapr Integration"

Write-Info "Checking Dapr components..."
kubectl get components -n todo-app

Write-Info "Checking pod status (should show 2/2 for Dapr sidecar)..."
kubectl get pods -n todo-app -o wide

Write-Info "Checking Dapr sidecar injection..."
$pods = kubectl get pods -n todo-app -o jsonpath='{.items[*].spec.containers[*].name}' 2>$null
if ($pods -match "daprd") {
    Write-Success "Dapr sidecars detected in pods."
} else {
    Write-ErrorMsg "Warning: Dapr sidecars may not be injected. Check pod annotations."
}

# -- Step 7: Summary --
Write-Step "7/7" "Deployment Summary"

Write-Host ""
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host ""

$minikubeIp = minikube ip
Write-Success "Minikube IP: $minikubeIp"
Write-Info "Services deployed:"
Write-Host "  - Backend        : http://${minikubeIp}:8000" -ForegroundColor White
Write-Host "  - Frontend       : http://${minikubeIp}:3000" -ForegroundColor White
Write-Host "  - Notification   : Internal (ClusterIP)" -ForegroundColor DarkGray
Write-Host "  - Recurring Task : Internal (ClusterIP)" -ForegroundColor DarkGray
Write-Host ""
Write-Info "Dapr Building Blocks Active:"
Write-Host "  - Pub/Sub (Redis)     : pubsub" -ForegroundColor White
Write-Host "  - State Store (Redis) : statestore" -ForegroundColor White
Write-Host "  - Cron Binding        : cron-binding" -ForegroundColor White
Write-Host "  - Secret Store (K8s)  : kubernetes-secrets" -ForegroundColor White
Write-Host "  - Service Invocation  : Enabled via appconfig" -ForegroundColor White
Write-Host ""
Write-Info "Next steps:"
Write-Host "  1. Run: minikube tunnel (for LoadBalancer access)" -ForegroundColor White
Write-Host "  2. Run: powershell -File ./scripts/verify_cluster.ps1" -ForegroundColor White
Write-Host ""
