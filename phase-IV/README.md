# Phase 4: Todo Application - Local Kubernetes Deployment

## Overview

This repository contains the Phase 4 implementation of the Todo Chatbot application, featuring containerization and deployment to a local Kubernetes cluster using Minikube. The application consists of a Next.js frontend and a FastAPI backend, both containerized and orchestrated using Helm charts.

## Features

- **Containerized Architecture**: Multi-stage Docker builds for both frontend and backend
- **Kubernetes Orchestration**: Helm charts for easy deployment and management
- **Local Development**: Minikube-based local Kubernetes environment
- **AI Integration**: OpenAI-powered chatbot for natural language todo management
- **Scalable Design**: Designed for horizontal scaling with proper resource limits
- **Secure by Default**: Non-root containers and proper secrets management

## Architecture

The application follows a microservices architecture with:

- **Frontend**: Next.js application served via nginx in a Docker container
- **Backend**: FastAPI application with OpenAI integration
- **Database**: Neon PostgreSQL (external serverless database)
- **Orchestration**: Kubernetes with Helm charts for deployment

## Prerequisites

- Docker Desktop with Kubernetes enabled OR Minikube
- Helm 3.12+
- kubectl
- kubectl-ai (optional, for AI-assisted operations)

## 🔄 Daily Start Guide (How to Run)

Follow these steps every time you restart your laptop or want to look at the project:

1.  **Open Docker Desktop** and wait for it to be ready.
2.  **Open PowerShell as Administrator**.
3.  **Start the Cluster**:
    ```powershell
    minikube start
    ```
4.  **Start the Tunnel** (Required for the website to work):
    ```powershell
    minikube tunnel
    ```
    *Keep this window open! If it asks for a password, enter your computer password.*

5.  **Open your browser** and go to:
    **[http://127.0.0.1](http://127.0.0.1)**

---

## 🚀 One-Click Setup (New Installations Only)

To install everything initially (Images + Helm), you used:
```cmd
.\setup.bat
```

### Accessing the Application

- **URL**: [http://127.0.0.1](http://127.0.0.1)
- **Note**: Ensure `minikube tunnel` is running in an Administrator terminal.

## Documentation

- [Deployment Guide](docs/phase4/DEPLOYMENT.md)
- [Troubleshooting Guide](docs/phase4/TROUBLESHOOTING.md)
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
│       ├── values-dev.yaml
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
helm upgrade --install todo-app ./helm-charts/todo-app --namespace todo-app -f ./helm-charts/todo-app/values-dev.yaml
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Update documentation as needed
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.