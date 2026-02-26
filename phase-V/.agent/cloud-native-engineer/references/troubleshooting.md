# Distributed Troubleshooting Matrix

Use this matrix to diagnose "Silent Failures" where logs appear clean but features are broken.

| Symptom | Probable Cause | Fix |
| :--- | :--- | :--- |
| **401 Unauthorized** | `JWKS_URL` mismatch | In K8s, `JWKS_URL` must point to the **internal** service name (e.g., `http://frontend:80/api/auth/jwks`). |
| **ERR_CONNECTION_REFUSED** | Browser vs Cluster DNS | Ensure browser calls use `localhost` (via port-forward) while internal calls use service names. |
| **Sidecar Restart Loop** | Redis Connection Timeout | Increase `initialDelaySeconds` in `readinessProbes` to 30-45s. Dapr needs time to dial Redis. |
| **Reminders Not Triggering** | Job naming collision | Ensure `dapr-app-id` is unique for each service and matches the Job ID used in code. |
| **Agent Latency (5s+)** | MCP Cold Start | Implement the persistent MCP singleton in `lifespan` as per `LATENCY_OPTIMIZATION.md`. |

## Diagnostic Workflow

1. **Check Infrastructure First**:
   ```bash
   kubectl get pods -l app=redis
   dapr list -k
   ```
2. **Sniff Cross-Service Traffic**:
   If a service isn't receiving events, check the `daprd` container logs:
   ```bash
   kubectl logs <pod-name> -c daprd
   ```
3. **Validate Auth Pipeline**:
   Log the `JWKS_URL` on backend startup to ensure it correctly resolves to the expected internal/external address.
4. **Environment Sanitization**:
   Ensure `.env` is NOT copied into Docker images. Use K8s Secrets for all sensitive keys.
