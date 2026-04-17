---
description: Generate comprehensive documentation for backend API services with deployment and architecture guides (Backend Only)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype backend_only` and parse for ENV_VALID.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: project/service to document, target audience (developers/operators/stakeholders), documentation scope (API only/full system/deployment guide). Request clarification if incomplete.

### 4. Analyze Project Structure

Scan project to identify:
- API modules and endpoints
- Database models and schemas
- Background workers and jobs
- Helm charts and deployment configs
- CI/CD pipelines
- Dependencies and integrations

### 5. Generate API Documentation

**A. README.md** - Project Overview:
```markdown
# {Project Name} API

## Overview
{Brief description of the service and its purpose}

## Architecture
- **Framework**: FastAPI {version}
- **Language**: Python {version}
- **Package Manager**: Poetry
- **Database**: PostgreSQL / Redis
- **Deployment**: AKS via Helm
- **CI/CD**: Azure DevOps

## Quick Start

### Prerequisites
- Python 3.11+
- Poetry 1.7+
- Docker (for local development)
- Access to AT&T VPN and Azure resources

### Local Development Setup

1. Clone repository:
   ```bash
   git clone <repo-url>
   cd {project-name}
   ```

2. Install dependencies:
   ```bash
   cd {app_acronym}-api
   poetry install
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with local configuration
   ```

4. Run database migrations:
   ```bash
   poetry run alembic upgrade head
   ```

5. Start development server:
   ```bash
   poetry run uvicorn {app_acronym}_api.main:app --reload --port 8000
   ```

6. Access API documentation:
   - Swagger UI: http://localhost:8000/api/v1/docs
   - ReDoc: http://localhost:8000/api/v1/redoc

## Project Structure

```
{app_acronym}-api/
├── {app_acronym}_api/
│   ├── api/v1/              # API endpoints
│   ├── core/                # Configuration and utilities
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic
├── tests/                   # Test suite
├── Dockerfile               # Container definition
├── pyproject.toml           # Poetry dependencies
└── pipeline.yaml            # ADO CI/CD pipeline
```

## Available Scripts

- `poetry run uvicorn {app_acronym}_api.main:app --reload` - Start dev server
- `poetry run pytest` - Run test suite
- `poetry run pytest --cov` - Run tests with coverage
- `poetry run black .` - Format code
- `poetry run ruff check .` - Lint code
- `poetry run alembic revision --autogenerate -m "message"` - Create migration
- `poetry run alembic upgrade head` - Apply migrations

## Environment Variables

All environment variables use the `{APP_ACRONYM}_` prefix:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `{APP_ACRONYM}_ENV` | Environment (nprd/stage/prod) | Yes | nprd |
| `{APP_ACRONYM}_DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `{APP_ACRONYM}_REDIS_HOST` | Redis host | No | - |
| `{APP_ACRONYM}_REDIS_PASSWORD` | Redis password (from Key Vault) | No | - |
| `{APP_ACRONYM}_SECRET_KEY` | JWT secret (from Key Vault) | Yes | - |

## Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov={app_acronym}_api --cov-report=html

# Run specific test file
poetry run pytest tests/unit/test_users.py

# Run integration tests only
poetry run pytest tests/integration/
```

## Contributing

1. Create feature branch from `develop`
2. Make changes following code style guidelines
3. Add tests for new functionality
4. Run linting and tests locally
5. Submit pull request to `develop`

## License

Internal AT&T project - All rights reserved
```

**B. docs/API.md** - API Reference:
```markdown
# API Documentation

## Base URL

- **NPRD**: `https://aaa.dev.att.com/{app_acronym}/api`
- **Stage**: `https://aaa.stage.att.com/{app_acronym}/api`
- **Prod**: `https://aaa.web.att.com/{app_acronym}/api`

## Authentication

All endpoints require Bearer token authentication:

```bash
Authorization: Bearer <jwt_token>
```

Tokens are obtained via Entra ID authentication.

## Endpoints

### Health Checks

#### GET /monitor/liveness
Check if service is alive.

**Response**: 200 OK
```json
{
  "status": "alive"
}
```

