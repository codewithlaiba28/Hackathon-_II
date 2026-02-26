# Troubleshooting Guide for Todo Application

## Common Issues and Solutions

### Pod Issues

#### Pods stuck in Pending state
**Problem**: Pods show status Pending instead of Running
**Solution**:
1. Check resource requests vs available cluster resources:
   ```bash
   kubectl describe nodes
   kubectl get pods -o wide
   ```
2. Reduce resource requests in values.yaml if needed
3. Ensure Minikube has adequate resources allocated

#### Pods stuck in ContainerCreating state
**Problem**: Pods show status ContainerCreating indefinitely
**Solution**:
1. Check if images exist in the registry:
   ```bash
   kubectl describe pod <pod-name> -n todo-app
   ```
2. Verify image pull secrets if using private registry
3. Check if the node can pull images

#### CrashLoopBackOff
**Problem**: Pods are constantly restarting
**Solution**:
1. Check pod logs:
   ```bash
   kubectl logs <pod-name> -n todo-app
   kubectl logs <pod-name> -n todo-app --previous
   ```
2. Verify environment variables and secrets are correctly set
3. Check if the container is able to connect to required services

### Service and Networking Issues

#### Cannot access application via Ingress
**Problem**: Application is not accessible at http://todo.local
**Solution**:
1. Verify ingress is properly configured:
   ```bash
   kubectl get ingress -n todo-app
   kubectl describe ingress -n todo-app
   ```
2. Check if the /etc/hosts entry exists:
   ```bash
   grep todo.local /etc/hosts
   ```
3. Verify Minikube ingress addon is enabled:
   ```bash
   minikube addons list | grep ingress
   ```

#### Port forwarding not working
**Problem**: Cannot access services via port forwarding
**Solution**:
1. Check if services are running:
   ```bash
   kubectl get svc -n todo-app
   kubectl describe svc todo-app-frontend -n todo-app
   ```
2. Verify correct port numbers are used

### Database Connection Issues

#### Backend cannot connect to database
**Problem**: Backend logs show database connection errors
**Solution**:
1. Verify database URL in secrets:
   ```bash
   kubectl get secrets -n todo-app
   kubectl describe secret todo-app-db-secret -n todo-app
   ```
2. Check if database is accessible from the cluster
3. Verify SSL settings if connecting to Neon PostgreSQL

### Image Building Issues

#### Docker build fails
**Problem**: Docker build process fails
**Solution**:
1. Check Dockerfile syntax
2. Verify base images exist and are accessible
3. Check for missing dependencies in the build context

#### Large image sizes
**Problem**: Docker images exceed size limits
**Solution**:
1. Use multi-stage builds to separate build and runtime environments
2. Use minimal base images (alpine, slim variants)
3. Remove unnecessary files in Dockerfile

## Diagnostic Commands

### General Cluster Status
```bash
# Check all pods
kubectl get pods -A

# Check all nodes
kubectl get nodes

# Check cluster info
kubectl cluster-info
```

### Application-Specific Diagnostics
```bash
# Check application pods
kubectl get pods -n todo-app

# Check application services
kubectl get svc -n todo-app

# Check application ingress
kubectl get ingress -n todo-app

# Check application logs
kubectl logs -n todo-app -l app=todo-frontend
kubectl logs -n todo-app -l app=todo-backend

# Check application events
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

### Configuration Verification
```bash
# Check ConfigMaps
kubectl get configmaps -n todo-app

# Check Secrets
kubectl get secrets -n todo-app

# Render Helm templates locally
helm template todo-app ./helm-charts/todo-app --namespace todo-app
```

## Using kubectl-ai for Troubleshooting

If kubectl-ai is available, you can use natural language queries:

```bash
# Describe why a pod is failing
kubectl ai "why is the backend pod failing in todo-app namespace?"

# Get a summary of all resources
kubectl ai "summarize all resources in todo-app namespace"

# Troubleshoot common issues
kubectl ai "troubleshoot common issues with the todo application"
```

## Debugging Steps

1. **Identify the problem area** (pods, services, networking, database)
2. **Check the logs** for error messages
3. **Verify configuration** (ConfigMaps, Secrets, values)
4. **Test connectivity** between services
5. **Validate resource availability** (CPU, memory, storage)
6. **Check events** for any warnings or errors

## When to Restart

Sometimes a simple restart can resolve issues:

```bash
# Restart all pods in a deployment
kubectl rollout restart deployment/todo-app-frontend -n todo-app
kubectl rollout restart deployment/todo-app-backend -n todo-app

# Check rollout status
kubectl rollout status deployment/todo-app-frontend -n todo-app
kubectl rollout status deployment/todo-app-backend -n todo-app
```

## Getting Help

If issues persist:

1. Check the application documentation
2. Look for similar issues in the project repository
3. Use the AI troubleshooting commands if available
4. Consult Kubernetes documentation for advanced issues