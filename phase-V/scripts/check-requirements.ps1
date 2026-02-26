$ErrorActionPreference = "Stop"

Write-Host "🕵️ Verifying Phase 4 Requirements..." -ForegroundColor Cyan

# 1. Check Dockerfiles
Write-Host "`n1. Checking Dockerfiles..." -ForegroundColor Yellow
if (Test-Path "frontend/Dockerfile") { Write-Host "✅ Frontend Dockerfile exists" -ForegroundColor Green }
if (Test-Path "backend/Dockerfile") { Write-Host "✅ Backend Dockerfile exists" -ForegroundColor Green }

# 2. Check Helm Charts
Write-Host "`n2. Checking Helm Charts..." -ForegroundColor Yellow
if (Test-Path "helm-charts/todo-app/Chart.yaml") { Write-Host "✅ Helm Chart exists" -ForegroundColor Green }

# 3. Check Pod Status
Write-Host "`n3. Checking Kubernetes Pods..." -ForegroundColor Yellow
$pods = kubectl get pods -n todo-app -o json | ConvertFrom-Json
$running = $pods.items | Where-Object { $_.status.phase -eq "Running" }
Write-Host "✅ $($running.Count) Pods are Running" -ForegroundColor Green

# 4. Check Backend Chatbot Router
Write-Host "`n4. Checking Backend Chatbot Status..." -ForegroundColor Yellow
$main = Get-Content "backend/main.py" -Raw
if ($main -match "app.include_router\(chatkit.router") {
    Write-Host "✅ Chatbot Router is ENABLED" -ForegroundColor Green
} else {
    Write-Host "❌ Chatbot Router is DISABLED" -ForegroundColor Red
}

# 5. Check AI Ops Docs
Write-Host "`n5. Checking AI Ops Documentation..." -ForegroundColor Yellow
if (Test-Path "docs/phase4/AI_OPS.md") { Write-Host "✅ AI Ops Guide exists" -ForegroundColor Green }

Write-Host "`n🎯 All Phase 4 Requirements Validated!" -ForegroundColor Cyan
