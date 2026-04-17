---
description: Refactor enterprise microservice to apply multi-stack best practices, security, and cloud-native patterns (Enterprise Microservice)
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
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype enterprise-microservice` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/enterprise-microservice/enterprise-microservice-constitution.md` for enterprise patterns, multi-stack standards, and security requirements
- Read `${ARCHETYPES_BASEDIR}/backend-only/backend-only-constitution.md` for inherited base rules

### 3. Parse Input
Extract from $ARGUMENTS: target files/modules, technology stack (Java/Python), refactoring goals (performance, security, DevOps compliance, code quality, enterprise standards), specific issues to address. Request clarification if incomplete.

### 4. Detect Technology Stack

Identify service stack from project files:
- **Java/Spring Boot**: `pom.xml`, `build.gradle`, `application.yaml`, `@SpringBootApplication`
- **Python/FastAPI**: `pyproject.toml`, `requirements.txt`, `main.py`, `FastAPI()`

### 5. Analyze Existing Code

Scan target service for issues across both stacks:

**Enterprise Compliance**:
- Missing health endpoints (`/actuator/health` or `/monitor/liveness`)
- Graceful shutdown not configured or < 30s
- Public endpoints without authentication
- Missing OpenTelemetry instrumentation

**DevOps Compliance** (inherited from backend-only):
- Not following cookiecutter structure
- JFrog auth not using variable groups
- Missing workload identity configuration
- Istio sidecar not configured
- Missing resource limits/requests
- Missing liveness/readiness probes
- Secrets hardcoded instead of Key Vault

**Spring Boot-Specific Issues**:
- Field injection instead of constructor injection
- Missing `@RestControllerAdvice` global error handler
- Not using RFC 7807 ProblemDetail for errors
- Missing profile-based configuration
- Actuator endpoints over-exposed
- Missing `@ConfigurationProperties` validation
- N+1 queries without `@EntityGraph`
- Missing Flyway/Liquibase migrations
- HikariCP pool not tuned

**FastAPI-Specific Issues**:
- Missing Pydantic validation on inputs
- Synchronous blocking operations in async handlers
- No structured logging (JSON format)
- SQLAlchemy pool not configured
- Missing async database operations
- No caching strategy

**Security Issues** (Both Stacks):
- Hardcoded credentials or API keys
- Missing input validation
- SQL injection vulnerabilities
- Insecure CORS configuration
- Missing security headers

Report findings with severity (critical/high/medium/low) and file locations.

### 6. Generate Refactoring Plan

Create prioritized plan:

**Phase 1: Critical Enterprise Compliance**:
1. Add health endpoints (stack-appropriate)
2. Configure graceful shutdown (>= 30s)
3. Add authentication to public endpoints
4. Remove hardcoded secrets -> Key Vault

**Phase 2: Stack-Specific Best Practices**:

*Spring Boot*:
1. Convert field injection -> constructor injection
2. Add `@RestControllerAdvice` with ProblemDetail
3. Configure profile-based settings
4. Secure actuator endpoints
5. Add `@ConfigurationProperties` validation
6. Add Flyway migrations

*FastAPI*:
1. Add Pydantic models for all inputs
2. Convert sync operations -> async
3. Configure SQLAlchemy pool
4. Add structured JSON logging
5. Add Redis caching layer
6. Configure OpenTelemetry

**Phase 3: DevOps Compliance**:
1. Update to cookiecutter structure
2. Fix JFrog auth -> variable groups
3. Add Istio sidecar config
4. Configure resource limits
5. Add proper probes for stack

**Phase 4: Performance & Code Quality**:
1. Fix N+1 queries (EntityGraph/selectinload)
2. Add database indexes
3. Implement connection pooling
4. Add missing type hints / generics
5. Split large functions/methods

### 7. Apply Refactorings

Execute refactorings in priority order with stack-specific patterns:

**A. Health Endpoints**:

*Spring Boot*:
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      probes:
        enabled: true
