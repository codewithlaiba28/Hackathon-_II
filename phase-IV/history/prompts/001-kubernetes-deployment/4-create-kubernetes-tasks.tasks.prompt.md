---
id: 4
title: Create Kubernetes Tasks
stage: tasks
date_iso: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-kubernetes-deployment
branch: 001-kubernetes-deployment
user: user
command: /sp.tasks
labels:
  - kubernetes
  - containerization
  - deployment
  - docker
  - helm
  - tasks
link_spec: specs/001-kubernetes-deployment/spec.md
link_plan: specs/001-kubernetes-deployment/plan.md
link_tasks: specs/001-kubernetes-deployment/tasks.md
link_ticket: null
link_adr: null
link_pr: null
files_yaml:
  - specs/001-kubernetes-deployment/tasks.md
tests_yaml: []
---

# Prompt

```
Break down the plan into atomic tasks:

## Task Group 1: Environment Setup

### Task 1.1: Install and Configure Minikube
**Preconditions:** Docker Desktop installed
**Description:** Set up Minikube cluster with necessary addons
**Steps:**
1. Install Minikube
2. Start Minikube: `minikube start --driver=docker --cpus=4 --memory=8192`
3. Enable addons: `minikube addons enable ingress`
4. Enable addons: `minikube addons enable metrics-server`
5. Verify: `kubectl cluster-info`
**Outputs:** Running Minikube cluster
**Acceptance:** `kubectl get nodes` shows Ready status

### Task 1.2: Install kubectl-ai
**Preconditions:** kubectl installed
**Description:** Install kubectl-ai for AI-assisted operations
**Steps:**
1. Install kubectl-ai plugin
2. Configure OpenAI API key
3. Test: `kubectl-ai "show all pods"`
**Outputs:** Working kubectl-ai installation
**Acceptance:** kubectl-ai responds to queries

### Task 1.3: Install Helm
**Preconditions:** None
**Description:** Install Helm package manager
**Steps:**
1. Install Helm 3.12+
2. Verify: `helm version`
3. Add stable repo (if needed)
**Outputs:** Working Helm installation
**Acceptance:** `helm version` shows 3.12+

### Task 1.4: Enable Docker AI (Gordon)
**Preconditions:** Docker Desktop 4.53+
**Description:** Enable Docker AI agent
**Steps:**
1. Update Docker Desktop to 4.53+
2. Go to Settings → Beta features
3. Toggle on Docker AI
4. Test: `docker ai "what can you do?"`
**Outputs:** Working Docker AI
**Acceptance:** Gordon responds to queries (or skip if unavailable)

---

## Task Group 2: Containerization

### Task 2.1: Create Frontend Dockerfile
**Preconditions:** Phase 3 frontend completed
**Description:** Create optimized multi-stage Dockerfile for Next.js
**Steps:**
1. Create `frontend/Dockerfile`
2. Use multi-stage build (builder + runner)
3. Base: node:20-alpine
4. Install dependencies
5. Build Next.js app
6. Use standalone output
7. Expose port 3000
8. Run as non-root user
**Outputs:** `frontend/Dockerfile`
**Acceptance:** Image builds successfully, < 500MB

### Task 2.2: Create Frontend .dockerignore
**Preconditions:** None
**Description:** Exclude unnecessary files from Docker build
**Steps:**
1. Create `frontend/.dockerignore`
2. Exclude: node_modules, .next, .git, etc.
**Outputs:** `frontend/.dockerignore`
**Acceptance:** Build context is smaller

### Task 2.3: Create Backend Dockerfile
**Preconditions:** Phase 3 backend completed
**Description:** Create optimized Dockerfile for FastAPI
**Steps:**
1. Create `backend/Dockerfile`
2. Base: python:3.13-slim
3. Install dependencies via pip/uv
4. Copy application code
5. Expose port 8000
6. Run as non-root user
7. CMD: uvicorn main:app --host 0.0.0.0 --port 8000
**Outputs:** `backend/Dockerfile`
**Acceptance:** Image builds successfully, < 300MB

### Task 2.4: Create Backend .dockerignore
**Preconditions:** None
**Description:** Exclude unnecessary files from Docker build
**Steps:**
1. Create `backend/.dockerignore`
2. Exclude: __pycache__, .pytest_cache, .venv, etc.
**Outputs:** `backend/.dockerignore`
**Acceptance:** Build context is smaller

### Task 2.5: Build and Test Images Locally
**Preconditions:** Tasks 2.1-2.4 complete
**Description:** Build images and test locally
**Steps:**
1. Set Minikube Docker environment: `eval $(minikube docker-env)`
2. Build frontend: `docker build -t todo-frontend:v1 ./frontend`
3. Build backend: `docker build -t todo-backend:v1 ./backend`
4. Test frontend: `docker run -p 3000:3000 todo-frontend:v1`
5. Test backend: `docker run -p 8000:8000 todo-backend:v1`
**Outputs:** Working Docker images
**Acceptance:** Both services start without errors

---

## Task Group 3: Helm Chart Creation

### Task 3.1: Initialize Helm Chart Structure
**Preconditions:** Helm installed
**Description:** Create Helm chart skeleton
**Steps:**
1. Create directory: `mkdir -p helm-charts`
2. Run: `helm create helm-charts/todo-app`
3. Remove default templates (we'll create custom ones)
**Outputs:** `helm-charts/todo-app/` structure
**Acceptance:** Directory structure exists

### Task 3.2: Create Chart.yaml
**Preconditions:** Task 3.1 complete
**Description:** Define chart metadata
**Steps:**
1. Edit `helm-charts/todo-app/Chart.yaml`
2. Set name: todo-app
3. Set version: 1.0.0
4. Set appVersion: 4.0.0 (Phase 4)
5. Add description
**Outputs:** `helm-charts/todo-app/Chart.yaml`
**Acceptance:** Valid Chart.yaml

### Task 3.3: Create values.yaml
**Preconditions:** None
**Description:** Define default configuration values
**Steps:**
1. Create `helm-charts/todo-app/values.yaml`
2. Define frontend config (image, replicas, resources, env)
3. Define backend config (image, replicas, resources, env)
4. Define ingress config (host, paths)
5. Define secrets (placeholder values)
**Outputs:** `helm-charts/todo-app/values.yaml`
**Acceptance:** All required values defined

### Task 3.4: Create Frontend Deployment Template
**Preconditions:** values.yaml defined
**Description:** Create Kubernetes Deployment for frontend
**Steps:**
1. Create `helm-charts/todo-app/templates/frontend/deployment.yaml`
2. Template metadata (name, labels)
3. Template spec (replicas, selector, template)
4. Define containers (image, ports, env, resources)
5. Add livenessProbe and readinessProbe
6. Use values from values.yaml
**Outputs:** Frontend Deployment template
**Acceptance:** Template renders with `helm template`

### Task 3.5: Create Frontend Service Template
**Preconditions:** None
**Description:** Create Kubernetes Service for frontend
**Steps:**
1. Create `helm-charts/todo-app/templates/frontend/service.yaml`
2. Type: ClusterIP
3. Port: 3000
4. Selector: matches frontend deployment
**Outputs:** Frontend Service template
**Acceptance:** Template renders correctly

### Task 3.6: Create Frontend ConfigMap Template
**Preconditions:** None
**Description:** Create ConfigMap for frontend environment
**Steps:**
1. Create `helm-charts/todo-app/templates/frontend/configmap.yaml`
2. Include NEXT_PUBLIC_API_URL
3. Include other non-sensitive config
**Outputs:** Frontend ConfigMap template
**Acceptance:** Template renders correctly

### Task 3.7: Create Backend Deployment Template
**Preconditions:** values.yaml defined
**Description:** Create Kubernetes Deployment for backend
**Steps:**
1. Create `helm-charts/todo-app/templates/backend/deployment.yaml`
2. Template metadata (name, labels)
3. Template spec (replicas, selector, template)
4. Define containers (image, ports, env, resources)
5. Add livenessProbe (GET /health) and readinessProbe
6. Mount secrets for DATABASE_URL and OPENAI_API_KEY
7. Use values from values.yaml
**Outputs:** Backend Deployment template
**Acceptance:** Template renders with `helm template`

### Task 3.8: Create Backend Service Template
**Preconditions:** None
**Description:** Create Kubernetes Service for backend
**Steps:**
1. Create `helm-charts/todo-app/templates/backend/service.yaml`
2. Type: ClusterIP
3. Port: 8000
4. Selector: matches backend deployment
**Outputs:** Backend Service template
**Acceptance:** Template renders correctly

### Task 3.9: Create Backend Secret Template
**Preconditions:** None
**Description:** Create Secret for sensitive backend config
**Steps:**
1. Create `helm-charts/todo-app/templates/backend/secret.yaml`
2. Include DATABASE_URL (base64 encoded)
3. Include OPENAI_API_KEY (base64 encoded)
4. Use values from values.yaml
**Outputs:** Backend Secret template
**Acceptance:** Template renders correctly

### Task 3.10: Create Ingress Template
**Preconditions:** nginx-ingress addon enabled
**Description:** Create Ingress for external access
**Steps:**
1. Create `helm-charts/todo-app/templates/ingress.yaml`
2. Host: todo.local
3. Paths:
   - / → frontend service
   - /api → backend service
4. Use values from values.yaml
**Outputs:** Ingress template
**Acceptance:** Template renders correctly

### Task 3.11: Validate Helm Chart
**Preconditions:** All templates created
**Description:** Lint and validate Helm chart
**Steps:**
1. Run: `helm lint helm-charts/todo-app`
2. Run: `helm template helm-charts/todo-app`
3. Fix any errors
**Outputs:** Valid Helm chart
**Acceptance:** No lint errors, templates render

---

## Task Group 4: Deployment Scripts

### Task 4.1: Create Minikube Setup Script
**Preconditions:** None
**Description:** Automate Minikube cluster setup
**Steps:**
1. Create `scripts/minikube-setup.sh`
2. Start Minikube with correct settings
3. Enable ingress addon
4. Enable metrics-server addon
5. Add /etc/hosts entry for todo.local
**Outputs:** `scripts/minikube-setup.sh`
**Acceptance:** Script runs without errors

### Task 4.2: Create Image Build Script
**Preconditions:** Dockerfiles created
**Description:** Automate Docker image building
**Steps:**
1. Create `scripts/build-images.sh`
2. Set Minikube Docker environment
3. Build frontend image
4. Build backend image
5. Tag images with version
6. Optional: Push to Docker Hub
**Outputs:** `scripts/build-images.sh`
**Acceptance:** Images build successfully

### Task 4.3: Create Deployment Script
**Preconditions:** Helm chart created
**Description:** Automate Helm deployment
**Steps:**
1. Create `scripts/deploy.sh`
2. Create namespace if not exists
3. Install/upgrade Helm release
4. Use values-dev.yaml for development
5. Wait for rollout to complete
6. Display access instructions
**Outputs:** `scripts/deploy.sh`
**Acceptance:** Deployment succeeds

### Task 4.4: Create Cleanup Script
**Preconditions:** None
**Description:** Automate resource cleanup
**Steps:**
1. Create `scripts/cleanup.sh`
2. Uninstall Helm release
3. Delete namespace
4. Optionally stop Minikube
**Outputs:** `scripts/cleanup.sh`
**Acceptance:** Cleanup succeeds

---

## Task Group 5: Deployment and Testing

### Task 5.1: Deploy to Minikube
**Preconditions:** All previous tasks complete
**Description:** Deploy application to Minikube
**Steps:**
1. Run: `scripts/minikube-setup.sh`
2. Run: `scripts/build-images.sh`
3. Run: `scripts/deploy.sh`
4. Wait for pods to be Ready
5. Check pod status: `kubectl get pods -n todo-app`
**Outputs:** Running application in Minikube
**Acceptance:** All pods in Running state

### Task 5.2: Verify Services
**Preconditions:** Deployment complete
**Description:** Test that services are accessible
**Steps:**
1. Port-forward frontend: `kubectl port-forward svc/frontend 3000:3000 -n todo-app`
2. Access http://localhost:3000 in browser
3. Port-forward backend: `kubectl port-forward svc/backend 8000:8000 -n todo-app`
4. Test API: `curl http://localhost:8000/health`
5. Access via Ingress: http://todo.local (if /etc/hosts configured)
**Outputs:** Working services
**Acceptance:** All services respond correctly

