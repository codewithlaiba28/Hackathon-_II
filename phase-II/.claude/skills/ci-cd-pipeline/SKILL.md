---
name: ci-cd-pipeline
description: |
  This skill creates comprehensive CI/CD pipelines for full-stack applications with FastAPI backend and Next.js frontend using GitHub Actions. Use this skill when you need to implement automated testing, building, and deployment workflows for your application.
---

# CI/CD Pipeline Skill

This skill should be used when users need to create comprehensive CI/CD pipelines for full-stack applications with FastAPI backend and Next.js frontend using GitHub Actions.

## Skill Type: Automation

## Domain: CI/CD Pipeline Configuration with GitHub Actions

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Current project structure, dependencies, deployment targets, existing CI/CD setup |
| **Conversation** | User's specific deployment requirements, hosting platforms, security constraints |
| **Skill References** | GitHub Actions documentation, Docker best practices, deployment strategies |
| **User Guidelines** | Project-specific deployment conventions, security policies, environment requirements |

Ensure all required context is gathered before implementing.

## Core Concepts

CI/CD pipelines involve:
- Automated testing of code changes
- Building and packaging applications
- Security scanning and quality checks
- Deployment to various environments
- Rollback capabilities
- Monitoring and notifications

## Pipeline Architecture

The CI/CD pipeline follows these stages:
1. Code validation and security scanning
2. Backend testing and building
3. Frontend testing and building
4. Integration testing
5. Deployment to staging/production
6. Post-deployment validation

## Implementation Steps

### 1. Setup GitHub Actions Workflow Directory

Create the GitHub Actions workflows directory:

```bash
# Create the workflows directory if it doesn't exist
mkdir -p .github/workflows
```

### 2. Create Code Validation Workflow

Create a workflow for code validation and security scanning:

```yaml
# .github/workflows/code-validation.yml
name: Code Validation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  lint-and-validate:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18.x]
        python-version: [3.9, 3.10, 3.11]

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Set up Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json

    - name: Install Python dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest black flake8 mypy

    - name: Install Node.js dependencies
      run: |
        cd frontend
        npm ci

    - name: Run Python linting
      run: |
        cd backend
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        black --check .

    - name: Run Python type checking
      run: |
        cd backend
        mypy .

    - name: Run Node.js linting
      run: |
        cd frontend
        npm run lint

    - name: Run Node.js type checking
      run: |
        cd frontend
        npx tsc --noEmit
```

### 3. Create Backend Testing Workflow

Create a workflow for backend testing:

```yaml
# .github/workflows/backend-tests.yml
name: Backend Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run backend tests
      run: |
        cd backend
        python -m pytest tests/ -v --cov=backend --cov-report=xml
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        JWT_SECRET: test-secret-key-for-ci

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml
        flags: backend
        name: backend
```

### 4. Create Frontend Testing Workflow

Create a workflow for frontend testing:

```yaml
# .github/workflows/frontend-tests.yml
name: Frontend Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x]

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json

    - name: Install dependencies
      run: |
        cd frontend
        npm ci

    - name: Run unit tests
      run: |
        cd frontend
        npm test -- --coverage --ci --reporters=default --reporters=jest-junit

    - name: Run build
      run: |
        cd frontend
        npm run build
      env:
        NEXT_PUBLIC_API_URL: http://localhost:8000

    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: frontend-test-results
        path: frontend/jest-junit.xml
```

### 5. Create Integration Testing Workflow

Create a workflow for integration testing:

```yaml
# .github/workflows/integration-tests.yml
name: Integration Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  integration-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10]
        node-version: [18.x]

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Set up Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json

    - name: Install backend dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest

    - name: Install frontend dependencies
      run: |
        cd frontend
        npm ci

    - name: Start backend server
      run: |
        cd backend
        uvicorn main:app --host 0.0.0.0 --port 8000 &
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        JWT_SECRET: test-secret-key-for-ci

    - name: Wait for backend to be ready
      run: |
        timeout 60 bash -c 'until curl -f http://localhost:8000/api/health; do sleep 2; done'

    - name: Run integration tests
      run: |
        cd backend
        python -m pytest tests/test_integration.py -v
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        JWT_SECRET: test-secret-key-for-ci
```

### 6. Create Staging Deployment Workflow

Create a workflow for staging deployment:

