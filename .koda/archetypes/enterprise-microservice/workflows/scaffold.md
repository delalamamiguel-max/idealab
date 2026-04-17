---
description: Generate enterprise microservice with multi-stack support (Java/Spring Boot or Python/FastAPI), Helm, and cloud-native deployment (Enterprise Microservice)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR [⋯]

**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory

**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set (workflow will halt if this variable is not present in the environment)

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Environment Setup
// turbo
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype enterprise-microservice --json` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/enterprise-microservice/enterprise-microservice-constitution.md` for hard-stop rules, multi-stack patterns, and enterprise extensions
- Read `${ARCHETYPES_BASEDIR}/backend-only/backend-only-constitution.md` for inherited base rules

### 3. Parse Input
Extract from $ARGUMENTS:
- Service name and app acronym
- Technology stack (Java/Spring Boot or Python/FastAPI)
- API type (REST/GraphQL/gRPC)
- Database requirement (PostgreSQL/MySQL/MongoDB/Redis/None)
- Authentication (Entra ID/OAuth 2.0/JWT/mTLS/None)
- Messaging (Kafka/RabbitMQ/None)
- Caching (Redis/Caffeine/None)
- Background workers needed (Celery/Spring Async/None)
- Scheduled jobs/cronjobs needed
- Deployment target (AKS/Azure App Service)

Request clarification if incomplete. Default to Python/FastAPI if stack not specified.

### 4. Validate Constraints
Check against hard-stop rules (inherited from backend-only + enterprise extensions):
- ✘ Refuse if secrets would be hardcoded
- ✘ Refuse if missing health endpoints (`/health` or `/actuator/health`)
- ✘ Refuse if graceful shutdown < 30 seconds
- ✘ Refuse if public endpoints lack authentication
- ✘ Refuse if JFrog token not using variable groups
- ✘ Refuse if private endpoints not configured
- ✘ Refuse if Istio sidecar not enabled for AKS deployment
- ✘ Refuse if workload identity not configured for Key Vault access

If violated, explain clearly and suggest compliant alternative.

### 5. Generate Project Structure

#### For Python/FastAPI Stack

Create monorepo backend service following AT&T DevOps cookiecutter standards:

```
{service-name}/
├── api/                           # API module
│   ├── src/{package_prefix}_api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── settings.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── health.py
│   ├── test/
│   ├── docker/
│   │   └── start_server.sh
│   ├── Dockerfile
│   ├── pipeline.yaml
│   ├── pyproject.toml
│   └── README.md
├── shared/                        # Shared package
│   ├── src/{package_prefix}_shared/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── schemas/
│   │   └── utils/
│   ├── test/
│   ├── alembic/
│   ├── alembic.ini
│   ├── pyproject.toml
│   └── README.md
├── worker/                        # Worker module (if needed)
├── jobs/                          # Jobs module (if needed)
├── helm/{app_name}/
│   ├── templates/
│   │   ├── api/
│   │   ├── worker/
│   │   ├── jobs/
│   │   └── common/
│   ├── values/
│   │   ├── nprdValues.yaml
│   │   ├── stageValues.yaml
│   │   └── prodValues.yaml
│   ├── Chart.yaml
│   └── values.yaml
├── .gitignore
└── README.md
```

#### For Java/Spring Boot Stack

Create standard Maven/Gradle project:

```
{service-name}/
├── src/
│   ├── main/
│   │   ├── java/{package}/
│   │   │   ├── Application.java
│   │   │   ├── config/
│   │   │   │   ├── SecurityConfig.java
│   │   │   │   └── AppConfig.java
│   │   │   ├── controller/
│   │   │   │   └── HealthController.java
│   │   │   ├── service/
│   │   │   ├── repository/
│   │   │   ├── model/
│   │   │   └── exception/
│   │   │       └── GlobalExceptionHandler.java
│   │   └── resources/
│   │       ├── application.yaml
│   │       ├── application-dev.yaml
│   │       ├── application-stage.yaml
│   │       └── application-prod.yaml
│   └── test/
│       └── java/{package}/
├── docker/
│   └── Dockerfile
├── helm/{app_name}/
│   ├── templates/
│   ├── values/
│   ├── Chart.yaml
│   └── values.yaml
├── ci/
│   └── pipeline.yaml
├── pom.xml (or build.gradle)
├── .gitignore
└── README.md
```

### 6. Generate Application Code (Python/FastAPI)

If Python stack selected, generate:
- `api/src/{package_prefix}_api/main.py` - FastAPI application with CORS, OpenTelemetry, health router
- `api/src/{package_prefix}_api/settings.py` - Pydantic settings with `{APP_ACRONYM}_` prefix
- `api/src/{package_prefix}_api/routers/health.py` - Liveness and readiness endpoints
- `shared/pyproject.toml` - Shared module with SQLAlchemy, Pydantic, Alembic
- `api/pyproject.toml` - API module with FastAPI, uvicorn, gunicorn
- `api/docker/start_server.sh` - Gunicorn startup script
- `api/Dockerfile` - Multi-stage build with non-root user

