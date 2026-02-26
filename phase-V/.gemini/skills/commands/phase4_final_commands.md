# Phase IV Commands - Local Kubernetes Deployment

## Spec-Kit Plus Commands for Phase 4

### 1. Initialize Phase IV Environment
```bash
# Initialize the project for Phase IV
specifyplus init hackathon-todo-phase4

# Update constitution with Phase IV principles
/specifyplus.constitution

# Add Phase 4 specific principles:
# - Containerization standards using Docker best practices
# - Kubernetes manifest conventions
# - Helm chart structure and values management
# - Local development with Minikube requirements
# - Health checks and readiness probes
# - Resource limits and requests standards
```

### 2. Phase IV Specification Commands
```bash
# Define Phase 4 features
/specifyplus.specify

# Feature Name: Phase 4 - Local Kubernetes Deployment

# Key User Stories:
# US-4.1: Container Images - Containerize frontend and backend applications
# US-4.2: Helm Chart Creation - Create Helm charts for easy deployment
# US-4.3: Minikube Deployment - Deploy to local Minikube cluster

# Technical Requirements:
# TR-4.1: Container Requirements - Optimized Docker images
# TR-4.2: Kubernetes Requirements - Minikube with required addons
# TR-4.3: Helm Requirements - Proper chart structure and validation
```

### 3. Clarify Specification
```bash
# Clarify the specification details
/specifyplus.clarify

# Review for:
# 1. Docker build strategy (multi-stage vs single-stage)
# 2. Image registry choice (local Minikube registry)
# 3. Database connection (continue using Neon or local PostgreSQL in K8s)
# 4. Secrets management approach (Kubernetes Secrets)
# 5. Service exposure (Ingress vs NodePort)
# 6. Resource limits (CPU/memory) for each service
# 7. Helm chart structure (umbrella chart vs separate charts)
```

### 4. Generate Implementation Plan
```bash
# Generate detailed implementation plan
/specifyplus.plan

# Key Architecture Decisions:
# AD-4.1: Containerization Strategy - Multi-stage Docker builds
# AD-4.2: Kubernetes Architecture - Single namespace with proper services
# AD-4.3: Helm Chart Structure - Umbrella chart with organized templates
# AD-4.4: Image Registry Strategy - Minikube local registry
# AD-4.5: Database Strategy - Continue using Neon Serverless PostgreSQL
# AD-4.6: Service Exposure Strategy - Minikube Ingress
```

### 5. Create Task Breakdown
```bash
# Break down the plan into atomic tasks
/specifyplus.tasks

# Task Groups for Phase IV:

## Task Group 1: Environment Setup
# Task 1.1: Install and Configure Minikube
# - Start Minikube with Docker driver
# - Enable ingress and metrics-server addons
# - Verify cluster is ready

# Task 1.2: Install Helm
# - Install Helm 3.12+
# - Verify installation
# - Add any required repositories

## Task Group 2: Containerization
# Task 2.1: Create Frontend Dockerfile
# - Multi-stage build for Next.js app
# - Use node:20-alpine base image
# - Optimize build layers
# - Run as non-root user

# Task 2.2: Create Backend Dockerfile
# - Multi-stage build for FastAPI app
# - Use python:3.13-slim base image
# - Install dependencies efficiently
# - Run as non-root user

# Task 2.3: Create Docker ignore files
# - Create .dockerignore for frontend
# - Create .dockerignore for backend

# Task 2.4: Build Docker images
# - Build frontend image
# - Build backend image
# - Tag images appropriately
# - Test images locally

## Task Group 3: Helm Chart Creation
# Task 3.1: Initialize Helm chart structure
# - Create umbrella chart directory
# - Set up proper folder structure
# - Define Chart.yaml metadata

# Task 3.2: Create values.yaml
# - Define default configuration values
# - Set up frontend and backend configs
# - Define ingress configuration
# - Set up placeholder secrets

# Task 3.3: Create frontend templates
# - Deployment template
# - Service template
# - ConfigMap template

# Task 3.4: Create backend templates
# - Deployment template
# - Service template
# - Secret template

# Task 3.5: Create ingress template
# - Configure Ingress resource
# - Set up routing rules
# - Define host and paths

# Task 3.6: Validate Helm chart
# - Run helm lint
# - Run helm template
# - Fix any validation errors

## Task Group 4: Deployment Scripts
# Task 4.1: Create Minikube setup script
# - Automate Minikube start
# - Enable required addons
# - Set up hosts entry

# Task 4.2: Create image build script
# - Automate Docker image building
# - Set Minikube Docker environment
# - Tag and push images

# Task 4.3: Create deployment script
# - Automate Helm deployment
# - Create namespace
# - Install/upgrade release

# Task 4.4: Create cleanup script
# - Uninstall Helm release
# - Delete namespace
# - Clean up resources

## Task Group 5: Deployment and Testing
# Task 5.1: Deploy to Minikube
# - Run setup script
# - Build images
# - Deploy via Helm

# Task 5.2: Verify services
# - Check pod status
# - Test service connectivity
# - Access via Ingress

# Task 5.3: End-to-end testing
# - Test complete user workflow
# - Verify database connectivity
# - Test chatbot functionality

## Task Group 6: Documentation
# Task 6.1: Create deployment guide
# Task 6.2: Create troubleshooting guide
# Task 6.3: Update main README
```

