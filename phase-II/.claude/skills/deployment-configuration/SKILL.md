---
name: deployment-configuration
description: |
  This skill creates comprehensive deployment configurations for containerized applications using Docker, Docker Compose, and Kubernetes. Use this skill when you need to implement containerized deployment solutions for your applications.
---

# Deployment Configuration Skill

This skill should be used when users need to create comprehensive deployment configurations for containerized applications using Docker, Docker Compose, and Kubernetes.

## Skill Type: Builder

## Domain: Containerized Application Deployment

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Application structure, dependencies, environment variables, ports, volumes |
| **Conversation** | User's specific deployment requirements, target platform, scaling needs |
| **Skill References** | Docker, Docker Compose, Kubernetes best practices, security patterns |
| **User Guidelines** | Infrastructure constraints, security policies, compliance requirements |

Ensure all required context is gathered before implementing.

## Core Concepts

Containerized deployment involves:
- Containerizing applications with proper isolation
- Managing environment-specific configurations
- Orchestrating multi-container applications
- Scaling applications horizontally
- Implementing health checks and monitoring
- Managing secrets and sensitive data

## Deployment Architecture

The deployment follows these patterns:
1. Containerization of applications
2. Multi-stage builds for optimization
3. Service orchestration with Docker Compose
4. Kubernetes deployment for production
5. Persistent storage configuration
6. Network configuration and security

## Implementation Steps

### 1. Create Dockerfile for Backend Application

Create a Dockerfile for the FastAPI backend:

```dockerfile
# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create Dockerfile for Frontend Application

Create a Dockerfile for the Next.js frontend:

```dockerfile
# frontend/Dockerfile
# Multi-stage build for optimization
FROM node:18-alpine AS deps
WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS builder
WORKDIR /app

# Copy package files and source code
COPY package*.json ./
COPY tsconfig.json ./
COPY . .

# Install all dependencies and build
RUN npm ci
RUN npm run build

FROM node:18-alpine AS runtime
WORKDIR /app

# Copy production dependencies
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/node_modules/.prune ./node_modules

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/next.config.ts ./
COPY --from=builder /app/package*.json ./

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

USER nextjs

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

CMD ["npm", "start"]
```

### 3. Create Docker Compose Configuration

Create a Docker Compose file for local development:

```yaml
# docker-compose.yml
version: '3.8'

services:
  # PostgreSQL database
  db:
    image: postgres:13-alpine
    container_name: todo-app-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: todo_app
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend API service
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: todo-app-backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/todo_app
      - JWT_SECRET=${JWT_SECRET:-change-this-in-production}
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./backend:/app
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend service
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: todo-app-frontend
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - NEXT_PUBLIC_APP_NAME=Todo App
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
```

### 4. Create Production Docker Compose

Create a Docker Compose file for production:

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # PostgreSQL database
  db:
    image: postgres:13-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend API service
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${DB_PASSWORD}@db:5432/${POSTGRES_DB}
      - JWT_SECRET_FILE=/run/secrets/jwt_secret
      - ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES:-30}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    secrets:
      - jwt_secret
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend service
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    environment:
      - NEXT_PUBLIC_API_URL=${FRONTEND_API_URL}
      - NEXT_PUBLIC_APP_NAME=${APP_NAME}
    depends_on:
      - backend
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Nginx reverse proxy
  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/conf.d:/etc/nginx/conf.d
      - certbot_certs:/etc/letsencrypt
      - certbot_data:/var/lib/letsencrypt
    depends_on:
      - frontend
      - backend
    networks:
      - app-network

volumes:
  postgres_data:
  certbot_certs:
  certbot_data:

networks:
  app-network:
    driver: bridge

secrets:
  db_password:
    file: ./secrets/db_password.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt
```

### 5. Create Kubernetes Manifests

Create Kubernetes deployment manifests:

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app
```

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-app-secrets
  namespace: todo-app
type: Opaque
data:
  db-password: <base64-encoded-password>
  jwt-secret: <base64-encoded-jwt-secret>
```

```yaml
# k8s/postgres-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: todo-app
  labels:
    app: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:13-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: "todo_app"
        - name: POSTGRES_USER
          value: "postgres"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: db-password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        livenessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: todo-app
spec:
  selector:
    app: postgres
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
  type: ClusterIP
```

```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: todo-app
  labels:
    app: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: ghcr.io/your-org/todo-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          value: "postgresql://postgres:$(DB_PASSWORD)@postgres-service:5432/todo_app"
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: jwt-secret
        - name: ACCESS_TOKEN_EXPIRE_MINUTES
          value: "30"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"

---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: todo-app
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
```

