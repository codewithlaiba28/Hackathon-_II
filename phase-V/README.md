# Phase 5: Todo Application - Advanced Cloud-Native Features (Dapr, Kafka, Kubernetes)

## Overview

This repository contains the Phase 5 implementation of the Todo Chatbot application, featuring advanced cloud-native capabilities. It utilizes Dapr for building block capabilities (state management, pub/sub, secrets), Apache Kafka for event streaming, and Kubernetes for orchestration. The application consists of a Next.js frontend, a FastAPI backend, a Recurring Task Service, and a Notification Service, all containerized and orchestrated using Helm charts.

## Features

- **Containerized Architecture**: Multi-stage Docker builds for all services (Frontend, Backend, Recurring Tasks, Notifications).
- **Kubernetes Orchestration**: Helm charts for easy deployment and management on a local Kubernetes cluster (Minikube).
- **Dapr Integration**: Leverages Dapr building blocks for state management (PostgreSQL), publish/subscribe (Kafka), and secret management.
- **Event-Driven Microservices**: Utilizes Apache Kafka for asynchronous communication between services (e.g., task completion events, reminders).
- **Advanced Task Management**: Recurring tasks, reminders, priority, tags, and due dates.
- **Local Development**: Minikube-based local Kubernetes environment with Dapr.
- **AI Integration**: OpenAI-powered chatbot for natural language todo management.
- **Scalable Design**: Designed for horizontal scaling with proper resource limits.
- **Secure by Default**: Non-root containers and robust secrets management.
- **Structured Logging**: Implemented with correlation IDs for improved observability.
- **Health Checks**: Liveness and readiness probes configured for all services.

## Architecture

The application follows a microservices architecture leveraging cloud-native patterns:

- **Frontend**: Next.js application, containerized, exposed via Kubernetes Ingress.
- **Backend**: FastAPI application, containerized, handles core API logic, integrates with Dapr for state and pub/sub.
- **Recurring Task Service**: FastAPI application, containerized, subscribes to task events from Kafka via Dapr Pub/Sub to manage recurring tasks.
- **Notification Service**: FastAPI application, containerized, subscribes to reminder events from Kafka via Dapr Pub/Sub to send notifications.
- **Database**: Neon Serverless PostgreSQL (external), used as Dapr state store.
- **Message Broker**: Apache Kafka (deployed via Helm), used as Dapr Pub/Sub component.
- **Orchestration**: Kubernetes with Helm charts for deployment and Dapr sidecars for inter-service communication and building blocks.
- **Authentication**: Better Auth JWT for user authentication.

## Prerequisites

- Docker Desktop with Kubernetes enabled OR Minikube
- Helm 3.12+
- kubectl
- kubectl-ai (optional, for AI-assisted operations)

## 🚀 One-Click Setup (Recommended)

To start everything (Minikube + Images + Helm + Tunnels), simply run:
```cmd
.\setup.bat
```

### Manual Setup Steps (if needed)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hackathon-todo/phase-IV
```

### 2. Set Up Minikube (if not using Docker Desktop Kubernetes)

```bash
minikube start --driver=docker --cpus=4 --memory=8192
minikube addons enable ingress
minikube addons enable metrics-server
```

### 3. Build Docker Images

Please refer to the [Quickstart Guide](specs/001-kubernetes-deployment/quickstart.md) for detailed instructions on building Docker images for all services.

### 4. Deploy with Helm

```bash
# Navigate to helm-charts directory
cd helm-charts

# Install the chart. Ensure your values.yaml is configured as needed.
helm upgrade --install todo-app ./todo-app \
  --namespace todo-app \
  --create-namespace
```

### 5. Access the Application

```bash
# Add entry to /etc/hosts
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts

# Visit http://todo.local in your browser
```

## Documentation

- [Quickstart Guide](specs/001-kubernetes-deployment/quickstart.md)
- [Deployment Guide](docs/phase4/DEPLOYMENT.md) # This might need updating for Phase 5
- [Troubleshooting Guide](docs/phase4/TROUBLESHOOTING.md) # This might need updating for Phase 5
- [AI Ops Guide (Gordon, kubectl-ai, kagent)](docs/phase4/AI_OPS.md)
- [kubectl-ai Usage Guide](docs/phase4/KUBECTL-AI-GUIDE.md)

## Project Structure

```
├── backend/                    # FastAPI backend application
│   ├── Dockerfile             # Multi-stage build for backend
│   └── .dockerignore
├── frontend/                   # Next.js frontend application
│   ├── Dockerfile             # Multi-stage build for frontend
│   └── .dockerignore
├── helm-charts/               # Helm charts for Kubernetes deployment
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
├── scripts/                   # Automation scripts
│   ├── build-images.sh        # Build Docker images
│   ├── hotfix-backend.ps1     # Fix for backend chatkit crash
│   ├── start-tunnel-visible.bat # **REQUIRED**: Port forwarding for local access
│   ├── verify-deployment.ps1  # Automated deployment verification
│   └── ...
├── docs/                      # Documentation
│   └── phase4/
│       ├── AI_OPS.md          # **Gordon, kubectl-ai, kagent Guide**
│       ├── DEPLOYMENT.md      # Detailed deployment steps
│       └── TROUBLESHOOTING.md # Common fixes
└── README.md
```

## ✅ Verification & Usage

1. **Start the Tunnel** (Required for `localhost` access):
   ```cmd
   .\scripts\start-tunnel-visible.bat
   ```
   *Keep the new windows open!*

2. **Verify Deployment**:
   ```powershell
   .\scripts\verify-deployment.ps1
   ```

3. **AI Ops & Gordon**:
   See [docs/phase4/AI_OPS.md](docs/phase4/AI_OPS.md) for instructions on using Docker AI and agents.

## Development

### Running Locally

For local development without Kubernetes:

```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Updating Helm Charts

After making changes to the Helm templates:

```bash
# Test template rendering
helm template todo-app ./helm-charts/todo-app --namespace todo-app

# Validate chart
helm lint ./helm-charts/todo-app

# Deploy changes
helm upgrade --install todo-app ./helm-charts/todo-app --namespace todo-app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Update documentation as needed
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.