@echo off
echo Starting Port Forwarding Tunnels...
echo.
echo 1. Opening Frontend Tunnel (Local 3000 -> Service 80)...
start "Todo Frontend" cmd /k "kubectl port-forward -n todo-app service/todo-app-frontend 3000:80"

echo 2. Opening Backend Tunnel (Local 8000 -> Service 80)...
start "Todo Backend" cmd /k "kubectl port-forward -n todo-app service/todo-app-backend 8000:80"

echo.
echo ✅ Tunnels started!
echo ⚠️  If the new windows close immediately or show errors, please check them.
echo.
echo App: http://localhost:3000
echo API: http://localhost:8000
echo.
pause
