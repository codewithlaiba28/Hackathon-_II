# Professional Kubernetes Deployment Workflow

Deploying distributed systems is fragile. Follow these production-ready steps for any project.

## 1. Local Pre-flight (Parity Check)
Before deploying to K8s, ensure your code handles "Env-Var Parity":
- **Standard**: All API calls should use a configurable variable.
- **Internal DNS**: Use internal service names (e.g., `http://backend:8000`) for cross-service calls.

## 2. Container Strategy (Elite Builds)
Microservices require targeted builds. Use the Multi-Stage pattern to keep images under 200MB.
- **Reference**: [DOCKER_BEST_PRACTICES.md](docker_best_practices.md).

## 3. Automated Orchestration
For a zero-error deployment sequence, use the provided orchestration script.

### One-Click Deployment (Local)
```powershell
powershell -File ./scripts/deploy_minikube.ps1 -ApiUrl http://localhost:8000
```
This script ensures:
1. Minikube connection is active.
2. Frontend API URLs are correctly baked into the image.
3. Infrastructure (Redis/Dapr) is healthy before application rollout.

## 4. Health Probes (Critical Tuning)
Always include liveness and readiness probes to handle sidecar startup latency. Standard K8s probes are often too aggressive for the Dapr sidecar connection handshake.

### Elite Pod Spec Pattern
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 60  # Safe window for sidecar attachment
  periodSeconds: 15
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
```

## 5. Verification Checklist
1. **Sidecars**: `kubectl get pods` should show `2/2` (App + Dapr).
2. **Connectivity**: Verify backend can resolve frontend via internal DNS.
3. **Tools**: Run [verify_cluster.ps1](../scripts/verify_cluster.ps1) to confirm end-to-end health.
