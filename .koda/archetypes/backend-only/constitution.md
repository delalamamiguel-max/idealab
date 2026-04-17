# Backend Only Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the **Backend Only** archetype, which generates production-ready backend API services with FastAPI, Poetry, Docker, Helm, and Azure DevOps CI/CD.

**Scope:** Backend services only (APIs, workers, jobs, shared packages, Helm charts, CI/CD pipelines). The agent must not introduce frontend, UI, or client-side changes.

**Source**: Created for AskTranscripts Platform aligned with AT&T DevOps cookiecutter standards

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code or design that violates these rules:

### Security
- ✘ **No hardcoded secrets**: Do not include API keys, credentials, tokens, or secrets directly in code
- ✘ **No JFrog tokens in code**: JFrog authentication must use Azure DevOps variable groups only
- ✘ **No plaintext password storage**: Never store passwords or secrets without strong hashing (Argon2id or bcrypt)
- ✘ **No logging of secrets or PII**: Do not log tokens, passwords, SSNs, credit card numbers, or access keys
- ✘ **No eval/exec on user data**: Prohibit `eval`, `exec`, or dynamic code execution on user-influenced data
- ✘ **No deprecated cryptography**: Disallow MD5, SHA1, unsalted hashes; use AES-256-GCM, SHA-256, TLS 1.2+
- ✘ **No SQL injection**: Do not construct SQL queries with string concatenation; use parameterized queries
- ✘ **No PII exposure in errors**: Errors must not leak user data, stack traces, or internal paths in production

### Infrastructure & DevOps
- ✘ **No non-cookiecutter structure**: Must follow AT&T DevOps cookiecutter template structure
- ✘ **No public endpoints**: Resources must be restricted to AT&T proxy CIDRs
- ✘ **No missing private endpoints**: Private endpoints must be configured for Azure resources
- ✘ **No Istio sidecar disabled**: Istio sidecar must be enabled for AKS deployments
- ✘ **No missing workload identity**: Workload identity must be configured for Key Vault access
- ✘ **No root containers**: Docker containers must run as non-root user
- ✘ **No missing resource limits**: Kubernetes deployments must specify CPU/memory requests and limits

### Code Quality
- ✘ **No incompatible dependency versions**: Verify compatibility (especially Pydantic + SQLAlchemy combinations)
- ✘ **No ambiguous ORM joins**: Do not use `.join()` without explicit ON conditions in SQLAlchemy
- ✘ **No undefined relationship overlaps**: Declare `overlaps` parameter for multiple relationships on same FK
- ✘ **No silent error swallowing**: Disallow catching exceptions without logging structured diagnostics
- ✘ **No unbounded queries**: Always enforce server-side limits and pagination

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

### Project Structure (Monorepo)
- ✔ **Module separation**: Separate api/, worker/, jobs/, shared/ modules
- ✔ **Shared package**: Database models, Pydantic schemas, and utilities in shared/ module
- ✔ **Path-based dependencies**: Use `path = "../shared/"` for local module dependencies
- ✔ **Environment variable prefix**: Use consistent `{APP_ACRONYM}_` prefix for all env vars

### FastAPI Application
- ✔ **Pydantic settings**: Use `pydantic_settings.BaseSettings` for typed configuration
- ✔ **Input validation**: Use Pydantic models for all request/response validation
- ✔ **CORS configuration**: Configure CORS with specific allowed origins
- ✔ **API versioning**: Version APIs with `/api/v1/` prefix
- ✔ **Health endpoints**: Provide `/monitor/liveness` and `/monitor/readiness` endpoints
- ✔ **Structured JSON logging**: Use correlation/trace IDs for each request
- ✔ **Standard error envelope**: Return `{error:{code,message,details,trace_id}}`
- ✔ **Dependency injection**: Use FastAPI DI for services instead of global singletons

### Database & ORM
- ✔ **Async drivers**: Use asyncpg for PostgreSQL async operations
- ✔ **Connection pooling**: Configure pool sizes and timeouts
- ✔ **Explicit join conditions**: Always specify ON clause: `.outerjoin(Model, Model.fk == Other.pk)`
- ✔ **Alembic migrations**: Database migrations in shared/alembic/
- ✔ **Reserved keyword avoidance**: Prefix columns to avoid ORM conflicts (e.g., `workflow_metadata` not `metadata`)

