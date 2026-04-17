---
description: Debug enterprise microservice failures across Java/Spring Boot and Python/FastAPI stacks (Enterprise Microservice)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR [⋯]

**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory

**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Environment Setup
// turbo
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype enterprise-microservice` and parse for debugging tools availability.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/enterprise-microservice/enterprise-microservice-constitution.md` for enterprise anti-patterns and multi-stack standards
- Read `${ARCHETYPES_BASEDIR}/backend-only/backend-only-constitution.md` for inherited base patterns

### 3. Parse Input
Extract from $ARGUMENTS: error description, error messages/stack traces, technology stack (Java/Python), affected endpoints/services, steps to reproduce, environment (dev/nprd/stage/prod), pod/container logs. Request clarification if incomplete.

### 4. Detect Technology Stack

Identify service stack from:
- **Java/Spring Boot**: `pom.xml`, `build.gradle`, `application.yaml`, `@SpringBootApplication`
- **Python/FastAPI**: `pyproject.toml`, `requirements.txt`, `main.py`, `FastAPI()`

### 5. Categorize Error Type

Analyze error to determine category:

**API Errors** (Both Stacks):
- HTTP 4xx client errors (validation, auth, not found)
- HTTP 5xx server errors (crashes, timeouts)
- Request timeout errors
- Rate limiting issues

**Spring Boot-Specific Errors**:
- Bean creation failures (`BeanCreationException`)
- Circular dependency issues
- Actuator endpoint failures
- Profile misconfiguration
- JPA/Hibernate mapping errors
- Flyway/Liquibase migration failures

**FastAPI-Specific Errors**:
- Pydantic validation errors
- Async event loop issues
- SQLAlchemy connection pool exhaustion
- Alembic migration failures

**Infrastructure Errors** (Both Stacks):
- Pod crashes and restarts (OOMKilled)
- Liveness/readiness probe failures
- Istio sidecar issues
- Key Vault access failures
- Graceful shutdown timeout

**Deployment Errors** (Both Stacks):
- Docker build failures
- Helm deployment failures
- Pipeline failures
- Image pull errors

### 6. Debug Spring Boot Errors

**A. Bean Creation Failures**:
```java
// SYMPTOM: BeanCreationException on startup

// DEBUG APPROACH:
// 1. Check constructor dependencies
// 2. Verify @Configuration classes
// 3. Check for missing beans or qualifiers
// 4. Review circular dependency chains

// FIX: Use constructor injection with @Lazy for circular deps
@Service
public class OrderService {
    private final UserService userService;

    public OrderService(@Lazy UserService userService) {
        this.userService = userService;
    }
}
```

**B. Actuator Health Failures**:
```yaml
# SYMPTOM: /actuator/health returns DOWN

# DEBUG APPROACH:
# 1. Check individual health indicators
# 2. Verify database connectivity
# 3. Check external service health
# 4. Review custom HealthIndicator implementations

# FIX: Add detailed health checks
management:
  endpoint:
    health:
      show-details: always
  health:
    db:
      enabled: true
    redis:
      enabled: true
```

**C. JPA/Hibernate Mapping Errors**:
```java
// SYMPTOM: MappingException or LazyInitializationException

// DEBUG APPROACH:
// 1. Verify entity annotations
// 2. Check fetch type (LAZY vs EAGER)
// 3. Review transaction boundaries
// 4. Check for N+1 query issues

// FIX: Use @EntityGraph for fetch optimization
@EntityGraph(attributePaths = {"orders", "orders.items"})
Optional<User> findByIdWithOrders(Long id);
```

### 7. Debug FastAPI Errors

**A. Async Event Loop Issues**:
```python
# SYMPTOM: "RuntimeError: This event loop is already running"

# DEBUG APPROACH:
# 1. Check for mixing sync/async code
# 2. Verify database session management
# 3. Check background task configuration

# FIX: Use async-compatible libraries
import httpx

async def call_external_api():
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(url)
        return response.json()
```

**B. Connection Pool Exhaustion**:
```python
# SYMPTOM: "QueuePool limit exceeded"

# DEBUG APPROACH:
# 1. Check pool size configuration
# 2. Monitor active connections
# 3. Verify context managers for sessions

# FIX: Adjust pool settings
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,
)
```

### 8. Debug Infrastructure Errors

