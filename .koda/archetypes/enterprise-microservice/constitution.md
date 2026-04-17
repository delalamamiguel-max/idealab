# Enterprise Microservice Constitution

## Purpose

Define foundational principles and hard-stop rules for the Enterprise Microservice archetype, which provides a universal, team-agnostic standard for building production-ready backend services.

**Domain:** Cloud-native microservices, multi-stack backend development (Java/Spring Boot, Python/FastAPI)  
**Use Cases:** Building production REST APIs, event-driven services, database-backed microservices with Kubernetes deployment  
**Key Principle:** Guardrails, not prescriptions—teams choose their technology stack while adhering to universal enterprise standards.

> **Inherited Rules:** This archetype extends `backend-only`. All hard-stop rules, mandatory patterns, and preferred patterns from [backend-only-constitution.md](../backend-only/backend-only-constitution.md) are inherited and apply here. The following sections define **additional** rules specific to enterprise microservices.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code that violates:

### Health & Availability
- ✘ **No missing health endpoints**: Must expose `/health` or `/actuator/health` (Spring Boot) or `/monitor/liveness` + `/monitor/readiness` (FastAPI)
- ✘ **No graceful shutdown < 30s**: Minimum 30 seconds for graceful termination period (45s recommended)
- ✘ **No public endpoints without auth**: All production endpoints require authentication (OAuth 2.0, JWT, or mTLS)

### Multi-Stack Consistency
- ✘ **No stack without standard project structure**: Every service must include README, Dockerfile, Helm chart, CI pipeline, docs, and tests directories regardless of stack
- ✘ **No missing multi-stage Docker builds**: All Dockerfiles must use multi-stage builds with non-root runtime user
- ✘ **No unversioned schema migrations**: Database schema changes must use Flyway/Liquibase (Java) or Alembic (Python)

### Testing
- ✘ **No unit test coverage below 80%**: All services must maintain >80% unit test coverage
- ✘ **No missing contract tests**: API contracts must be validated via Pact or OpenAPI specification

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify:

### Project Structure (All Stacks)
- ✔ **Common layout**: README.md, .gitignore, docker/Dockerfile, helm/ (Chart.yaml + values.yaml + templates/), ci/pipeline.yaml, docs/, tests/
- ✔ **Java/Spring Boot layout**: `src/main/java/{package}/` with Application.java, config/, controller/, service/, repository/, model/, exception/ and `src/main/resources/application.yaml`
- ✔ **Python/FastAPI layout**: api/, shared/, worker/ (optional), jobs/ (optional) modules with pyproject.toml per module

### Health & Readiness
- ✔ **Spring Boot actuator**: Expose `/actuator/health`, `/actuator/health/liveness`, `/actuator/health/readiness`, and `/actuator/info` with probes enabled
- ✔ **FastAPI health router**: Provide `/monitor/liveness` and `/monitor/readiness` with dependency checks (database, cache)
- ✔ **Kubernetes probes**: Configure startup, liveness, and readiness probes in Helm charts with stack-appropriate paths

### Spring Boot Patterns
- ✔ **Constructor injection**: Prefer over field injection for testability; use `@Lazy` only to break circular dependencies
- ✔ **Global exception handler**: Use `@RestControllerAdvice` with `@ExceptionHandler` returning RFC 7807 `ProblemDetail`
- ✔ **Profile-based config**: Use `application-{profile}.yaml` for environment-specific settings (dev, stage, prod)
- ✔ **Fail-fast startup**: Validate required config with `@ConfigurationProperties` and `@Validated`
- ✔ **Actuator security**: Expose only `health,info,metrics,prometheus` endpoints; protect sensitive endpoints
- ✔ **HikariCP pooling**: Configure connection pool with proper sizing for target load
- ✔ **Flyway/Liquibase migrations**: Manage all schema changes with versioned migration scripts
- ✔ **N+1 prevention**: Use `@EntityGraph` or `JOIN FETCH` for relationship loading
- ✔ **Micrometer metrics**: Instrument with Micrometer for Prometheus/Grafana integration

### FastAPI Patterns
- ✔ **Pydantic settings**: Validate config with `pydantic-settings` and `{APP_ACRONYM}_` env prefix
- ✔ **Dependency injection**: Use FastAPI `Depends()` for services instead of global singletons
- ✔ **Async database**: Use `asyncpg` with SQLAlchemy async sessions and properly sized connection pools
- ✔ **Background tasks**: Use `BackgroundTasks` or Celery for async processing

### CI/CD Pipeline
- ✔ **Five-stage pipeline**: Build → Test (>80% coverage) → Scan (SAST + dependency check) → Package (Docker) → Deploy (Helm)
- ✔ **Stack-appropriate build**: Maven/Gradle for Java, Poetry for Python
- ✔ **Security scanning**: SAST and dependency vulnerability scanning in every pipeline run

### Observability
- ✔ **OpenTelemetry tracing**: Instrument requests across both stacks (Micrometer bridge for Spring Boot, `opentelemetry-instrumentation-fastapi` for FastAPI)
- ✔ **Structured logging**: JSON format with trace correlation IDs
- ✔ **Custom health indicators**: Implement downstream dependency checks (database, cache, external services)

