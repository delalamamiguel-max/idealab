# Container Solution Architect

Design and implement containerized solutions using Podman/Docker with security hardening, credential management, and operational excellence.

## Purpose

This archetype helps you build containerized applications that:

- Use multi-stage Dockerfiles for minimal production images
- Compile credentials at build time (never in runtime ENV)
- Run services with process supervision (supervisord)
- Enforce resource limits and health checks
- Support both Podman (dev) and Kubernetes (prod) runtimes

## Key Patterns

- **Credential Compilation**: Secrets compiled into config files at build time, readable only by service UID
- **Base + Overlay Images**: Heavy base image built once, thin per-user credential overlays
- **Process Supervision**: supervisord manages multiple services in a single container
- **Overlay FS for Scratch**: Zero memory overhead for temporary storage
- **Health Endpoints**: Liveness and readiness checks for all services

## Workflows

| Workflow | Description |
|----------|-------------|
| `/scaffold-container-solution-architect` | Generate complete containerized solution with Containerfile, scripts, and compose |
| `/debug-container-solution-architect` | Diagnose container build failures, health check issues, and process supervision problems |
| `/refactor-container-solution-architect` | Improve existing container setup for security, performance, or maintainability |
| `/test-container-solution-architect` | Validate container builds, health checks, and lifecycle operations |
| `/document-container-solution-architect` | Generate documentation for container architecture and operations |
| `/compare-container-solution-architect` | Compare two container approaches or architectures |

## Anti-Patterns (Avoided)

- ✘ Hard-coded credentials in Containerfiles
- ✘ Using `latest` tag without digest
- ✘ Running processes as root (UID 0)
- ✘ Missing health checks
- ✘ ENV vars for secrets at runtime
- ✘ Public registry base images
- ✘ tmpfs for scratch in multi-container scenarios
- ✘ Single-stage builds with dev dependencies

## Related Archetypes

- `aks-devops-deployment` — Deploy containers to AKS with Helm
- `dev-ops-engineer` — Orchestrate data pipelines with CI/CD
- `microservice-cicd-architect` — CI/CD pipelines for microservices
