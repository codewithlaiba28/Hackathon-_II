# Data Model: Phase 4 - Local Kubernetes Deployment

## Kubernetes Resources

### Namespace
- **Purpose**: Isolate application resources
- **Name**: `todo-app`
- **Labels**: `app.kubernetes.io/name=todo-app`

### Frontend Deployment
- **Replicas**: 2 (configurable via values.yaml)
- **Image**: `todo-frontend:{version}`
- **Ports**: 3000 (nginx serving Next.js build)
- **Environment Variables**:
  - `NEXT_PUBLIC_API_URL`: Backend API URL
- **Resource Requests/Limits**: Per research document
- **Health Probes**: Per research document

### Backend Deployment
- **Replicas**: 2 (configurable via values.yaml)
- **Image**: `todo-backend:{version}`
- **Ports**: 8000 (FastAPI application)
- **Environment Variables**:
  - `DATABASE_URL`: From secret
  - `OPENAI_API_KEY`: From secret
  - `BETTER_AUTH_SECRET`: From secret
  - `NEXT_PUBLIC_BETTER_AUTH_URL`: Frontend URL
- **Resource Requests/Limits**: Per research document
- **Health Probes**: Per research document

### Frontend Service
- **Type**: ClusterIP
- **Port**: 80 (external) -> 3000 (internal)
- **Selector**: Match frontend deployment

### Backend Service
- **Type**: ClusterIP
- **Port**: 80 (external) -> 8000 (internal)
- **Selector**: Match backend deployment

### Ingress
- **Host**: `todo.local`
- **Paths**:
  - `/` -> Frontend service
  - `/api/` -> Backend service
  - `/v1/` -> Backend service (API routes)

### ConfigMap: app-config
- **Data**:
  - `NEXT_PUBLIC_API_URL`: Backend service URL
  - `ENVIRONMENT`: Development environment identifier

### Secrets
#### db-credentials
- **Data**:
  - `DATABASE_URL`: Encrypted database connection string

#### api-keys
- **Data**:
  - `OPENAI_API_KEY`: Encrypted OpenAI API key
  - `BETTER_AUTH_SECRET`: Encrypted auth secret

## Docker Images

### Frontend Image (Next.js)
- **Build Context**: frontend/ directory
- **Base Images**:
  - Build stage: `node:20-alpine`
  - Runtime stage: `nginx:alpine`
- **Exposed Port**: 3000
- **Non-root User**: `nginx` user
- **Volume Mounts**: None required

### Backend Image (FastAPI)
- **Build Context**: backend/ directory
- **Base Images**:
  - Build stage: `python:3.13-slim`
  - Runtime stage: `python:3.13-slim`
- **Exposed Port**: 8000
- **Non-root User**: `app` user
- **Volume Mounts**: None required

## Helm Chart Structure

### Chart: todo-app
- **Version**: 1.0.0
- **AppVersion**: Same as application version
- **Dependencies**: None (standalone)

### Value Parameters
- `frontend.image.repository`: Frontend image name
- `frontend.image.tag`: Frontend image tag
- `frontend.replicaCount`: Number of frontend replicas
- `frontend.resources`: Resource requests/limits for frontend
- `backend.image.repository`: Backend image name
- `backend.image.tag`: Backend image tag
- `backend.replicaCount`: Number of backend replicas
- `backend.resources`: Resource requests/limits for backend
- `ingress.hosts`: Hostnames for ingress
- `secrets`: Encrypted secret values
- `config`: Non-sensitive configuration values