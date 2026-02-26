#!/bin/bash

# Script: minikube-setup.sh
# Description: Set up Minikube cluster with necessary addons

set -e  # Exit on any error

echo "Setting up Minikube cluster..."

# Check if Minikube is available
if ! command -v minikube &> /dev/null; then
    echo "Error: Minikube is not installed"
    exit 1
fi

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed"
    exit 1
fi

# Start Minikube with Docker driver and adequate resources
echo "Starting Minikube with Docker driver..."
minikube start --driver=docker --cpus=4 --memory=8192

# Enable required addons
echo "Enabling ingress addon..."
minikube addons enable ingress

echo "Enabling metrics-server addon..."
minikube addons enable metrics-server

# Display cluster info
echo "Minikube cluster started successfully!"
echo ""
kubectl cluster-info
echo ""
echo "Cluster status:"
kubectl get nodes
echo ""

# Add entry to /etc/hosts for todo.local (this requires sudo)
echo "Adding todo.local to /etc/hosts (requires sudo)..."
sudo sh -c 'echo "$(minikube ip) todo.local" >> /etc/hosts'

echo "Minikube setup completed successfully!"
echo "You can now access your services via http://todo.local if using Ingress"