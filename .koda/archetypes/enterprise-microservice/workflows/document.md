---
description: Generate comprehensive documentation for enterprise microservices across Java/Spring Boot and Python/FastAPI stacks (Enterprise Microservice)
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
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype enterprise-microservice` and parse for ENV_VALID.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/enterprise-microservice/enterprise-microservice-constitution.md` for documentation standards and enterprise requirements
- Read `${ARCHETYPES_BASEDIR}/backend-only/backend-only-constitution.md` for inherited documentation standards

### 3. Parse Input
Extract from $ARGUMENTS: project/service to document, technology stack (Java/Python), target audience (developers/operators/stakeholders), documentation scope (API only/full system/deployment guide). Request clarification if incomplete.

### 4. Detect Technology Stack

Identify service stack from project files:
- **Java/Spring Boot**: `pom.xml`, `build.gradle`, `application.yaml`
- **Python/FastAPI**: `pyproject.toml`, `requirements.txt`, `main.py`

### 5. Analyze Project Structure

Scan project to identify:
- API modules, endpoints, and controllers
- Database models/entities and schemas
- Background workers, scheduled tasks
- Helm charts and deployment configs
- CI/CD pipelines
- Dependencies and integrations
- Configuration profiles/settings

### 6. Generate README.md

Create project overview tailored to detected stack:

**Java/Spring Boot README**:
```markdown
# {Service Name}

## Overview
{Brief description}

## Architecture
- **Framework**: Spring Boot {version}
- **Language**: Java {version}
- **Build Tool**: Maven/Gradle
- **Database**: {database}
- **Deployment**: AKS via Helm

## Quick Start

### Prerequisites
- Java 17+ (LTS)
- Maven 3.9+ / Gradle 8+
- Docker
- AT&T VPN access

### Local Development
1. Clone repository
2. Build: `./mvnw clean install`
3. Run: `./mvnw spring-boot:run -Dspring.profiles.active=dev`
4. Access: http://localhost:8080/swagger-ui.html

## Testing
- Unit: `./mvnw test`
- Integration: `./mvnw verify -Pintegration`
- Coverage: `./mvnw jacoco:report`
```

**Python/FastAPI README**:
```markdown
# {Service Name}

## Overview
{Brief description}

## Architecture
- **Framework**: FastAPI {version}
- **Language**: Python {version}
- **Package Manager**: Poetry
- **Database**: {database}
- **Deployment**: AKS via Helm

## Quick Start

### Prerequisites
- Python 3.11+
- Poetry 1.7+
- Docker
- AT&T VPN access

### Local Development
1. Clone repository
2. Install: `cd api && poetry install`
3. Run: `poetry run uvicorn {package}_api.main:app --reload`
4. Access: http://localhost:8000/docs

## Testing
- All: `poetry run pytest`
- Coverage: `poetry run pytest --cov`
```

### 7. Generate API Documentation

**docs/API.md**:

Document all endpoints with:
- HTTP method and path
- Request/response schemas
- Authentication requirements
- Error responses
- Example curl commands

For Java/Spring Boot, reference Swagger/SpringDoc OpenAPI.
For Python/FastAPI, reference built-in `/docs` and `/redoc`.

Include:
- Base URLs per environment (NPRD, Stage, Prod)
- Authentication mechanism (Entra ID / JWT)
- Rate limiting policies
- Health check endpoints (stack-specific paths)

### 8. Generate Deployment Documentation

**docs/DEPLOYMENT.md**:

Document deployment process:
- Environment matrix (NPRD, Stage, Prod)
- Prerequisites (Terraform resources, Key Vault, ADO setup)
- Automatic deployment via pipeline (branch triggers, approvals)
- Manual deployment via Helm commands
- Helm configuration and values files
- Monitoring and observability setup
- Troubleshooting common issues
- Rollback procedures
- Security configuration

Adjust commands and paths based on stack:
- Java: `./mvnw`, `target/*.jar`, JVM flags
- Python: `poetry run`, `pyproject.toml`, Gunicorn workers

### 9. Generate Architecture Documentation

**docs/ARCHITECTURE.md**:

Document system architecture:
- Architecture diagram (ASCII art)
- Component descriptions
- Data flow (request flow, auth flow)
- Design patterns used
  - Java: Repository pattern, Service layer, DI via Spring
  - Python: Repository pattern, Service layer, DI via Depends()
- Security architecture (auth, secrets, network)
- Scalability strategy (HPA, connection pooling, caching)
- Observability setup (logging, metrics, tracing)
- Disaster recovery (backups, rollback)
- Technology stack table with versions

### 10. Generate Stack-Specific Documentation

**Java/Spring Boot Extras**:
- Spring profile configuration guide
- Spring Security configuration notes
- Actuator endpoint reference
- Database migration guide (Flyway/Liquibase)
- JVM tuning recommendations

**Python/FastAPI Extras**:
- Async best practices guide
- Pydantic model documentation
- SQLAlchemy migration guide (Alembic)
- Background task configuration
- Poetry dependency management

### 11. Generate Environment Variables Documentation

Create environment variables table:
- Variable name (with stack-appropriate prefix)
- Description
- Required / Optional
- Default value
- Source (Key Vault / Config / Pipeline)

### 12. Generate Documentation Report

```
📚 Enterprise Microservice Documentation

📍 Technology Stack: <Java/Spring Boot | Python/FastAPI>

📄 Files Created:
   ✓ README.md - Project overview and quick start
   ✓ docs/API.md - API reference and endpoints
   ✓ docs/DEPLOYMENT.md - Deployment procedures
   ✓ docs/ARCHITECTURE.md - System architecture

📊 Documentation Coverage:
   ✓ Setup instructions (stack-specific)
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
   4. Commit documentation to repository
```

## Error Handling

**Incomplete Project**: Request clarification on which modules to document.

**Unknown Stack**: Auto-detect from project files; ask user to confirm if ambiguous.

**Missing Information**: Identify gaps and request details (endpoints, config, deployment).

## Examples

**Example 1**: `/document-enterprise-microservice Document the Spring Boot order-service architecture`

**Example 2**: `/document-enterprise-microservice Create deployment guide for FastAPI notification-service`

**Example 3**: `/document-enterprise-microservice Generate full documentation for Java payment-service`

## References

Constitution: `${ARCHETYPES_BASEDIR}/enterprise-microservice/enterprise-microservice-constitution.md`
Backend-Only Constitution: `${ARCHETYPES_BASEDIR}/backend-only/backend-only-constitution.md`
