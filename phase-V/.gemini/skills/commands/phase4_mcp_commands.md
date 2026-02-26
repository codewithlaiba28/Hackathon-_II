# MCP Commands for Phase IV - Local Kubernetes Deployment

## Overview
This document contains MCP (Model Context Protocol) commands specifically designed for Phase IV of the hackathon: Local Kubernetes Deployment. These commands can be integrated into an MCP server to automate the deployment workflow.

## MCP Command Definitions

### 1. Containerization Commands

#### Command: create-dockerfiles
```
Purpose: Generate Dockerfiles for frontend and backend applications
Parameters:
  - app_type (required): "frontend" or "backend"
  - base_image (optional): base image to use (defaults to node:18-alpine for frontend, python:3.11-slim for backend)
  - port (optional): application port (defaults to 3000 for frontend, 8000 for backend)

Implementation:
- Creates a Dockerfile for the specified application type
- Optimizes for multi-stage build if possible
- Sets up proper environment variables
- Exposes the correct port
```

#### Command: build-docker-images
```
Purpose: Build Docker images for the application
Parameters:
  - frontend_tag (optional): tag for frontend image (defaults to "latest")
  - backend_tag (optional): tag for backend image (defaults to "latest")
  - push_registry (optional): registry to push to (defaults to none)

Implementation:
- Builds both frontend and backend Docker images
- Tags them appropriately
- Optionally pushes to specified registry
- Verifies images were built successfully
```

### 2. Kubernetes Commands

#### Command: setup-minikube
```
Purpose: Initialize and configure Minikube for the deployment
Parameters:
  - driver (optional): VM driver to use (defaults to auto-detect)
  - memory (optional): memory allocation in MB (defaults to 4096)
  - cpus (optional): CPU allocation (defaults to 2)

Implementation:
- Starts Minikube with specified configuration
- Enables required addons (ingress, registry, metrics-server)
- Sets up local registry mirror if needed
- Verifies cluster is ready
```

#### Command: create-k8s-manifests
```
Purpose: Generate Kubernetes manifests for the application
Parameters:
  - namespace (optional): target namespace (defaults to "todo-app")
  - replica_count (optional): number of replicas (defaults to 1)
  - resource_limits (optional): CPU/memory limits

Implementation:
- Creates Deployment manifests for frontend and backend
- Creates Service definitions
- Creates ConfigMap for environment variables
- Creates Secret for sensitive data
- Creates Ingress for external access
```

#### Command: deploy-to-k8s
```
Purpose: Deploy the application to Kubernetes
Parameters:
  - namespace (optional): target namespace (defaults to "todo-app")
  - wait_for_ready (optional): whether to wait for pods to be ready (defaults to true)

Implementation:
- Applies all generated manifests to the cluster
- Waits for deployments to be ready
- Reports deployment status
```

### 3. Helm Commands

#### Command: create-helm-chart
```
Purpose: Create a Helm chart for the application
Parameters:
  - chart_name (optional): name of the chart (defaults to "todo-app")
  - app_version (optional): application version (defaults to "0.1.0")
  - chart_version (optional): chart version (defaults to "0.1.0")

Implementation:
- Creates Helm chart structure with templates
- Generates values.yaml with configurable parameters
- Creates Chart.yaml with metadata
- Validates chart structure
```

#### Command: install-helm-release
```
Purpose: Install the Helm release to the cluster
Parameters:
  - release_name (optional): name of the release (defaults to "todo-app")
  - namespace (optional): target namespace (defaults to "todo-app")
  - values_file (optional): path to custom values file

Implementation:
- Installs the Helm chart as a release
- Monitors installation progress
- Reports installation status
```

### 4. Dapr Commands

#### Command: setup-dapr
```
Purpose: Install and configure Dapr in the Kubernetes cluster
Parameters:
  - runtime_version (optional): Dapr runtime version (defaults to latest stable)
  - namespace (optional): Dapr system namespace (defaults to "dapr-system")

Implementation:
- Initializes Dapr in the Kubernetes cluster
- Verifies Dapr control plane is running
- Reports Dapr status
```

#### Command: configure-dapr-components
```
Purpose: Create Dapr component configurations
Parameters:
  - pubsub_component (optional): pub/sub component type (defaults to "redis")
  - state_component (optional): state store component (defaults to "redis")
  - namespace (optional): target namespace (defaults to "todo-app")

Implementation:
- Creates Dapr component YAML files
- Configures pub/sub for messaging
- Configures state management
- Applies components to the cluster
```

### 5. Validation Commands

#### Command: validate-deployment
```
Purpose: Validate that the application is properly deployed
Parameters:
  - namespace (optional): namespace to validate (defaults to "todo-app")
  - timeout_seconds (optional): timeout for validation (defaults to 300)

Implementation:
- Checks all pods are running and ready
- Verifies services are accessible
- Tests ingress connectivity
- Reports validation results
```

#### Command: run-health-checks
```
Purpose: Perform health checks on the deployed application
Parameters:
  - frontend_url (required): URL of the frontend service
  - backend_url (required): URL of the backend service

Implementation:
- Tests frontend health endpoint
- Tests backend health endpoint
- Verifies API connectivity
- Reports health status
```

### 6. Monitoring Commands

#### Command: setup-monitoring
```
Purpose: Set up monitoring for the application
Parameters:
  - enable_logging (optional): whether to enable logging (defaults to true)
  - enable_metrics (optional): whether to enable metrics (defaults to true)
  - prometheus_enabled (optional): whether to deploy Prometheus (defaults to false)

Implementation:
- Creates monitoring configurations
- Sets up service monitors if Prometheus is enabled
- Configures logging if enabled
- Reports monitoring setup status
```

### 7. Cleanup Commands

#### Command: cleanup-phase4
```
Purpose: Clean up all resources created during Phase IV
Parameters:
  - namespace (optional): namespace to clean up (defaults to "todo-app")
  - delete_namespace (optional): whether to delete the namespace (defaults to false)

Implementation:
- Deletes all deployments, services, and other resources
- Removes Helm releases if installed
- Cleans up Dapr components if configured
- Reports cleanup status
```

## MCP Server Configuration

To implement these commands in an MCP server, you would create an endpoint that accepts these commands and executes the corresponding implementations. Each command should return structured responses with:
- status: success, error, or in-progress
- message: human-readable status message
- data: any relevant data from the command execution
- next_steps: suggested next actions if applicable

## Usage Examples

### Example 1: Full deployment sequence
```
1. setup-minikube
2. create-dockerfiles (frontend)
3. create-dockerfiles (backend)
4. build-docker-images
5. create-k8s-manifests
6. deploy-to-k8s
7. validate-deployment
```

### Example 2: Helm-based deployment
```
1. create-helm-chart
2. install-helm-release
3. validate-deployment
```

### Example 3: Dapr-enhanced deployment
```
1. setup-dapr
2. configure-dapr-components
3. deploy-to-k8s (with Dapr annotations)
4. run-health-checks
```