@echo off
echo Opening Todo App in your browser...
echo NOTE: Keep this window OPEN. Closing it will stop the tunnel.
minikube service todo-app-frontend -n todo-app