```yaml
# .github/workflows/deploy-staging.yml
name: Deploy to Staging

on:
  push:
    branches: [ develop ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: staging

    permissions:
      contents: read
      packages: write
      id-token: write

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata for Docker
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=sha,prefix={{branch}}-

    - name: Build and push Docker image for backend
      uses: docker/build-push-action@v5
      with:
        context: ./backend
        file: ./backend/Dockerfile
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

    - name: Build and push Docker image for frontend
      uses: docker/build-push-action@v5
      with:
        context: ./frontend
        file: ./frontend/Dockerfile
        push: true
        tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-frontend:${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

    - name: Deploy to staging environment
      run: |
        # This would typically involve deploying to your staging platform
        # For example, using kubectl, terraform, or a platform-specific CLI
        echo "Deploying to staging environment..."
        # Example: Deploy to a staging environment using your deployment tool
        # kubectl set image deployment/backend backend=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        # kubectl set image deployment/frontend frontend=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-frontend:${{ github.sha }}

    - name: Run post-deployment tests
      run: |
        # Run health checks and smoke tests
        # curl -f https://staging.yourapp.com/api/health
        echo "Running post-deployment tests..."

    - name: Notify team of deployment
      if: success()
      run: |
        # Send notification to your team's communication tool
        # Example: curl -X POST -H 'Content-Type: application/json' \
        #   -d '{"text":"Staging deployment successful: ${{ github.sha }}"}' \
        #   ${{ secrets.SLACK_WEBHOOK_URL }}
        echo "Deployment notification sent"
```

### 7. Create Production Deployment Workflow

Create a workflow for production deployment:

```yaml
# .github/workflows/deploy-production.yml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    permissions:
      contents: read
      packages: write
      id-token: write

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata for Docker
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=tag
          type=raw,value=latest

    - name: Build and push Docker image for backend
      uses: docker/build-push-action@v5
      with:
        context: ./backend
        file: ./backend/Dockerfile
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

    - name: Build and push Docker image for frontend
      uses: docker/build-push-action@v5
      with:
        context: ./frontend
        file: ./frontend/Dockerfile
        push: true
        tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-frontend:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max

    - name: Deploy to production environment
      run: |
        # This would typically involve deploying to your production platform
        echo "Deploying to production environment..."
        # Example: Deploy to production using your deployment tool
        # kubectl set image deployment/backend backend=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
        # kubectl set image deployment/frontend frontend=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-frontend:latest

    - name: Run post-deployment tests
      run: |
        # Run health checks and smoke tests
        echo "Running post-deployment tests..."

    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        draft: false
        prerelease: false

    - name: Notify team of production deployment
      if: success()
      run: |
        echo "Production deployment notification sent"
```

### 8. Create Security Scanning Workflow

Create a workflow for security scanning:

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * 1'  # Run weekly on Mondays at 2 AM

jobs:
  security-scan:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      if: always()
      with:
        sarif_file: 'trivy-results.sarif'

    - name: Run Python security audit
      run: |
        cd backend
        pip install bandit
        bandit -r . -f json -o bandit-results.json || true

    - name: Run Node.js security audit
      run: |
        cd frontend
        npm audit --audit-level=moderate
        npm audit --json > npm-audit.json || true
```

### 9. Create Dockerfiles for Applications

Create Dockerfiles for both backend and frontend:

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
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

FROM node:18-alpine AS runtime

WORKDIR /app

# Install production dependencies only
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy built application
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/next.config.ts ./

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs

EXPOSE 3000

ENV PORT=3000

CMD ["node_modules/.bin/next", "start"]
```

### 10. Create Environment Configuration

Create environment configuration files:

```yaml
# .github/workflows/deploy-environments.yml
name: Deploy to Multiple Environments

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata for Docker
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=sha,prefix={{branch}}-

    - name: Build and push Docker images
      run: |
        # Build and push backend
        docker build -t ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} ./backend
        docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

        # Build and push frontend
        docker build -t ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-frontend:${{ github.sha }} ./frontend
        docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-frontend:${{ github.sha }}

    - name: Deploy to ${{ inputs.environment }}
      run: |
        echo "Deploying to ${{ inputs.environment }} environment..."
        # Add your deployment commands here
```

## Best Practices

1. **Use environment-specific secrets** for different deployment stages
2. **Implement proper branch protection** rules requiring CI checks
3. **Use semantic versioning** for releases
4. **Implement rollback procedures** for failed deployments
5. **Monitor deployments** with health checks and alerts
6. **Scan for security vulnerabilities** regularly
7. **Maintain proper audit trails** for compliance
8. **Use infrastructure as code** for consistent deployments

## Deployment Checklist

- [ ] GitHub Actions workflows configured for all stages
- [ ] Environment-specific secrets properly set
- [ ] Branch protection rules in place
- [ ] Docker images properly configured
- [ ] Security scanning integrated
- [ ] Health checks implemented
- [ ] Rollback procedures documented
- [ ] Notification systems configured
- [ ] Monitoring and alerting set up

## Running Workflows

```bash
# Workflows run automatically on configured triggers
# To run a workflow manually, use the GitHub Actions UI
# Or trigger via GitHub API

# Example: Create a release tag to trigger production deployment
git tag v1.0.0
git push origin v1.0.0
```

This skill provides a comprehensive approach to CI/CD pipeline configuration for full-stack applications, ensuring secure, reliable, and automated deployments from development to production.