#### GET /monitor/readiness
Check if service is ready to accept traffic.

**Response**: 200 OK
```json
{
  "status": "ready",
  "checks": {
    "database": true,
    "redis": true
  }
}
```

### Users

#### GET /api/v1/users
List all users with pagination.

**Query Parameters**:
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)

**Response**: 200 OK
```json
{
  "items": [
    {
      "id": 1,
      "email": "user@att.com",
      "name": "John Doe",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 150,
  "skip": 0,
  "limit": 100
}
```

#### POST /api/v1/users
Create a new user.

**Request Body**:
```json
{
  "email": "user@att.com",
  "name": "John Doe",
  "password": "SecurePass123!"
}
```

**Response**: 201 Created
```json
{
  "id": 1,
  "email": "user@att.com",
  "name": "John Doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input data
- `409 Conflict`: User already exists
- `500 Internal Server Error`: Server error

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Rate Limiting

- **Rate**: 1000 requests per minute per IP
- **Header**: `X-RateLimit-Remaining` shows remaining requests

## OpenAPI Specification

Interactive API documentation available at:
- Swagger UI: `{base_url}/docs`
- ReDoc: `{base_url}/redoc`
- OpenAPI JSON: `{base_url}/openapi.json`
```

### 6. Generate Deployment Documentation

**docs/DEPLOYMENT.md** - Deployment Guide:
```markdown
# Deployment Guide

## Overview

This service is deployed to Azure Kubernetes Service (AKS) using Helm charts and Azure DevOps pipelines.

## Environments

| Environment | Subscription | Namespace | URL |
|-------------|--------------|-----------|-----|
| NPRD | ACC-NPRD-30176-Insights-Engine | {app_acronym}-nprd | aaa.dev.att.com/{app_acronym} |
| Stage | ACC-NPRD-30176-Insights-Engine | {app_acronym}-stage | aaa.stage.att.com/{app_acronym} |
| Prod | ACC-PROD-30176-Insights-Engine | {app_acronym}-prod | aaa.web.att.com/{app_acronym} |

## Prerequisites

### Infrastructure Setup

1. **Terraform Resources** (in infrastructure repo):
   - Key Vault: `{app_acronym}-eastus2-{env}-kv`
   - PostgreSQL: `{app_acronym}-eastus2-{env}-postgres`
   - Redis: `{app_acronym}-eastus2-{env}-redis`
   - Managed Identity: `{app_acronym}-eastus2-{env}-mi`
   - AKS Namespace: `{app_acronym}-{env}`

2. **Key Vault Secrets**:
   - `{app_acronym}-secret-key`: JWT signing key
   - `{app_acronym}-database-password`: PostgreSQL password
   - `{app_acronym}-redis-password`: Redis password

3. **Azure DevOps Setup**:
   - Variable group: `aaa-jfrog-credentials`
   - Service connection to AKS cluster
   - Container registry access

## Deployment Process

### Automatic Deployment (via Pipeline)

1. **NPRD Deployment**:
   - Trigger: Push to `develop` branch
   - Pipeline: Automatically runs build and deploy
   - Approval: Not required

2. **Stage Deployment**:
   - Trigger: Push to `main` branch
   - Pipeline: Automatically runs build and deploy
   - Approval: Required from team lead

3. **Production Deployment**:
   - Trigger: Manual pipeline run
   - Pipeline: Requires production approval
   - Approval: Required from manager + change request

### Manual Deployment (via Helm)

```bash
# Set context
kubectl config use-context ie-eastus2-nprd-aks

# Deploy/upgrade
helm upgrade --install {app_acronym}-api ./helm/{app_name} \
  --namespace {app_acronym}-nprd \
  --set image.version=<build-id> \
  --set env=nprd \
  --values helm/{app_name}/values-nprd.yaml

# Check deployment status
kubectl rollout status deployment/{app_acronym}-api -n {app_acronym}-nprd

# View pods
kubectl get pods -n {app_acronym}-nprd

