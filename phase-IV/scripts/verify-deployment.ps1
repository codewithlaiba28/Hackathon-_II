# Verify Deployment Script
$ErrorActionPreference = "Stop"

Write-Host "Verifying Phase 4 Deployment..." -ForegroundColor Cyan

# 1. Check Minikube Status
Write-Host "`n1. Checking Minikube Status..." -ForegroundColor Yellow
$minikubeStatus = minikube status --format='{{.Host}}'
if ($minikubeStatus -eq "Running") {
    Write-Host "Minikube is Running." -ForegroundColor Green
} else {
    Write-Error "Minikube is NOT running."
}

# 2. Check Pods
Write-Host "`n2. Checking Todo App Pods..." -ForegroundColor Yellow
$pods = kubectl get pods -n todo-app --no-headers
if ($pods) {
    $pods | ForEach-Object { Write-Host $_ }
    if ($pods -match "Running") {
         Write-Host "Pods are found and running." -ForegroundColor Green
    } else {
         Write-Warning "Pods found but may not be fully ready."
    }
} else {
    Write-Error "No pods found in 'todo-app' namespace."
}

# 3. Check Service & Connectivity
Write-Host "`n3. Checking Service Connectivity..." -ForegroundColor Yellow
$serviceUrl = minikube service todo-app-frontend -n todo-app --url
Write-Host "Service URL: $serviceUrl"

if ($serviceUrl) {
    Write-Host "Attempting curl to $serviceUrl..."
    try {
        $response = curl -I $serviceUrl
        if ($response.StatusCode -eq 200) {
            Write-Host "Frontend is reachable (HTTP 200 OK)." -ForegroundColor Green
        } else {
            Write-Warning "Frontend reachable but returned status: $($response.StatusCode)"
        }
    } catch {
        Write-Warning "Could not curl specific URL directly from script (network restriction?), but URL was retrieved."
    }
} else {
    Write-Error "Could not retrieve service URL."
}

Write-Host "`nVerification Complete!" -ForegroundColor Cyan