### Task 5.3: End-to-End Test
**Preconditions:** Services verified
**Description:** Test complete user workflow
**Steps:**
1. Open chatbot UI
2. Create a todo via natural language
3. List todos
4. Complete a todo
5. Delete a todo
6. Verify database persistence
**Outputs:** Working end-to-end flow
**Acceptance:** All CRUD operations work

### Task 5.4: Test with kubectl-ai
**Preconditions:** kubectl-ai installed
**Description:** Use AI-assisted operations
**Steps:**
1. Query pods: `kubectl-ai "show all pods in todo-app namespace"`
2. Check logs: `kubectl-ai "show logs of backend pod"`
3. Describe resources: `kubectl-ai "describe the frontend deployment"`
4. Troubleshoot: `kubectl-ai "why is pod X failing?"`
**Outputs:** kubectl-ai usage examples
**Acceptance:** AI responds correctly

### Task 5.5: Test with Gordon (Docker AI)
**Preconditions:** Gordon enabled
**Description:** Use Docker AI for operations
**Steps:**
1. Inspect images: `docker ai "show me the layers of todo-frontend:v1"`
2. Troubleshoot: `docker ai "why did this image build fail?"`
3. Optimize: `docker ai "how can I make this image smaller?"`
**Outputs:** Gordon usage examples
**Acceptance:** AI responds correctly (or documented as unavailable)