# Check logs
kubectl logs -f deployment/{app_acronym}-api -n {app_acronym}-nprd
```

## Helm Configuration

### Values Files

- `values.yaml`: Default NPRD values
- `values-stage.yaml`: Stage overrides
- `values-prod.yaml`: Production overrides

### Key Configuration

```yaml
# Resource limits
api:
  replicas: 2
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi

# Autoscaling (production)
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

## Monitoring and Observability

### Application Insights

- **NPRD**: `{app_acronym}-eastus2-nprd-ai`
- **Stage**: `{app_acronym}-eastus2-stage-ai`
- **Prod**: `{app_acronym}-eastus2-prod-ai`

### Key Metrics

- Request rate and latency (P50, P95, P99)
- Error rate (4xx, 5xx)
- Database connection pool usage
- Memory and CPU utilization

### Alerts

- API error rate > 5%
- P95 latency > 1000ms
- Pod restart count > 3 in 5 minutes
- Memory usage > 80%

## Troubleshooting

### Common Issues

**Issue**: Pod fails to start with ImagePullBackOff
- **Cause**: Image not found in registry
- **Fix**: Verify image tag and registry access

**Issue**: Pod crashes with OOMKilled
- **Cause**: Memory limit too low
- **Fix**: Increase memory limits in values.yaml

**Issue**: Cannot connect to database
- **Cause**: Key Vault secret not mounted
- **Fix**: Verify SecretProviderClass and workload identity

### Debug Commands

```bash
# Check pod status
kubectl get pods -n {app_acronym}-nprd

# View pod logs
kubectl logs <pod-name> -n {app_acronym}-nprd

# Describe pod for events
kubectl describe pod <pod-name> -n {app_acronym}-nprd

# Check secrets
kubectl get secrets -n {app_acronym}-nprd

# Port forward for local testing
kubectl port-forward <pod-name> 8000:8000 -n {app_acronym}-nprd

# Execute into pod
kubectl exec -it <pod-name> -n {app_acronym}-nprd -- /bin/bash
```

## Rollback Procedure

```bash
# View deployment history
helm history {app_acronym}-api -n {app_acronym}-nprd

# Rollback to previous version
helm rollback {app_acronym}-api -n {app_acronym}-nprd

# Rollback to specific revision
helm rollback {app_acronym}-api <revision> -n {app_acronym}-nprd
```

## Security

- All secrets stored in Azure Key Vault
- Workload identity for pod authentication
- Network policies restrict pod-to-pod communication
- Istio service mesh for mTLS
- Private endpoints for all Azure resources
- AT&T proxy CIDR restrictions applied
```

### 7. Generate Architecture Documentation

**docs/ARCHITECTURE.md** - System Architecture:
```markdown
# Architecture Documentation

## System Overview

{App Name} is a backend API service built with FastAPI, deployed on Azure Kubernetes Service (AKS), following AT&T DevOps standards and cookiecutter template structure.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Ingress (Istio)                         │
│              aaa.dev.att.com/{app_acronym}/api              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  {App} API Service                          │
│                   (FastAPI Pods)                            │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Pod 1      │  │   Pod 2      │  │   Pod N      │    │
│  │  (Replica)   │  │  (Replica)   │  │  (Replica)   │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└───────┬────────────────────┬────────────────────┬──────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  PostgreSQL  │    │    Redis     │    │  Key Vault   │
│  (Database)  │    │   (Cache)    │    │  (Secrets)   │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Components

### API Service
- **Framework**: FastAPI with async support
- **Language**: Python 3.11
- **ASGI Server**: Uvicorn
- **Replicas**: 2 (NPRD), 3 (Stage), 5 (Prod)
- **Resource Limits**: 1 CPU, 1Gi memory per pod

### Database Layer
- **Type**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0 with async support
- **Migrations**: Alembic
- **Connection Pooling**: 20 connections per pod

### Caching Layer
- **Type**: Redis 7+
- **Use Cases**: Session storage, API response caching
- **TTL**: Configurable per cache key

### Background Processing
- **Worker**: Celery with Redis broker
- **Tasks**: Async processing, scheduled jobs
- **Deployment**: Separate pod deployment

## Data Flow

### Request Flow
1. Client sends request to Ingress (Istio Gateway)
2. Istio routes to API service based on path
3. API validates JWT token
4. Business logic executes (may query DB/cache)
5. Response returned to client

