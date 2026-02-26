# Research Document: Phase 4 - Local Kubernetes Deployment

## Decision: Multi-stage Docker Builds for Optimization
**Rationale**: Multi-stage builds significantly reduce final image size by separating build dependencies from runtime environment. For frontend (Next.js), the build stage compiles assets which are then copied to a lightweight nginx container. For backend (FastAPI), dependencies are installed in one stage and copied to a minimal Python runtime.

**Alternatives considered**:
- Single-stage builds: Result in much larger images with unnecessary build tools in runtime
- Build-time variables: Less effective than true multi-stage separation

## Decision: Minikube Local Registry Strategy
**Rationale**: Using `eval $(minikube docker-env)` allows building images directly into Minikube's local registry without needing external registries for development. This simplifies local development and avoids network dependencies.

**Alternatives considered**:
- Docker Hub: Requires internet and public/private repo setup for development
- Kind/local registry: More complex setup than Minikube's built-in capability

## Decision: Continue with Neon Serverless PostgreSQL
**Rationale**: Neon provides serverless PostgreSQL with smart caching and instant pause/resume capabilities. It maintains connection with existing Phase 3 setup while providing reliable external database access. For offline development, local PostgreSQL can be enabled as an alternative.

**Alternatives considered**:
- Local PostgreSQL StatefulSet: Would require persistent volume management and backup strategies
- Other cloud DB providers: Would require additional setup and learning

## Decision: Kubernetes Secrets for Sensitive Data
**Rationale**: Kubernetes Secrets provide encrypted storage for sensitive information like database credentials and API keys. Combined with proper RBAC, they offer secure access control for pods while keeping sensitive data out of ConfigMaps and environment variables.

**Alternatives considered**:
- External secret stores (HashiCorp Vault, AWS Secrets Manager): Overengineering for local development environment
- Environment variables: Less secure and harder to manage

## Decision: Ingress with nginx-ingress for Service Exposure
**Rationale**: Ingress provides standardized way to expose HTTP/HTTPS routes from outside the cluster to services within the cluster. nginx-ingress is widely supported and works well with Minikube via the addon.

**Alternatives considered**:
- NodePort: Limited to specific port range and less flexible
- LoadBalancer: Not typically available in Minikube without additional cloud provider

## Decision: Resource Limits Based on Application Needs
**Rationale**: Based on typical resource consumption of Next.js frontend (~100-200MB RAM, ~0.1-0.5 CPU) and FastAPI backend (~200-400MB RAM, ~0.2-0.5 CPU), setting conservative limits that allow scaling while preventing resource exhaustion.

**Frontend**:
- Request: 100Mi memory, 0.1 CPU
- Limit: 300Mi memory, 0.5 CPU

**Backend**:
- Request: 200Mi memory, 0.2 CPU
- Limit: 500Mi memory, 0.8 CPU

**Alternatives considered**:
- No limits: Could lead to resource exhaustion
- Fixed amounts: Less adaptable to varying loads

## Decision: Umbrella Helm Chart Structure
**Rationale**: An umbrella chart allows managing the entire application as a single unit while maintaining separate configurations for frontend and backend. This approach provides better organization than individual charts while allowing shared configurations.

**Alternatives considered**:
- Separate charts: Would require coordinating deployments between charts
- Single combined chart: Would be harder to maintain and reuse components

## Decision: ConfigMaps for Non-Sensitive Configuration
**Rationale**: ConfigMaps are designed specifically for storing non-sensitive configuration data that can be mounted as volumes or injected as environment variables. They provide better separation of concerns than hardcoding configuration values.

**Alternatives considered**:
- Environment variables directly in Deployment: Less flexible and harder to update
- Inline configuration: Makes reusing templates more difficult

## Decision: Init Containers for Database Migrations
**Rationale**: Init containers are ideal for running setup tasks like database migrations before the main application starts. They ensure the database schema is properly set up before the application attempts to connect.

**Alternatives considered**:
- Application startup migrations: Could lead to race conditions with multiple replicas
- Manual migrations: Not reproducible or automated

## Decision: Health Check Endpoints and Timing
**Rationale**: Using application-specific endpoints for liveness and readiness probes with appropriate timeouts and thresholds. Readiness probes check if the app is ready to serve traffic, while liveness probes restart unresponsive containers.

**Settings**:
- Initial delay: 30 seconds
- Period: 10 seconds
- Timeout: 5 seconds
- Success threshold: 1
- Failure threshold: 3

**Alternatives considered**:
- TCP socket checks: Less informative than HTTP health checks
- Exec commands: More complex than HTTP endpoints