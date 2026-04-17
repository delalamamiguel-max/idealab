---
description: Refactor AKS microservice deployment to apply security, progressive delivery, and observability patterns
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Parse Refactoring Request

Extract from $ARGUMENTS:
- Service/component to refactor
- Refactoring goals (security, performance, observability)
- Current state analysis
- Constraints (downtime, timeline)

### 2. Analyze Current State

Scan existing deployment for:
- [ ] Dockerfile best practices violations
- [ ] Helm chart security gaps
- [ ] CI/CD pipeline weaknesses
- [ ] Observability gaps
- [ ] Constitution compliance issues

### 3. Refactor Dockerfile

Apply improvements:

```dockerfile
# Before: Unpinned base image
FROM node:20-alpine

# After: Pinned with digest, non-root, multi-stage
FROM artifact.it.att.com/docker-proxy/node:20-alpine@sha256:... AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM artifact.it.att.com/docker-proxy/node:20-alpine@sha256:...
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER 1001
HEALTHCHECK --interval=30s CMD wget -q --spider http://localhost:3000/health
CMD ["node", "server.js"]
```

### 4. Refactor Helm Charts

Apply security context and resource optimization:

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1001
  capabilities:
    drop: [ALL]
  readOnlyRootFilesystem: true

resources:
  requests:
    cpu: 250m
    memory: 512Mi
  limits:
    cpu: 1000m
    memory: 1Gi
```

### 5. Refactor CI/CD Pipeline

Add:
- Container vulnerability scanning
- SBOM generation
- Image signing
- Progressive delivery gates
- Automated rollback triggers

### 6. Refactor Observability

Add:
- JSON structured logging
- Prometheus metrics endpoint (`/metrics`)
- OpenTelemetry tracing
- Health check endpoints

### 7. Validate Constitution Compliance

Check all hard-stop rules from constitution:
- [ ] Supply chain security (1.1)
- [ ] Deployment safety (1.2)
- [ ] Resource governance (1.3)
- [ ] Observability (1.4)
- [ ] Secrets management (1.5)
- [ ] Registry configuration (1.7, 1.8)

## Error Handling

**Breaking Changes**: Flag changes that require coordination and provide migration path.

**Downtime Required**: Recommend blue/green deployment for zero-downtime refactoring.

**Constitution Violation**: Block refactoring that would introduce violations.

## Examples

### Example 1: Security Hardening

```
/refactor-aks-devops-deployment "
Harden fraud-api Dockerfile and Helm charts.
Add non-root user, pin base images, drop capabilities.
"
```

### Example 2: Observability Upgrade

```
/refactor-aks-devops-deployment "
Add Prometheus metrics and structured logging to user-service.
Current: Basic console.log, no metrics endpoint.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/aks-devops-deployment/aks-devops-deployment-constitution.md`
- **Security Hardening**: Constitution Section V
- **Related**: debug-aks-devops-deployment, test-aks-devops-deployment