### 6. Execute Implementation
```bash
# Execute tasks in sequence
/specifyplus.implement

# Implementation Rounds:
# Round 1: Setup (Tasks 1.1-1.2) - Environment preparation
# Round 2: Dockerfiles (Tasks 2.1-2.4) - Containerization
# Round 3: Helm Chart (Tasks 3.1-3.6) - Chart creation
# Round 4: Scripts (Tasks 4.1-4.4) - Automation scripts
# Round 5: Deploy (Tasks 5.1-5.3) - Deployment and testing
# Round 6: Document (Tasks 6.1-6.3) - Documentation
```

## Kubernetes-Specific Commands for Phase IV

### Minikube Commands
```bash
# Start Minikube cluster
minikube start --driver=docker --cpus=4 --memory=8192

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server

# Set Docker environment to Minikube
eval $(minikube docker-env)

# Check cluster status
kubectl cluster-info
kubectl get nodes

# Access Minikube dashboard
minikube dashboard
```

### Docker Commands for Containerization
```bash
# Build frontend image
docker build -t todo-frontend:v1.0 ./frontend

# Build backend image
docker build -t todo-backend:v1.0 ./backend

# Tag images for local registry
docker tag todo-frontend:v1.0 localhost:5000/todo-frontend:v1.0
docker tag todo-backend:v1.0 localhost:5000/todo-backend:v1.0

# Push to local registry
docker push localhost:5000/todo-frontend:v1.0
docker push localhost:5000/todo-backend:v1.0

# Check built images
docker images | grep todo
```

### Helm Commands for Deployment
```bash
# Create Helm chart
helm create helm-charts/todo-app

# Lint the chart
helm lint helm-charts/todo-app

# Template the chart (dry run)
helm template todo-app helm-charts/todo-app

# Install/upgrade the release
helm upgrade --install todo-app helm-charts/todo-app --namespace todo-app --create-namespace

# Check release status
helm status todo-app -n todo-app

# List releases
helm list -n todo-app

# Uninstall release
helm uninstall todo-app -n todo-app
```

### Kubernetes Commands for Management
```bash
# Create namespace
kubectl create namespace todo-app

# Check deployments
kubectl get deployments -n todo-app

# Check pods
kubectl get pods -n todo-app

# Check services
kubectl get services -n todo-app

# Check ingress
kubectl get ingress -n todo-app

# Check logs
kubectl logs -l app=frontend -n todo-app
kubectl logs -l app=backend -n todo-app

# Port forward for testing
kubectl port-forward svc/frontend 3000:3000 -n todo-app
kubectl port-forward svc/backend 8000:8000 -n todo-app

# Describe resources for debugging
kubectl describe pod <pod-name> -n todo-app
kubectl describe deployment <deployment-name> -n todo-app
```

### Deployment Script Commands
```bash
# Run the complete deployment process
./scripts/minikube-setup.sh
./scripts/build-images.sh
./scripts/deploy.sh

# Verify deployment
./scripts/verify-deployment.sh

# Cleanup when done
./scripts/cleanup.sh
```

## Integration with Available Skills

### Using Docker Expert Skill
```bash
# Use the docker-expert skill for Dockerfile optimization
Use the docker-expert skill proactively for:
- Dockerfile optimization
- Multi-stage build improvements
- Image size reduction
- Security hardening
- Container networking
```

### Using Kubernetes Specialist Skill
```bash
# Use the kubernetes-specialist skill for deployment
Use the kubernetes-specialist skill for:
- Kubernetes manifest optimization
- Resource configuration
- Security best practices
- Performance tuning
- Troubleshooting
```

### Using Helm Chart Scaffolding Skill
```bash
# Use the helm-chart-scaffolding skill for chart creation
Use the helm-chart-scaffolding skill for:
- Helm chart structure
- Template creation
- Values management
- Chart validation
- Packaging
```

### Using DevOps Engineer Skill
```bash
# Use the devops-engineer skill for infrastructure setup
Use the devops-engineer skill for:
- CI/CD pipeline setup
- Infrastructure as code
- Cloud platform integration
- GitOps workflows
- Container registry management
```

## MCP Server Commands for Phase IV

Create MCP prompts in `.claude/commands/` directory:

### Containerization Prompt
```
Command: containerize-application
Description: Create Dockerfiles and build container images for frontend and backend
Input:
- app_type: frontend or backend
- image_name: name for the Docker image
- build_context: path to build context
Action: Generate Dockerfile and build the image
```

### Kubernetes Deployment Prompt
```
Command: deploy-to-kubernetes
Description: Deploy the application to a Kubernetes cluster
Input:
- cluster_type: minikube, kind, or remote
- namespace: target namespace
- app_name: name of the application
Action: Create and apply Kubernetes manifests
```

### Helm Chart Generation Prompt
```
Command: generate-helm-chart
Description: Create a Helm chart for the application
Input:
- chart_name: name of the Helm chart
- app_version: application version
- namespace: target namespace
Action: Generate Helm chart templates and values
```

## Final Validation Commands
```bash
# Complete end-to-end validation
# 1. Verify all pods are running
kubectl get pods -n todo-app

# 2. Verify services are accessible
kubectl get services -n todo-app

# 3. Test ingress connectivity
minikube service list -n todo-app

# 4. Access the application
# Frontend: http://todo.local (if hosts entry added)
# Or use port forwarding: kubectl port-forward

# 5. Test the chatbot functionality
# Verify all Phase III features still work in Kubernetes environment
```