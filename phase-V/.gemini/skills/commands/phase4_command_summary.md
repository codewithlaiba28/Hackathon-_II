# Phase IV: Local Kubernetes Deployment - Command Summary

This document contains all the commands needed for Phase IV of the hackathon: Local Kubernetes Deployment.

## Table of Contents
1. [Environment Setup](#environment-setup)
2. [Containerization](#containerization)
3. [Helm Chart Creation](#helm-chart-creation)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Validation and Testing](#validation-and-testing)
6. [Cleanup](#cleanup)
7. [Skills Integration](#skills-integration)

## Environment Setup

### Minikube Setup
```bash
# Install and start Minikube
minikube start --driver=docker --cpus=4 --memory=8192

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server

# Set Docker environment to Minikube
eval $(minikube docker-env)

# Verify cluster
kubectl cluster-info
kubectl get nodes
```

### Helm Setup
```bash
# Install Helm (if not already installed)
# Verify Helm installation
helm version

# Create necessary directories
mkdir -p helm-charts/todo-app/templates/{frontend,backend}
mkdir -p scripts
mkdir -p docs/phase4
```

## Containerization

### Create Dockerfiles
```bash
# Create frontend Dockerfile
cat > frontend/Dockerfile << 'EOF'
# Multi-stage build for Next.js frontend
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json yarn.lock* ./
RUN yarn install --frozen-lockfile

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN yarn build

FROM node:20-alpine AS runner
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Set production environment
ENV NODE_ENV=production

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json

USER nextjs

EXPOSE 3000

CMD ["node", "server.js"]
EOF

# Create backend Dockerfile
cat > backend/Dockerfile << 'EOF'
# Multi-stage build for FastAPI backend
FROM python:3.13-slim AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

FROM python-base AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python-base AS final
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Create Docker ignore files
cat > frontend/.dockerignore << 'EOF'
node_modules
npm-debug.log
.next
.git
README.md
.nyc_output
coverage
.env.local
.env.development.local
.env.test.local
.env.production.local
.eslintcache
.yarn/cache
.yarn/unplugged
.yarn/build-state.yml
.yarn/install-state.gz
EOF

cat > backend/.dockerignore << 'EOF'
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
.venv/
.ENV
.venv.bak
env.bak
*.swp
*.swo
*~
__pycache__/
.pytest_cache/
.coverage
htmlcov/
.pyup.yml
.DS_Store
.git
.gitignore
README.md
.env
EOF
```

### Build Docker Images
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

# Verify images
docker images | grep todo
```

## Helm Chart Creation

### Initialize Helm Chart
```bash
# Create Helm chart structure
cat > helm-charts/todo-app/Chart.yaml << 'EOF'
apiVersion: v2
name: todo-app
description: A Helm chart for the Todo application
type: application
version: 1.0.0
appVersion: "4.0.0"
EOF

cat > helm-charts/todo-app/values.yaml << 'EOF'
# Default values for todo-app
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

global:
  imageRegistry: ""
  imagePullSecrets: []
  storageClass: ""

# Frontend configuration
frontend:
  replicaCount: 2
  image:
    repository: localhost:5000/todo-frontend
    pullPolicy: IfNotPresent
    tag: "v1.0"
  service:
    type: ClusterIP
    port: 3000
  ingress:
    enabled: true
    className: ""
    annotations: {}
    hosts:
      - host: todo.local
        paths:
          - path: /
            pathType: Prefix
    tls: []
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 128Mi
  autoscaling:
    enabled: false
    minReplicas: 1
    maxReplicas: 100
    targetCPUUtilizationPercentage: 80
  nodeSelector: {}
  tolerations: []
  affinity: {}

# Backend configuration
backend:
  replicaCount: 2
  image:
    repository: localhost:5000/todo-backend
    pullPolicy: IfNotPresent
    tag: "v1.0"
  service:
    type: ClusterIP
    port: 8000
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 128Mi
  env:
    DATABASE_URL: ""
    OPENAI_API_KEY: ""
    JWT_SECRET: ""
  autoscaling:
    enabled: false
    minReplicas: 1
    maxReplicas: 100
    targetCPUUtilizationPercentage: 80
  nodeSelector: {}
  tolerations: []
  affinity: {}

# Database configuration
database:
  host: ""
  port: 5432
  username: ""
  name: ""
  sslRequired: false
EOF
```

### Create Helm Templates
```bash
# Create frontend templates
cat > helm-charts/todo-app/templates/frontend/deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-app.fullname" . }}-frontend
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
    app: frontend
spec:
  {{- if not .Values.frontend.autoscaling.enabled }}
  replicas: {{ .Values.frontend.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "todo-app.selectorLabels" . | nindent 6 }}
      app: frontend
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "todo-app.selectorLabels" . | nindent 8 }}
        app: frontend
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}-frontend
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.frontend.image.repository }}:{{ .Values.frontend.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.frontend.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 3000
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
          resources:
            {{- toYaml .Values.frontend.resources | nindent 12 }}
          env:
            - name: NEXT_PUBLIC_API_URL
              value: "http://todo.local/api"
      {{- with .Values.frontend.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.frontend.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.frontend.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
EOF

cat > helm-charts/todo-app/templates/frontend/service.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-app.fullend" . }}-frontend
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
spec:
  type: {{ .Values.frontend.service.type }}
  ports:
    - port: {{ .Values.frontend.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "todo-app.selectorLabels" . | nindent 4 }}
    app: frontend
EOF

cat > helm-charts/todo-app/templates/backend/deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-app.fullname" . }}-backend
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
    app: backend
spec:
  {{- if not .Values.backend.autoscaling.enabled }}
  replicas: {{ .Values.backend.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "todo-app.selectorLabels" . | nindent 6 }}
      app: backend
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "todo-app.selectorLabels" . | nindent 8 }}
        app: backend
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}-backend
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 8000
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health
              port: http
          readinessProbe:
            httpGet:
              path: /health
              port: http
          resources:
            {{- toYaml .Values.backend.resources | nindent 12 }}
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ include "todo-app.fullname" . }}-backend-secret
                  key: database-url
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: {{ include "todo-app.fullname" . }}-backend-secret
                  key: openai-api-key
            - name: JWT_SECRET
              valueFrom:
                secretKeyRef:
                  name: {{ include "todo-app.fullname" . }}-backend-secret
                  key: jwt-secret
      {{- with .Values.backend.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.backend.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.backend.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
EOF

cat > helm-charts/todo-app/templates/backend/service.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-app.fullname" . }}-backend
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
spec:
  type: {{ .Values.backend.service.type }}
  ports:
    - port: {{ .Values.backend.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "todo-app.selectorLabels" . | nindent 4 }}
    app: backend
EOF

cat > helm-charts/todo-app/templates/backend/secret.yaml << 'EOF'
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "todo-app.fullname" . }}-backend-secret
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
type: Opaque
data:
  database-url: {{ .Values.database.host | b64enc | quote }}
  openai-api-key: {{ .Values.backend.env.OPENAI_API_KEY | b64enc | quote }}
  jwt-secret: {{ .Values.backend.env.JWT_SECRET | b64enc | quote }}
