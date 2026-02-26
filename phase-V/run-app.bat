@echo off
echo ==========================================
echo 🚀 Todo App Daily Runner (No Build)
echo ==========================================
powershell -Command "minikube start; Start-Process cmd -ArgumentList '/k', 'kubectl port-forward -n todo-app service/todo-app-frontend 3000:80'; Start-Process cmd -ArgumentList '/k', 'kubectl port-forward -n todo-app service/todo-app-backend 8000:80'"
echo.
echo ✅ Tunnels are starting in new windows...
echo 🌍 Visit: http://localhost:3000
pause