**A. Pod Crashes and OOM Kills**:
```bash
# DEBUG APPROACH (both stacks):
# 1. kubectl logs <pod-name> -n <namespace>
# 2. kubectl logs <pod-name> -n <namespace> --previous
# 3. kubectl top pod <pod-name> -n <namespace>
# 4. Review resource limits in Helm values

# FIX: Adjust resource limits
# Java typically needs more memory than Python
# Java: requests 512Mi, limits 1-2Gi
# Python: requests 256Mi, limits 512Mi-1Gi
```

**B. Health Probe Failures**:
```bash
# DEBUG APPROACH:
# 1. Test health endpoints manually
# 2. Check probe path matches stack:
#    - Spring Boot: /actuator/health/liveness
#    - FastAPI: /monitor/liveness
# 3. Verify probe timeout settings
# 4. Check if startup probe allows enough time

# FIX: Adjust probe configuration in Helm
startupProbe:
  httpGet:
    path: /actuator/health/liveness  # or /monitor/liveness
    port: 8080                        # or 8100 for FastAPI
  failureThreshold: 30
  periodSeconds: 10
```

**C. Graceful Shutdown Issues**:
```bash
# SYMPTOM: Requests fail during deployments

# DEBUG APPROACH:
# 1. Check terminationGracePeriodSeconds (must be >= 30s)
# 2. Verify shutdown hooks are configured
# 3. Check Istio sidecar cleanup

# FIX (Spring Boot):
# application.yaml:
# server.shutdown: graceful
# spring.lifecycle.timeout-per-shutdown-phase: 45s

# FIX (FastAPI):
# Add shutdown event handler
@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()
```

### 9. Debug Deployment Errors

**A. Docker Build Failures**:
```bash
# DEBUG APPROACH:
# 1. Check build logs for dependency errors
# 2. Verify base image availability
# 3. Java: check Maven/Gradle cache, JDK version
# 4. Python: check Poetry lock file, JFrog auth

# Common Java fix: Multi-stage with dependency caching
# Common Python fix: Poetry lock --no-update
```

**B. Helm Deployment Failures**:
```bash
# DEBUG APPROACH:
# 1. helm status <release> -n <namespace>
# 2. kubectl get events -n <namespace>
# 3. Verify image tag and registry access
# 4. Check probe paths match the technology stack

# Dry-run to validate:
helm upgrade <release> ./helm/<app> \
  --dry-run --debug \
  --set image.version=<tag> \
  -n <namespace>
```

### 10. Provide Debugging Guidance

For each identified issue:

**Issue Description**: Clear explanation of the problem

**Root Cause**: Why the error occurred (code, config, infrastructure)

**Stack-Specific Context**: Java/Spring Boot or Python/FastAPI specific notes

**Fix**: Specific changes needed with code examples

**Verification**: How to test the fix

**Prevention**: How to avoid in future (monitoring, tests, guardrails)

### 11. Generate Debug Report

```
🐛 Enterprise Microservice Debug Report

📍 Technology Stack: <Java/Spring Boot | Python/FastAPI>
📍 Error Type: <category>
📍 Severity: <critical/high/medium/low>
📍 Affected Services: <list>
📍 Environment: <dev/nprd/stage/prod>

🔍 Root Cause Analysis:
<Detailed explanation>

🛠️ Fixes Applied:
1. <Fix description> - <file>:<line>
2. <Configuration change> - <config file>

✅ Verification Steps:
1. Test endpoint / run tests
2. Check logs
3. Monitor metrics

🚫 Prevention Measures:
- Add test coverage
- Add monitoring alert
- Update documentation
```

### 12. Validate Fix

// turbo
Run tests to verify fix based on stack:
- **Java**: `./mvnw test`
- **Python**: `poetry run pytest -v`

Check deployment health and report confirmation.

## Error Handling

**Cannot Reproduce**: Request pod logs, Application Insights traces, exact request details.

**Unknown Stack**: Ask user to specify or auto-detect from project files.

**Multiple Root Causes**: Prioritize by severity and impact, address systematically.

## Examples

**Example 1**: `/debug-enterprise-microservice Spring Boot actuator health returns DOWN after deployment`

**Example 2**: `/debug-enterprise-microservice FastAPI pod keeps restarting with OOMKilled status`

**Example 3**: `/debug-enterprise-microservice Java service gets BeanCreationException on startup`

**Example 4**: `/debug-enterprise-microservice Helm deployment fails with probe timeout for Python service`

## References

Constitution: `${ARCHETYPES_BASEDIR}/enterprise-microservice/enterprise-microservice-constitution.md`
Backend-Only Constitution: `${ARCHETYPES_BASEDIR}/backend-only/backend-only-constitution.md`
