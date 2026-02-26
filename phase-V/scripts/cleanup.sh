#!/bin/bash

# Script: cleanup.sh
# Description: Clean up resources created by the todo application

set -e  # Exit on any error

echo "Cleaning up resources..."

# Check if Helm is available
if ! command -v helm &> /dev/null; then
    echo "Warning: Helm is not installed, skipping Helm cleanup"
else
    # Uninstall Helm release if it exists
    if helm status todo-app -n todo-app &> /dev/null; then
        echo "Uninstalling Helm release todo-app..."
        helm uninstall todo-app -n todo-app
    else
        echo "Helm release todo-app not found, skipping..."
    fi
fi

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "Warning: kubectl is not installed, skipping Kubernetes cleanup"
else
    # Delete namespace if it exists
    if kubectl get namespace todo-app &> /dev/null; then
        echo "Deleting namespace todo-app..."
        kubectl delete namespace todo-app
    else
        echo "Namespace todo-app not found, skipping..."
    fi
fi

# Optionally stop Minikube
read -p "Do you want to stop Minikube? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Stopping Minikube..."
    minikube stop
fi

# Optionally remove todo.local from /etc/hosts
read -p "Do you want to remove todo.local from /etc/hosts? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing todo.local from /etc/hosts (requires sudo)..."
    sudo sed -i '/todo.local/d' /etc/hosts
fi

echo "Cleanup completed!"