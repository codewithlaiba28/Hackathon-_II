# Troubleshooting Guide

This guide provides common troubleshooting steps for setting up, deploying, and operating the Todo Chatbot application with its cloud-native components.

## 1. General Kubernetes/Minikube Issues

### Problem: `kubectl` commands fail or cluster is not responsive.
*   **Verify Minikube status:**
    ```bash
    minikube status
    ```
    If not running, start it: `minikube start`
*   **Check `kubectl` context:** Ensure `kubectl` is configured to interact with your Minikube cluster.
    ```bash
    kubectl config current-context
    ```
    If it's not `minikube`, switch to it: `kubectl config use-context minikube`
*   **Check for resource limits:** Minikube might be running out of resources.
    ```bash
    minikube addons configure dashboard # and check usage
    ```
    Consider increasing Minikube's resources: `minikube config set memory 8192` (then `minikube delete` and `minikube start` may be needed).

## 2. Dapr Related Issues

### Problem: Dapr sidecars are not injecting or applications are not communicating via Dapr.
*   **Verify Dapr control plane status:**
    ```bash
    dapr status -k
    ```
    All Dapr control plane components should be healthy. If not, re-initialize Dapr: `dapr uninstall -k --all && dapr init -k`
*   **Check Dapr annotations on deployments:** Ensure your Kubernetes deployment YAMLs (in `helm-charts/todo-app/templates/`) have the correct Dapr annotations:
    ```yaml
    # Example for backend deployment
    annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "backend"
        dapr.io/app-port: "8000" # Or relevant port for the service
        dapr.io/config: "appconfig" # Name of your Dapr Configuration
    ```
*   **Check Dapr logs for specific pods:**
    ```bash
    kubectl logs <pod-name> -c daprd -n todo-app
    ```
    Look for errors during sidecar startup or communication issues.

### Problem: Dapr components (statestore, pubsub, secretstore) are not working.
*   **Verify Dapr component status:**
    ```bash
    dapr components -k -n todo-app
    ```
    All components should show `STATUS: HEALTHY`.
*   **Check component YAMLs:** Double-check the configuration in `dapr/components/*.yaml` for correctness, especially connection strings, secrets references, and metadata.
*   **Check component logs:**
    ```bash
    kubectl logs <dapr-operator-pod-name> -n dapr-system
    kubectl logs <dapr-sentry-pod-name> -n dapr-system
    ```
    These logs might reveal why a component failed to initialize or bind.

## 3. Kafka Related Issues

### Problem: Events are not being published/consumed by services (e.g., Recurring Task Service not reacting to `task.completed`).
*   **Verify Kafka cluster health:**
    ```bash
    helm test todo-app-kafka # if using Bitnami chart, or check Kafka pod logs
    ```
*   **Check `kafka-pubsub` Dapr component:** See "Dapr Components Issues" above. Ensure it's healthy and correctly configured to connect to Kafka.
*   **Check service logs:**
    *   **Publisher service (e.g., Backend for `task.completed`):** Check logs for errors during `client.publish_event`.
        ```bash
        kubectl logs <backend-pod-name> -n todo-app
        ```
    *   **Subscriber service (e.g., Recurring Task Service, Notification Service):** Check logs for errors during event reception or processing.
        ```bash
        kubectl logs <recurring-task-service-pod-name> -n todo-app
        kubectl logs <notification-service-pod-name> -n todo-app
        ```
*   **Verify Dapr subscription YAML:** Ensure the `dapr.io/app-id` in the subscription matches the service name, and the topic names (`task-events`, `reminders`) are correct. Subscriptions are typically dynamic for FastAPI applications, so check logs of the FastAPI app starting up for subscription errors.

## 4. PostgreSQL (Neon) Issues

### Problem: Services cannot connect to the Neon database.
*   **Verify Kubernetes Secret:** Ensure the `neon-db-connection` Kubernetes Secret exists in the `todo-app` namespace and contains the correct connection string.
    ```bash
    kubectl get secret neon-db-connection -n todo-app -o yaml
    ```
    Decode the `connection-string` field to verify.
*   **Check Dapr `statestore` component:** See "Dapr Components Issues" above. Ensure it's correctly configured to use the `neon-db-connection` secret.
*   **Check service logs:** The backend service or other services trying to access the database will show connection errors in their logs.
    ```bash
    kubectl logs <backend-pod-name> -n todo-app
    ```
*   **Network connectivity:** If running on a local Minikube, ensure there are no firewall rules preventing egress to Neon's cloud-hosted database.

## 5. Application Specific Issues (Backend/Frontend)

### Problem: Frontend not displaying data or backend API calls failing.
*   **Check Frontend logs:**
    ```bash
    kubectl logs <frontend-pod-name> -n todo-app
    ```
    Look for JavaScript errors, API call failures, or network issues.
*   **Check Backend logs:**
    ```bash
    kubectl logs <backend-pod-name> -n todo-app
    ```
    Look for API route errors, database query failures, or Dapr client errors.
*   **Verify service exposure:** Ensure Kubernetes Services are correctly exposing the ports for Frontend (e.g., NodePort or LoadBalancer) and Backend services.
    ```bash
    kubectl get services -n todo-app
    ```
    You should be able to access the Frontend externally and the Backend internally via its service name.

### Problem: Authentication/Authorization issues.
*   **Check `better-auth` integration:** Verify that the JWT tokens are being correctly generated and validated.
*   **Check user creation/login flow:** Step through the login/signup process and observe network requests and backend logs for errors.
*   **Ensure `get_current_user` is correctly implemented:** In `backend/src/auth.py`, ensure the placeholder `get_current_user` is correctly configured and returning user data.
*   **Dapr secrets access:** If any auth secrets are stored via Dapr secrets, ensure the `kubernetes-secrets` component is healthy and accessible.