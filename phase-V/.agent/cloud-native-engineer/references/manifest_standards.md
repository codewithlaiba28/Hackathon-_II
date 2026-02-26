# Standardized Kubernetes Manifest Patterns

Consistency across microservices manifests is key to a maintainable distributed system. Follow these standards for all deployments.

## 1. Naming Conventions
- **Lower-kebab-case**: All resource names must use kebab-case (e.g., `task-service`, `notification-deployment`).
- **Internal DNS**: Use short, predictable service names (e.g., `redis-master`, `backend`) to simplify cross-service configuration.

## 2. Resource Management (Config & Secrets)
Never hardcode environment-specific variables.

### ConfigMaps
Use for non-sensitive values like API ports, LOG_LEVEL, or environment tags.
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-config
data:
  LOG_LEVEL: "INFO"
  ALLOWED_ORIGINS: "*"
```

### Secrets
Use for API keys, DB passwords, and Auth secrets.
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  GEMINI_API_KEY: <base64-encoded-key>
```

## 3. Service Definitions
Always use the `type: ClusterIP` for internal services. Only use `LoadBalancer` or `NodePort` for the main frontend/ingress entry point.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  selector:
    app: backend
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
```

## 4. Manifest Organization
Keep your deployment directory structured:
```
deploy/
├── 01-namespace.yaml
├── 02-infrastructure/ (Redis, Dapr sidecar configs)
├── 03-config/ (ConfigMaps & Secrets)
└── 04-services/ (Application microservices)
```
Applying them in numerical order ensures dependencies are satisfied.
