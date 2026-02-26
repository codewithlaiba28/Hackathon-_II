# Phase IV Commands - Local Kubernetes Deployment

## Spec-Kit Plus Commands

### 1. Initialize Spec-Kit Plus for Phase IV
```bash
# Initialize the project for Phase IV
specifyplus init hackathon-todo-phase4

# Create the constitution for Phase IV
specifyplus constitution
```

### 2. Phase IV Specification Commands
```bash
# Create Phase IV specifications
specifyplus specify --phase "Phase IV: Local Kubernetes Deployment"

# Define the requirements for containerization
specifyplus clarify --topic "Docker Containerization Requirements"

# Generate the technical plan for Kubernetes deployment
specifyplus plan --target "Minikube Deployment"

# Create task breakdown for Phase IV
specifyplus tasks --breakdown "Kubernetes Deployment Tasks"
```

### 3. Containerization Commands
```bash
# Create Dockerfiles for frontend and backend
specifyplus implement --feature "Docker Containerization"

# Build Docker images
docker build -t hackathon-todo-frontend ./frontend
docker build -t hackathon-todo-backend ./backend

# Tag images for local registry
docker tag hackathon-todo-frontend localhost:5000/hackathon-todo-frontend
docker tag hackathon-todo-backend localhost:5000/hackathon-todo-backend
```

### 4. Kubernetes Commands
```bash
# Start Minikube
minikube start

# Enable required addons
minikube addons enable ingress
minikube addons enable registry

# Create Kubernetes manifests
kubectl create namespace todo-app
kubectl config set-context --current --namespace=todo-app

# Deploy to Kubernetes
specifyplus deploy --platform kubernetes --environment local
```

### 5. Helm Chart Commands
```bash
# Create Helm chart structure
helm create todo-app-chart

# Package the Helm chart
helm package todo-app-chart

# Install the Helm chart
helm install todo-app ./todo-app-chart --namespace todo-app

# Upgrade the Helm chart
helm upgrade todo-app ./todo-app-chart --namespace todo-app

# Uninstall the Helm chart
helm uninstall todo-app --namespace todo-app
```

### 6. MCP Server Commands for Phase IV
```bash
# Initialize MCP server for Phase IV
specifyplus mcp init --name "phase4-mcp-server"

# Add Phase IV specific commands to MCP
specifyplus mcp add-command --name "containerize-app" --description "Containerize frontend and backend apps"
specifyplus mcp add-command --name "deploy-minikube" --description "Deploy to local Minikube cluster"
specifyplus mcp add-command --name "create-helm-charts" --description "Generate Helm charts for deployment"
specifyplus mcp add-command --name "configure-dapr" --description "Configure Dapr for the application"
```

### 7. Docker Commands for Phase IV
```bash
# Build and push images to local registry
docker build -t localhost:5000/todo-frontend:latest ./frontend
docker push localhost:5000/todo-frontend:latest

docker build -t localhost:5000/todo-backend:latest ./backend
docker push localhost:5000/todo-backend:latest

# Verify images
docker images | grep todo
```

### 8. Kubernetes Resource Management
```bash
# Create ConfigMaps and Secrets
kubectl create configmap app-config --from-literal=NODE_ENV=production
kubectl create secret generic app-secrets --from-literal=DB_PASSWORD=password --from-literal=JWT_SECRET=secret

# Apply Kubernetes manifests
kubectl apply -f k8s/manifests/

# Check deployment status
kubectl get pods,svc,ingress,configmaps,secrets

# Port forward for testing
kubectl port-forward svc/todo-backend 8000:8000
```

### 9. Dapr Integration Commands
```bash
# Initialize Dapr
dapr init -k

# Create Dapr component files
mkdir -p dapr-components
kubectl apply -f dapr-components/

# Run application with Dapr
dapr run --app-id todo-backend --app-port 8000 -- uvicorn main:app --reload
```

### 10. Monitoring and Validation
```bash
# Check cluster status
kubectl cluster-info
kubectl get nodes

# Monitor deployment
kubectl get deployments
kubectl get pods
kubectl describe pod <pod-name>

# View logs
kubectl logs -f deployment/todo-backend
kubectl logs -f deployment/todo-frontend

# Test ingress
minikube service list
minikube tunnel  # Run in separate terminal
```

### 11. Phase IV Specific MCP Commands
```bash
# Execute Phase IV workflow
specifyplus run-workflow --phase "Phase IV" --steps "containerize,deploy,helm,dapr"

# Validate Phase IV completion
specifyplus validate --phase "Phase IV" --criteria "kubernetes-deployment-success"

# Generate Phase IV report
specifyplus report --phase "Phase IV" --format "kubernetes-deployment-summary"
```

### 12. Cleanup Commands
```bash
# Clean up Phase IV resources
kubectl delete namespace todo-app

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete

# Remove Docker images
docker rmi -f $(docker images --filter=reference='*todo*')
```

## MCP Server Configuration for Phase IV

Create a `.claude/commands/phase4-commands` directory structure with the following commands as MCP prompts:

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

### Dapr Configuration Prompt
```
Command: configure-dapr
Description: Set up Dapr for the application
Input:
- app_id: Dapr application ID
- app_port: application port
- components: list of Dapr components to configure
Action: Create Dapr component files and annotate deployments
```