### Observability
- ✔ **OpenTelemetry tracing**: Instrument requests, DB calls, and external HTTP clients
- ✔ **Azure Monitor integration**: Configure `azure-monitor-opentelemetry` when connection string provided
- ✔ **OTEL resource attributes**: Set `service.namespace` and `service.instance.id`
- ✔ **Structured logging**: JSON format with trace correlation

### Docker & Containers
- ✔ **Multi-stage builds**: Use builder stage for dependencies, slim runtime stage
- ✔ **Non-root user**: Create and use `appuser:appgroup` with UID 1000
- ✔ **JFrog auth cleanup**: Unset JFrog credentials after poetry install in same RUN layer
- ✔ **Base images**: Use `cerebroacr.azurecr.io/aaa/python-poetry:3.11` base images

### Helm & Kubernetes
- ✔ **Workload identity**: Configure `azure.workload.identity/use: "true"` label
- ✔ **Service account**: Use dedicated service account for workload identity
- ✔ **Probes configured**: Startup, liveness, and readiness probes for all deployments
- ✔ **Resource limits**: CPU/memory requests and limits for all containers
- ✔ **Secret provider class**: Use CSI driver for Key Vault secret mounting
- ✔ **Istio virtual service**: Configure for service mesh routing
- ✔ **Environment-specific values**: Separate nprdValues.yaml, stageValues.yaml, prodValues.yaml

### CI/CD Pipeline
- ✔ **Proxy configuration**: Set HTTP_PROXY/HTTPS_PROXY for AT&T network
- ✔ **JFrog via variable groups**: Use `$(jfrog-mechid)` and `$(jfrog-token)` from ADO
- ✔ **Coverage reports**: Generate and publish coverage XML
- ✔ **Path replacement**: Fix absolute paths in coverage reports for ADO display
- ✔ **Credential cleanup**: Always unset JFrog auth in `condition: always()` step

### Python Dependencies
- ✔ **Poetry for management**: Use pyproject.toml with Poetry
- ✔ **Version pinning**: Pin production dependencies to specific versions
- ✔ **JFrog source**: Configure `aaa-pypi-proxy` as primary source
- ✔ **Segregated dev/test**: Maintain separate dependency groups
- ✔ **Compatible combinations**:
  - FastAPI 0.110.x + Pydantic 2.9.x + SQLAlchemy 2.0.35+ (Recommended)
  - Avoid: Pydantic 2.11+ with SQLAlchemy < 2.0.35

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

### Code Quality
- ➜ **Type hints**: Full type annotations for all functions
- ➜ **Docstrings**: Google-style docstrings for public APIs
- ➜ **Function size**: Keep functions under 50 lines
- ➜ **Ruff linting**: Configure ruff for linting and formatting

### API Design
- ➜ **RESTful conventions**: Standard HTTP methods and status codes
- ➜ **Pagination**: Paginate list endpoints with limit/offset
- ➜ **OpenAPI docs**: Auto-generate Swagger/OpenAPI documentation
- ➜ **Rate limiting headers**: Expose `X-RateLimit-*` headers

### Performance
- ➜ **Async endpoints**: Use async/await for I/O-bound operations
- ➜ **Query optimization**: Monitor slow queries (>200ms) and add indices
- ➜ **Connection pooling**: Configure appropriate pool sizes for load
- ➜ **Circuit breakers**: Apply timeouts and fallback logic for external services

### Testing
- ➜ **Unit tests**: pytest with >80% coverage target
- ➜ **Integration tests**: Test with real database in CI
- ➜ **API tests**: Use httpx for async endpoint testing
- ➜ **Performance smoke tests**: Basic latency checks for key endpoints

### Developer Experience
- ➜ **README documentation**: Quick-start guide with common commands
- ➜ **Architecture docs**: System overview and module interactions
- ➜ **Deployment guide**: Helm deployment and Key Vault setup instructions

## IV. SQLAlchemy Reserved Attributes

Never use as column names:
- `metadata`, `query`, `mapper`, `session`, `bind`
- `__tablename__`, `__table__`, `__mapper__`, `_sa_instance_state`

Use prefixed alternatives:
- `entity_metadata`, `workflow_metadata`, `search_query`, `user_session`

**Version**: 1.0.0
**Last Updated**: 2026-01-21
**Source**: AskTranscripts Platform / AT&T DevOps Standards