```

*FastAPI*:
```python
@app.get("/monitor/liveness")
async def liveness():
    return {"status": "alive"}

@app.get("/monitor/readiness")
async def readiness():
    checks = {"database": await check_db(), "redis": await check_redis()}
    if all(checks.values()):
        return {"status": "ready", "checks": checks}
    raise HTTPException(status_code=503, detail=checks)
```

**B. Graceful Shutdown**:

*Spring Boot*:
```yaml
server:
  shutdown: graceful
spring.lifecycle:
  timeout-per-shutdown-phase: 45s
```

*FastAPI*:
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
```

**C. Error Handling**:

*Spring Boot*:
```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ConstraintViolationException.class)
    public ProblemDetail handleValidation(ConstraintViolationException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.BAD_REQUEST, ex.getMessage());
        problem.setTitle("Validation Error");
        return problem;
    }
}
```

*FastAPI*:
```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "type": "validation_error"}
    )
```

**D. Constructor Injection (Spring Boot)**:
```java
// BEFORE: Field injection
@Service
public class OrderService {
    @Autowired
    private UserRepository userRepo;
}

// AFTER: Constructor injection
@Service
public class OrderService {
    private final UserRepository userRepo;

    public OrderService(UserRepository userRepo) {
        this.userRepo = userRepo;
    }
}
```

**E. Async Conversion (FastAPI)**:
```python
# BEFORE: Synchronous blocking
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user

# AFTER: Async operations
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
```

### 8. Update Infrastructure Configuration

Update Helm charts and Docker configuration:
- Adjust probe paths for detected stack
- Configure resource limits (Java needs more memory)
- Add workload identity labels
- Add Istio annotations
- Update environment variables

### 9. Validate Refactorings

// turbo
Run validation checks based on stack:

*Java*:
- `./mvnw test` - Run test suite
- `./mvnw checkstyle:check` - Code style
- `./mvnw spotbugs:check` - Static analysis

*Python*:
- `poetry run pytest` - Run test suite
- `poetry run ruff check .` - Lint code
- `poetry run black --check .` - Check formatting
- `poetry run mypy .` - Type checking

### 10. Generate Refactoring Report

```
🔧 Enterprise Microservice Refactoring Report

📍 Technology Stack: <Java/Spring Boot | Python/FastAPI>

📊 Issues Identified: <count>
   Critical: <count>
   High: <count>
   Medium: <count>
   Low: <count>

✅ Refactorings Applied:
   Enterprise Compliance: <count> fixes
   Stack Best Practices: <count> fixes
   DevOps Compliance: <count> fixes
   Performance: <count> optimizations
   Code Quality: <count> improvements

🏢 Enterprise Compliance:
   ✓ Health endpoints configured
   ✓ Graceful shutdown >= 30s
   ✓ Authentication on public endpoints
   ✓ Secrets in Key Vault

📦 Stack-Specific Improvements:
   <Stack-specific items>

✅ Next Steps:
   1. Review refactored code
   2. Run full test suite
   3. Deploy to NPRD for validation
   4. Monitor performance metrics
```

## Error Handling

**Breaking Changes**: Identify backward compatibility issues and provide migration guide.

**Test Failures**: Fix tests to match refactored code or identify regression issues.

**Mixed Stack**: If project uses both Java and Python, address each separately.

## Examples

**Example 1**: `/refactor-enterprise-microservice Add health checks and graceful shutdown to Spring Boot order-service`

**Example 2**: `/refactor-enterprise-microservice Convert FastAPI user-service to async with proper connection pooling`

**Example 3**: `/refactor-enterprise-microservice Apply enterprise security standards to Java payment-service`

**Example 4**: `/refactor-enterprise-microservice Migrate Spring Boot service from field injection to constructor injection`

## References

Constitution: `${ARCHETYPES_BASEDIR}/enterprise-microservice/enterprise-microservice-constitution.md`
Backend-Only Constitution: `${ARCHETYPES_BASEDIR}/backend-only/backend-only-constitution.md`