```yaml
# k8s/frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: todo-app
  labels:
    app: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: ghcr.io/your-org/todo-frontend:latest
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "http://backend-service"
        - name: NEXT_PUBLIC_APP_NAME
          value: "Todo App"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "256Mi"
            cpu: "200m"

---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: todo-app
spec:
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: ClusterIP
```

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-app-ingress
  namespace: todo-app
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  tls:
  - hosts:
    - your-app-domain.com
    secretName: todo-app-tls
  rules:
  - host: your-app-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 80
```

### 6. Create Production Dockerfiles

Create optimized Dockerfiles for production:

```dockerfile
# backend/Dockerfile.prod
FROM python:3.10-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gunicorn && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM base as production

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

EXPOSE 8000

CMD ["gunicorn", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker",
     "--bind", "0.0.0.0:8000", "--timeout", "120", "main:app"]
```

```dockerfile
# frontend/Dockerfile.prod
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy source code and build
COPY . .
RUN npm run build

FROM node:18-alpine AS runtime

WORKDIR /app

# Copy production dependencies
COPY --from=builder /app/node_modules ./node_modules

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/next.config.ts ./
COPY --from=builder /app/package*.json ./

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

USER nextjs

EXPOSE 3000

CMD ["node_modules/.bin/next", "start"]
```

### 7. Create Nginx Configuration

Create Nginx configuration for production:

```nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    server {
        listen 80;
        server_name _;

        # Serve frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Proxy API requests to backend
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check endpoint
        location /api/health {
            proxy_pass http://backend/api/health;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### 8. Create Environment Configuration

Create environment configuration files:

```bash
# .env.production
POSTGRES_DB=todo_app_prod
POSTGRES_USER=todo_user
ACCESS_TOKEN_EXPIRE_MINUTES=43200  # 30 days
JWT_SECRET=your-super-secure-production-jwt-secret
FRONTEND_API_URL=https://your-app-domain.com/api
APP_NAME=Todo App Production
LOG_LEVEL=INFO
```

```bash
# .env.staging
POSTGRES_DB=todo_app_staging
POSTGRES_USER=todo_user
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
JWT_SECRET=your-less-secure-staging-jwt-secret
FRONTEND_API_URL=https://staging.your-app-domain.com/api
APP_NAME=Todo App Staging
LOG_LEVEL=DEBUG
```

### 9. Create Deployment Scripts

Create scripts to manage deployments:

```bash
#!/bin/bash
# scripts/deploy.sh

set -e

ENVIRONMENT=${1:-production}

echo "Deploying to $ENVIRONMENT environment..."

case $ENVIRONMENT in
  "production")
    docker compose -f docker-compose.prod.yml up -d --build
    ;;
  "staging")
    docker compose -f docker-compose.staging.yml up -d --build
    ;;
  *)
    echo "Usage: $0 [production|staging]"
    exit 1
    ;;
esac

echo "Deployment completed!"
```

```bash
#!/bin/bash
# scripts/k8s-deploy.sh

set -e

NAMESPACE=${1:-todo-app}
ENVIRONMENT=${2:-production}

echo "Deploying to Kubernetes namespace: $NAMESPACE, environment: $ENVIRONMENT"

kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Apply secrets (you'll need to create these separately)
kubectl apply -f k8s/secrets.yaml -n $NAMESPACE

# Apply all other manifests
kubectl apply -f k8s/postgres-deployment.yaml -n $NAMESPACE
kubectl apply -f k8s/backend-deployment.yaml -n $NAMESPACE
kubectl apply -f k8s/frontend-deployment.yaml -n $NAMESPACE
kubectl apply -f k8s/ingress.yaml -n $NAMESPACE

echo "Kubernetes deployment completed!"
```

## Best Practices

1. **Use multi-stage builds** to reduce image sizes
2. **Run containers as non-root users** for security
3. **Implement health checks** for proper container management
4. **Use secrets management** for sensitive data
5. **Configure resource limits** to prevent resource exhaustion
6. **Use persistent volumes** for stateful data
7. **Implement proper logging** and monitoring
8. **Use environment-specific configurations** for different environments

## Deployment Checklist

- [ ] Dockerfiles created for all services
- [ ] Docker Compose configuration created
- [ ] Kubernetes manifests created
- [ ] Secrets management implemented
- [ ] Health checks configured
- [ ] Resource limits set
- [ ] Persistent storage configured
- [ ] Network configuration complete
- [ ] SSL/TLS termination configured
- [ ] Monitoring and logging implemented

## Running Deployments

```bash
# Local development
docker-compose up --build

# Production deployment with Docker Compose
docker-compose -f docker-compose.prod.yml up -d --build

# Kubernetes deployment
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n todo-app
kubectl get services -n todo-app
```

This skill provides a comprehensive approach to deployment configuration for containerized applications, ensuring secure, scalable, and maintainable deployments across different environments.