---

## Task Group 6: Documentation

### Task 6.1: Create Deployment Guide
**Preconditions:** Deployment successful
**Description:** Document deployment process
**Steps:**
1. Create `docs/phase4/DEPLOYMENT.md`
2. Include prerequisites
3. Step-by-step deployment instructions
4. Configuration options
5. Access instructions
**Outputs:** `docs/phase4/DEPLOYMENT.md`
**Acceptance:** Clear, complete guide

### Task 6.2: Create Troubleshooting Guide
**Preconditions:** Testing complete
**Description:** Document common issues and solutions
**Steps:**
1. Create `docs/phase4/TROUBLESHOOTING.md`
2. List common issues (pods not starting, image pull errors, etc.)
3. Provide solutions
4. Include debugging commands
**Outputs:** `docs/phase4/TROUBLESHOOTING.md`
**Acceptance:** Covers common scenarios

### Task 6.3: Create kubectl-ai Usage Guide
**Preconditions:** kubectl-ai tested
**Description:** Document AI-assisted operations
**Steps:**
1. Create `docs/phase4/KUBECTL-AI-GUIDE.md`
2. Include installation
3. Common queries
4. Examples for this project
5. Best practices
**Outputs:** `docs/phase4/KUBECTL-AI-GUIDE.md`
**Acceptance:** Useful examples