### Authentication Flow
1. Client authenticates with Entra ID
2. Receives JWT token
3. Includes token in Authorization header
4. API validates token signature and expiration
5. Extracts user identity from token claims

## Design Patterns

### Repository Pattern
- Separates data access from business logic
- Each model has corresponding repository
- Enables easier testing with mocks

### Service Layer
- Business logic isolated in service classes
- Services orchestrate repositories
- Maintains single responsibility principle

### Dependency Injection
- FastAPI's dependency system for shared resources
- Database sessions injected per request
- Configuration injected via settings

## Security Architecture

### Authentication & Authorization
- JWT tokens from Entra ID
- Token validation on every request
- Role-based access control (RBAC)

### Secrets Management
- All secrets in Azure Key Vault
- Workload identity for pod access
- No secrets in code or environment variables

### Network Security
- Private endpoints for all Azure resources
- Istio service mesh for mTLS
- Network policies restrict traffic
- AT&T proxy CIDR allowlist

## Scalability

### Horizontal Scaling
- Kubernetes HPA based on CPU/memory
- Stateless API design enables easy scaling
- Load balanced across pods by Istio

### Database Scaling
- Read replicas for read-heavy workloads
- Connection pooling per pod
- Query optimization and indexing

### Caching Strategy
- Redis for frequently accessed data
- Cache-aside pattern
- TTL-based expiration

## Observability

### Logging
- Structured JSON logging
- Centralized in Application Insights
- Correlation IDs for request tracing

### Metrics
- OpenTelemetry instrumentation
- Custom metrics for business KPIs
- Exported to Application Insights

### Tracing
- Distributed tracing with OpenTelemetry
- End-to-end request visibility
- Performance bottleneck identification

## Disaster Recovery

### Backup Strategy
- PostgreSQL: Daily automated backups (35-day retention)
- Redis: Persistence enabled, daily snapshots
- Application: Stateless, no backup needed

### Recovery Procedures
- Database restore from backup
- Helm rollback for application
- Runbook for common scenarios

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.11+ |
| Framework | FastAPI | 0.104+ |
| Database | PostgreSQL | 14+ |
| Cache | Redis | 7+ |
| ORM | SQLAlchemy | 2.0+ |
| Container | Docker | 24+ |
| Orchestration | Kubernetes (AKS) | 1.28+ |
| Service Mesh | Istio | 1.20+ |
| CI/CD | Azure DevOps | - |
| IaC | Terraform | 1.6+ |
| Package Manager | Poetry | 1.7+ |
```

### 8. Generate Documentation Report

```
📚 Documentation Generated

📄 Files Created:
   ✓ README.md - Project overview and quick start
   ✓ docs/API.md - API reference and endpoints
   ✓ docs/DEPLOYMENT.md - Deployment procedures
   ✓ docs/ARCHITECTURE.md - System architecture

📊 Documentation Coverage:
   ✓ Setup instructions
   ✓ API endpoints and examples
   ✓ Environment configuration
   ✓ Deployment procedures
   ✓ Troubleshooting guides
   ✓ Architecture diagrams
   ✓ Security practices
   ✓ Monitoring and observability

🎯 Target Audiences:
   ✓ Developers (setup, API usage)
   ✓ DevOps (deployment, troubleshooting)
   ✓ Architects (system design)

✅ Next Steps:
   1. Review generated documentation
   2. Add project-specific details
   3. Update API examples with real endpoints
   4. Add architecture diagrams if needed
   5. Commit documentation to repository
```

## Error Handling

**Incomplete Project**: Request clarification on which modules to document.

**Missing Information**: Identify gaps and request details (endpoints, deployment config).

**Complex Architecture**: Break down into multiple focused documents.

## Examples

**Example 1**: `/document-backend Document the user management API`

**Example 2**: `/document-backend Create deployment guide for operations team`

**Example 3**: `/document-backend Generate architecture documentation for review`

## References

Constitution: (pre-loaded above)
DevOps Standards: `vibe_cdo/2025.12.04-DevOpsArchetypeNotes.md`