Follow backend-only scaffold patterns for detailed file contents.

### 7. Generate Application Code (Java/Spring Boot)

If Java stack selected, generate:

**Application.java**:
```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

**application.yaml**:
```yaml
spring:
  application:
    name: {service-name}
  main:
    banner-mode: off
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

server:
  port: ${SERVER_PORT:8080}
  shutdown: graceful

spring.lifecycle:
  timeout-per-shutdown-phase: 45s

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true
  health:
    readinessstate:
      enabled: true
    livenessstate:
      enabled: true
```

**GlobalExceptionHandler.java**:
```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(Exception.class)
    public ProblemDetail handleException(Exception ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.INTERNAL_SERVER_ERROR, ex.getMessage());
        problem.setTitle("Internal Server Error");
        return problem;
    }
}
```

**pom.xml** with Spring Boot 3.x, Actuator, Web, Data JPA, Flyway, Micrometer dependencies.

**Dockerfile** (multi-stage):
```dockerfile
FROM eclipse-temurin:17-jdk AS builder
WORKDIR /app
COPY . .
RUN ./mvnw clean package -DskipTests

FROM eclipse-temurin:17-jre
WORKDIR /app
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser
COPY --from=builder /app/target/*.jar app.jar
USER appuser
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### 8. Generate Helm Charts

Create Helm chart with:
- Deployment with health probes (liveness, readiness, startup)
- Service (ClusterIP)
- Ingress with Istio VirtualService
- SecretProviderClass for Key Vault
- Workload identity labels
- Resource requests/limits
- Environment-specific values files (nprd, stage, prod)

Adjust probe paths based on stack:
- **Python/FastAPI**: `/monitor/liveness`, `/monitor/readiness`
- **Java/Spring Boot**: `/actuator/health/liveness`, `/actuator/health/readiness`

### 9. Generate CI/CD Pipeline

Create `ci/pipeline.yaml` with stages:
1. **Build** - Compile/install dependencies
2. **Test** - Run unit tests with >80% coverage
3. **Scan** - Security scan (SAST, dependency check)
4. **Package** - Docker image build and push
5. **Deploy** - Helm deployment to target environment

Adjust build steps based on stack:
- **Python**: Poetry install, pytest, Docker build
- **Java**: Maven/Gradle build, JUnit, Docker build

### 10. Generate Documentation

Create:
- `README.md` - Project overview, quick start, structure
- `docs/API.md` - API reference and endpoints
- `docs/DEPLOYMENT.md` - Helm deployment guide
- `docs/ARCHITECTURE.md` - System architecture diagram

### 11. Validate and Report

// turbo

**Report Completion**:
```
✅ Enterprise Microservice Scaffolded

📦 Service: {service-name}
   Stack: {Java/Spring Boot | Python/FastAPI}
   Database: {database_choice}
   Auth: {auth_choice}
   Messaging: {messaging_choice}
   Caching: {caching_choice}

📂 Project Structure:
   ├── src/ or api/             Application code
   ├── helm/{app_name}/         Helm charts
   ├── ci/                      CI/CD pipeline
   ├── docker/                  Container build
   └── docs/                    Documentation

🔒 Enterprise Compliance:
   ✓ Health endpoints configured
   ✓ Graceful shutdown >= 30s
   ✓ Authentication required
   ✓ Multi-stage Docker (non-root)
   ✓ Workload identity for Key Vault
   ✓ Istio sidecar enabled
   ✓ Resource limits configured
   ✓ OpenTelemetry instrumentation

📋 Next Steps:
   1. Update infrastructure repo Terraform
   2. Configure Key Vault secrets
   3. Install dependencies and run locally
   4. Run test suite
   5. Deploy via CI/CD pipeline
```

## Error Handling

**Hard-Stop Violations**: Explain violation, suggest compliant alternative.

**Incomplete Input**: List missing information with examples for both Java and Python stacks.

**Environment Failure**: Report missing dependencies with installation steps.

**Unsupported Stack**: If neither Java nor Python requested, explain supported stacks and suggest closest match.

## Examples

**Example 1**: `/scaffold-enterprise-microservice Create a Java Spring Boot REST API for order processing with PostgreSQL and Redis caching`

**Example 2**: `/scaffold-enterprise-microservice Build a Python FastAPI microservice with Kafka messaging and Entra ID auth`

**Example 3**: `/scaffold-enterprise-microservice Generate a Spring Boot service with OAuth 2.0, MongoDB, and scheduled cleanup jobs`

## References

Constitution: `${ARCHETYPES_BASEDIR}/enterprise-microservice/enterprise-microservice-constitution.md`
Backend-Only Constitution: `${ARCHETYPES_BASEDIR}/backend-only/backend-only-constitution.md`