### Task 6.4: Update Main README
**Preconditions:** All documentation created
**Description:** Update project README with Phase 4 info
**Steps:**
1. Edit `README.md`
2. Add Phase 4 section
3. Link to deployment docs
4. Update architecture diagram
5. Add Phase 4 to table of contents
**Outputs:** Updated `README.md`
**Acceptance:** README reflects Phase 4

---

## Task Dependencies Graph
```
1.1 (Minikube) → 4.1 (Setup Script)
1.2 (kubectl-ai) → 5.4 (kubectl-ai Test)
1.3 (Helm) → 3.1 (Chart Init)
1.4 (Gordon) → 5.5 (Gordon Test)

2.1-2.4 (Dockerfiles) → 2.5 (Build Test) → 4.2 (Build Script)

3.1-3.11 (Helm) → 4.3 (Deploy Script)

4.1-4.4 (Scripts) → 5.1 (Deploy)

5.1 (Deploy) → 5.2 (Verify) → 5.3 (E2E Test)
5.3 → 5.4 (kubectl-ai)
5.3 → 5.5 (Gordon)

5.1-5.5 (All Testing) → 6.1-6.4 (Documentation)
```
## Estimated Timeline
- Setup (Group 1): 2-3 hours
- Containerization (Group 2): 3-4 hours
- Helm Charts (Group 3): 5-6 hours
- Scripts (Group 4): 2-3 hours
- Deployment & Testing (Group 5): 3-4 hours
- Documentation (Group 6): 2-3 hours
**Total: 17-23 hours**
```

# Response

Generated the implementation tasks for Phase 4 - Local Kubernetes Deployment in the file `specs/001-kubernetes-deployment/tasks.md`. The tasks are organized by user story in priority order:

1. Phase 1: Setup Tasks (environment initialization)
2. Phase 2: Foundational Tasks (shared infrastructure)
3. Phase 3: [US-1] Containerize Applications (P1 priority)
4. Phase 4: [US-2] Helm Chart Creation (P1 priority)
5. Phase 5: [US-3] Minikube Deployment (P1 priority)
6. Phase 6: [US-4] AI-Assisted Operations (P3 priority)
7. Phase 7: Polish & Cross-Cutting Concerns

The tasks follow the required checklist format with sequential IDs (T001, T002, etc.), parallelizability markers [P], and user story labels [US1], [US2], etc. Each task includes a clear description with file paths where applicable.

Key features of the task breakdown:
- Total of 66 tasks across all phases
- Critical path identified: Setup → Containerization → Helm → Deployment → AI Operations
- Parallel execution opportunities marked with [P] where applicable
- Tasks organized by user story to enable independent implementation and testing
- Dependencies clearly outlined between user stories
- Each user story has independent test criteria as specified in the feature specification

The tasks are immediately executable with sufficient specificity for an LLM to complete them without additional context.