EOF

cat > helm-charts/todo-app/templates/ingress.yaml << 'EOF'
{{- if .Values.frontend.ingress.enabled -}}
{{- $fullName := include "todo-app.fullname" . -}}
{{- $svcPort := .Values.frontend.service.port -}}
{{- if and .Values.frontend.ingress.className (not (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion)) }}
  {{- if not (hasKey .Values.frontend.ingress.annotations "kubernetes.io/ingress.class") }}
  {{- $_ := set .Values.frontend.ingress.annotations "kubernetes.io/ingress.class" .Values.frontend.ingress.className}}
  {{- end }}
{{- end }}
{{- if semverCompare ">=1.19-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1
{{- else if semverCompare ">=1.14-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1beta1
{{- else -}}
apiVersion: extensions/v1beta1
{{- end }}
kind: Ingress
metadata:
  name: {{ $fullName }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
  {{- with .Values.frontend.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if and .Values.frontend.ingress.className (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion) }}
  ingressClassName: {{ .Values.frontend.ingress.className }}
  {{- end }}
  {{- if .Values.frontend.ingress.tls }}
  tls:
    {{- range .Values.frontend.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.frontend.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            {{- if and .pathType (semverCompare ">=1.18-0" $.Capabilities.KubeVersion.GitVersion) }}
            pathType: {{ .pathType }}
            {{- end }}
            backend:
              {{- if semverCompare ">=1.19-0" $.Capabilities.KubeVersion.GitVersion }}
              service:
                name: {{ $fullName }}-frontend
                port:
                  number: {{ $svcPort }}
              {{- else }}
              serviceName: {{ $fullName }}-frontend
              servicePort: {{ $svcPort }}
              {{- end }}
          {{- end }}
    {{- end }}
{{- end }}
EOF

cat > helm-charts/todo-app/templates/_helpers.tpl << 'EOF'
{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "todo-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.chart" . }}
{{ include "todo-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "todo-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "todo-app.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
EOF
```

### Validate Helm Chart
```bash
# Lint the chart
helm lint helm-charts/todo-app

# Template the chart (dry run)
helm template todo-app helm-charts/todo-app

# Package the chart (optional)
helm package helm-charts/todo-app
```

## Kubernetes Deployment

### Deploy Application
```bash
# Create namespace
kubectl create namespace todo-app

# Install the Helm release
helm upgrade --install todo-app helm-charts/todo-app --namespace todo-app --create-namespace

# Check deployment status
helm status todo-app -n todo-app

# Verify pods are running
kubectl get pods -n todo-app

# Verify services are created
kubectl get services -n todo-app

# Verify ingress is created
kubectl get ingress -n todo-app
```

### Update /etc/hosts for local testing
```bash
# Add entry to hosts file to resolve todo.local to Minikube IP
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts
```

## Validation and Testing

### Check Application Status
```bash
# Check all resources
kubectl get all -n todo-app

# Check pod logs
kubectl logs -l app=frontend -n todo-app
kubectl logs -l app=backend -n todo-app

# Describe pods for detailed information
kubectl describe pods -l app=frontend -n todo-app
kubectl describe pods -l app=backend -n todo-app

# Test service connectivity
kubectl port-forward svc/todo-app-backend 8000:8000 -n todo-app &
kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app &
```

### End-to-End Testing
```bash
# Test backend health endpoint
curl http://localhost:8000/health

# Access frontend via browser
# Open http://todo.local in browser
# Or access via port-forward: http://localhost:3000
```

## Cleanup

### Uninstall Application
```bash
# Uninstall Helm release
helm uninstall todo-app -n todo-app

# Delete namespace
kubectl delete namespace todo-app

# Stop Minikube
minikube stop

# Remove Docker images (optional)
docker rmi -f $(docker images --filter=reference='*todo*' -q)
```

## Skills Integration

### Using Available Skills for Phase IV

#### Docker Expert Skill
```bash
# Use when creating or optimizing Dockerfiles
Use the docker-expert skill for:
- Multi-stage build optimization
- Image size reduction techniques
- Security best practices in containers
- Networking configuration
- Volume mounting strategies
```

#### Kubernetes Specialist Skill
```bash
# Use when deploying or managing Kubernetes workloads
Use the kubernetes-specialist skill for:
- Cluster configuration and security hardening
- Resource optimization and performance tuning
- Network policies and service mesh setup
- Storage configuration and PV/PVC management
- RBAC policies and access control
```

#### Helm Chart Scaffolding Skill
```bash
# Use when creating or managing Helm charts
Use the helm-chart-scaffolding skill for:
- Chart structure and organization
- Template creation and best practices
- Values management and validation
- Chart packaging and distribution
- Versioning and release management
```

#### DevOps Engineer Skill
```bash
# Use when setting up CI/CD or infrastructure
Use the devops-engineer skill for:
- Infrastructure as code implementation
- CI/CD pipeline setup
- Cloud platform integration
- GitOps workflows
- Container registry management
- Monitoring and logging setup
```

## Automation Scripts

### Create Deployment Script
```bash
cat > scripts/deploy.sh << 'EOF'
#!/bin/bash

# Script to deploy the Todo application to Minikube

set -e

echo "Starting deployment to Minikube..."

# Set Docker environment to Minikube
eval $(minikube docker-env)

echo "Building Docker images..."
docker build -t todo-frontend:v1.0 ./frontend
docker build -t todo-backend:v1.0 ./backend

echo "Tagging images for local registry..."
docker tag todo-frontend:v1.0 localhost:5000/todo-frontend:v1.0
docker tag todo-backend:v1.0 localhost:5000/todo-backend:v1.0

echo "Pushing images to local registry..."
docker push localhost:5000/todo-frontend:v1.0
docker push localhost:5000/todo-backend:v1.0

echo "Creating namespace..."
kubectl create namespace todo-app || true

echo "Installing/upgrading Helm release..."
helm upgrade --install todo-app helm-charts/todo-app --namespace todo-app --create-namespace --wait --timeout=10m

echo "Deployment completed successfully!"
echo "Access the application at http://todo.local (make sure you've added it to /etc/hosts)"
EOF

chmod +x scripts/deploy.sh
```

### Create Cleanup Script
```bash
cat > scripts/cleanup.sh << 'EOF'
#!/bin/bash

# Script to clean up the Todo application from Minikube

set -e

echo "Cleaning up deployment..."

# Uninstall Helm release
helm uninstall todo-app -n todo-app || true

# Delete namespace
kubectl delete namespace todo-app || true

echo "Cleanup completed!"
EOF

chmod +x scripts/cleanup.sh
```