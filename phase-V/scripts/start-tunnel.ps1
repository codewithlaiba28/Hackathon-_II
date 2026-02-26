$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting Port Forwarding Tunnel..." -ForegroundColor Cyan
Write-Host "This will allow you to access the app at http://localhost:3000"
Write-Host "and the API at http://localhost:8000"
Write-Host "Keep this window OPEN!" -ForegroundColor Yellow

# Start port forwarding in parallel jobs
Start-Job -ScriptBlock { kubectl port-forward -n todo-app service/todo-app-frontend 3000:80 }
Start-Job -ScriptBlock { kubectl port-forward -n todo-app service/todo-app-backend 8000:80 }

# Keep the script running
while ($true) {
    Start-Sleep -Seconds 5
    Write-Host "." -NoNewline -ForegroundColor Gray
}
