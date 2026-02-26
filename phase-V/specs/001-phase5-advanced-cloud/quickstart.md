# Quickstart Guide: Phase 5 Advanced Cloud Deployment

This guide outlines the steps to quickly set up and run the Phase 5 Advanced Cloud Deployment features locally using Minikube, Dapr, and Kafka.

## Prerequisites

-   **Git**: Latest version installed.
-   **Docker Desktop**: Version 4.35+ installed and running.
-   **Minikube**: Version 1.33+ installed and configured. Ensure it's running: `minikube start`
-   **kubectl**: Configured to interact with your Minikube cluster.
-   **Dapr CLI**: Version 1.16+ installed.
-   **Helm**: Version 3.16+ installed.
-   **Python**: Version 3.13 installed (for backend services).
-   **Node.js**: Latest LTS version installed (for frontend).
-   **Poetry**: Python package manager: `pip install poetry`
-   **pnpm**: Node.js package manager: `npm install -g pnpm`
-   **Neon DB**: An external Neon Serverless PostgreSQL instance created and connection string obtained.

## 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_root>
```

## 2. Checkout Feature Branch

Switch to the feature branch for Phase 5 development:

```bash
git checkout 001-phase5-advanced-cloud
```

## 3. Set up Minikube and Dapr

Ensure Minikube is running and Dapr is initialized on the cluster:

```bash
minikube start
dapr init -k
```

Verify Dapr control plane pods are running in the `dapr-system` namespace:

```bash
kubectl get pods -n dapr-system
```

## 4. Install Kafka using Helm

Deploy Kafka to your Minikube cluster using the Bitnami Helm chart.

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
kubectl create namespace kafka # If not already created
helm install kafka bitnami/kafka --version 30.x --namespace kafka 
  --set replicaCount=1 
  --set zookeeper.replicaCount=1 
  --set auth.clientProtocol=plaintext 
  --set auth.interBrokerProtocol=plaintext 
  --set service.type=ClusterIP # Use ClusterIP for Minikube
```

Verify Kafka pods are running:

```bash
kubectl get pods -n kafka
```

## 5. Configure Dapr Components

Apply the Dapr components (Pub/Sub, State Store, Secrets) to the `todo-app` namespace.

First, create the `todo-app` namespace:
```bash
kubectl create namespace todo-app
```

Then, apply the Dapr components YAMLs (ensure these files are created in `dapr/components` or similar):

```bash
# Assuming dapr components YAMLs are in specs/001-phase5-advanced-cloud/contracts/
# You might need to adjust paths based on actual implementation location
kubectl apply -f specs/001-phase5-advanced-cloud/contracts/dapr-pubsub-kafka.yaml -n todo-app
kubectl apply -f specs/001-phase5-advanced-cloud/contracts/dapr-statestore.yaml -n todo-app
kubectl apply -f specs/001-phase5-advanced-cloud/contracts/dapr-secrets.yaml -n todo-app
```

**Note**: Before applying `dapr-statestore.yaml`, you must create a Kubernetes Secret named `neon-db-secret` in the `todo-app` namespace containing your Neon DB connection string.

```bash
kubectl create secret generic neon-db-secret --from-literal=connection-string='<YOUR_NEON_DB_CONNECTION_STRING>' -n todo-app
```

Replace `<YOUR_NEON_DB_CONNECTION_STRING>` with your actual connection string.

## 6. Build and Deploy Application Services

This phase requires building Docker images for each service (Frontend, Backend, Recurring Task Service, Notification Service) and deploying them using Helm charts.

### 6.1. Build Docker Images

Navigate to each service's directory (e.g., `backend/`, `frontend/`) and build its Docker image:

```bash
# Example for backend
cd backend
docker build -t todo-backend:latest .
eval $(minikube docker-env) # Point Docker to Minikube's daemon
docker build -t todo-backend:latest . # Rebuild using Minikube's daemon
cd ..

# Repeat for frontend, recurring-service, notification-service
# cd frontend && eval $(minikube docker-env) && docker build -t todo-frontend:latest . && cd ..
# cd recurring-service && eval $(minikube docker-env) && docker build -t recurring-service:latest . && cd ..
# cd notification-service && eval $(minikube docker-env) && docker build -t notification-service:latest . && cd ..
```

### 6.2. Deploy with Helm

Deploy the application using the umbrella Helm chart:

```bash
# Assuming the umbrella chart is at helm-charts/todo-app/
helm install todo-app helm-charts/todo-app --namespace todo-app
```

Verify all application pods are running and Dapr sidecars are injected:

```bash
kubectl get pods -n todo-app
```

## 7. Access the Application

To access the frontend, you'll likely need to use `minikube service` or set up port-forwarding:

```bash
minikube service todo-frontend -n todo-app
```

This will open the frontend in your browser.

## 8. Development Workflow

-   Make code changes in your local environment.
-   Rebuild Docker images for affected services (`eval $(minikube docker-env)` then `docker build`).
-   Upgrade the Helm deployment (`helm upgrade todo-app helm-charts/todo-app -n todo-app`).
-   Monitor logs using `kubectl logs -f <pod-name> -n <namespace>`.
-   Use Dapr CLI for debugging, e.g., `dapr invoke --app-id todo-backend --method /health/live`.
