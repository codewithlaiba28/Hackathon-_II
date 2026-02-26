# kubectl-ai Usage Guide for Todo Application

## Installation

If not already installed, install kubectl-ai plugin:

```bash
# Install kubectl-ai plugin
curl -fsSL https://raw.githubusercontent.com/itaysk/kubectl-ai/master/install.sh | sh

# Or using krew (if available)
kubectl krew install ai
```

## Configuration

Before using kubectl-ai, you need to configure your OpenAI API key:

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

## Common Queries for Todo Application

### Pod Management
```bash
# Show all pods in todo-app namespace
kubectl ai "show all pods in todo-app namespace"

# Show logs of backend pod
kubectl ai "show logs of backend pod in todo-app namespace"

# Describe the frontend deployment
kubectl ai "describe the frontend deployment in todo-app namespace"

# Why is a specific pod failing?
kubectl ai "why is pod todo-app-backend-xyz failing?"
```

### Service and Network Queries
```bash
# Show all services
kubectl ai "show all services in todo-app namespace"

# Check if frontend service is accessible
kubectl ai "is the frontend service accessible?"

# Show ingress configuration
kubectl ai "show ingress configuration for todo.local"
```

### Resource and Scaling Queries
```bash
# Show resource usage of application
kubectl ai "show resource usage of todo application"

# Scale backend deployment
kubectl ai "scale backend deployment to 3 replicas in todo-app namespace"

# Check if resource limits are adequate
kubectl ai "are the resource limits adequate for the todo application?"
```

### Troubleshooting
```bash
# Get status of all resources
kubectl ai "get status of all resources in todo-app namespace"

# Troubleshoot common issues
kubectl ai "troubleshoot common issues with the todo application"

# Check if ingress is working
kubectl ai "is the ingress working for todo.local?"
```

## Best Practices

1. **Be Specific**: Use specific namespaces and resource names in your queries
2. **Use Natural Language**: Formulate queries as you would ask a Kubernetes expert
3. **Combine Actions**: You can ask for multiple operations in a single query
4. **Check Before Action**: Always verify what a command will do before executing destructive actions

## Examples for This Project

```bash
# Deploy the application
kubectl ai "deploy the todo-app Helm chart with development values"

# Check application health
kubectl ai "check health of todo application including pods, services, and ingress"

# Troubleshoot if frontend is not accessible
kubectl ai "troubleshoot why frontend is not accessible at todo.local"

# Scale resources based on load
kubectl ai "suggest resource scaling for high load scenario"
```

## Security Considerations

- Never expose your OpenAI API key in shared environments
- Be cautious with commands that modify production resources
- Always verify AI-generated commands before execution
- Use dry-run options when available to preview changes