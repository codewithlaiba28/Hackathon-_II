# Universal Dapr Configuration Patterns

Dapr (Distributed Application Runtime) provides enterprise-grade building blocks. Use these patterns for any project.

## 1. Pub/Sub (Redis Backend)
Ideal for local development and cloud-native scaling.
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master:6379 # Points to cluster internal DNS
  - name: redisPassword
    secretKeyRef:
      name: redis-secret
      key: password
```

## 2. State Store (Redis or Postgres)
Persistent storage for service state.
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master:6379
```

## 3. Scheduled Jobs (Reminders/Cron)
Use the Dapr Jobs API (state-backed) for time-specific events.
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: jobs
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master:6379
```

## Best Practice: Local vs Cloud
For local dev (Minikube), use standalone Redis. For Production, swap the `spec.type` to `pubsub.kafka`, `pubsub.azure.servicebus`, or `pubsub.google.pubsub` without changing application code.