## III. Preferred Patterns (Recommended)

The LLM **should adopt** unless user overrides:

### Spring Boot
- ➜ **Banner disabled**: `spring.main.banner-mode=off` for clean production logs
- ➜ **Lazy initialization**: Consider `spring.main.lazy-initialization=true` for faster dev starts
- ➜ **Interface-based design**: Program to interfaces, not implementations
- ➜ **Custom thread pools**: Configure `@Async` with custom `TaskExecutor` for async operations
- ➜ **Scheduled task locking**: Use ShedLock or similar for distributed scheduled task locks
- ➜ **Virtual threads**: Consider Project Loom virtual threads for I/O-bound work (Java 21+)
- ➜ **Read replicas**: Configure separate datasources for read-heavy workloads

### FastAPI
- ➜ **Response caching**: Use `fastapi-cache2` or Redis for frequently accessed data
- ➜ **Streaming responses**: Use `StreamingResponse` for large payloads
- ➜ **Async-first**: Use async/await for all I/O-bound endpoint handlers

### General
- ➜ **Cross-references**: Link related archetypes (backend-only, aks-devops-deployment, observability) in docs
- ➜ **Architecture documentation**: Include system overview diagrams and module interaction docs
- ➜ **Deployment guide**: Document Helm deployment, Key Vault setup, and environment configuration
- ➜ **API documentation**: Auto-generate OpenAPI docs (Swagger UI / SpringDoc for Java, built-in for FastAPI)
- ➜ **Integration tests**: Test with real database in CI for key paths
- ➜ **Performance smoke tests**: Basic latency checks for critical endpoints

---

## IV. Technology Stack Reference

### Java/Spring Boot

| Component | Recommended Version |
|-----------|---------------------|
| Java | 17+ (LTS) |
| Spring Boot | 3.x |
| Build Tool | Maven or Gradle |
| Testing | JUnit 5, Mockito, or Spock |
| API | Spring MVC or Jersey |

### Python/FastAPI

| Component | Recommended Version |
|-----------|---------------------|
| Python | 3.11+ |
| FastAPI | 0.110+ |
| Build Tool | Poetry or pip |
| Testing | pytest |
| ORM | SQLAlchemy 2.0+ |

---

## V. Optional Integration Patterns

Enable as needed based on service requirements:

### Authentication Options
| Option | Use Case |
|--------|----------|
| OAuth 2.0 / OIDC | Standard authentication flows |
| JWT Bearer Tokens | Stateless API authentication |
| API Keys | Service-to-service (non-sensitive) |
| mTLS | High-security services |

### Database Options
| Option | Use Case |
|--------|----------|
| PostgreSQL | Relational data, ACID transactions |
| MySQL / MariaDB | Relational data, wide adoption |
| MongoDB | Document store, flexible schema |
| Redis | Caching, session storage |
| Cassandra | High-scale, write-heavy workloads |

### Messaging Options
| Option | Use Case |
|--------|----------|
| Kafka | Event streaming, high throughput |
| RabbitMQ | Task queues, pub/sub |
| AWS SQS/SNS | Cloud-native messaging |
| NATS | Lightweight, low-latency messaging |

### Caching Options
| Option | Use Case |
|--------|----------|
| Local (Caffeine/LRU) | Single-instance, static data |
| Redis | Distributed, shared state |
| CDN | Static assets, API responses |

### Encryption Options
| Option | Use Case |
|--------|----------|
| Format-Preserving Encryption | PII protection, data masking |
| Key Vault / Secrets Manager | Secrets, certificates, key rotation |
| TLS/mTLS | Transport encryption |
| AES-256-GCM | Data-at-rest encryption |

---

## VI. CI/CD Pipeline Stages

```
┌─────────┐   ┌──────┐   ┌──────┐   ┌─────────┐   ┌────────┐
│  Build  │──▶│ Test │──▶│ Scan │──▶│ Package │──▶│ Deploy │
└─────────┘   └──────┘   └──────┘   └─────────┘   └────────┘
```

| Stage | Requirements |
|-------|--------------|
| Build | Compile, dependency resolution |
| Test | Unit tests with coverage >80% |
| Scan | Security scan (SAST, dependency check) |
| Package | Docker image build |
| Deploy | Helm deployment to Kubernetes |

---

**Version**: 1.3.0  
**Last Updated**: 2026-02-19  
**Source**: Industry best practices for cloud-native microservices  
**Dependencies**: backend-only

**Changelog:**
- v1.3.0 (2026-02-19): Reformatted to standard constitution structure (I/II/III sections with ✘/✔/➜ markers); promoted Spring Boot and FastAPI best practices into Mandatory and Preferred patterns; all validated content preserved
- v1.2.0 (2026-02-17): Added Spring Boot and FastAPI best practices sections
- v1.1.0 (2026-02-10): Added optional integration patterns and CI/CD pipeline requirements
- v1.0.0 (2026-02-10): Initial constitution with enterprise-specific rules extending backend-only
