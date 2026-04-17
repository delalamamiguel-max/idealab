# Enterprise Microservice

## Overview

The **Enterprise Microservice** archetype is a universal, team-agnostic standard for building production-ready backend services. It combines industry best practices for cloud-native microservices while remaining framework and team independent. Supports both **Java/Spring Boot** and **Python/FastAPI** technology stacks.

## When to Use

- **Building new microservices** - Scaffold production-ready services with enterprise standards
- **Multi-stack teams** - Java/Spring Boot or Python/FastAPI with consistent patterns
- **Cloud-native deployments** - Kubernetes/Helm with AKS, Istio, and Key Vault
- **Refactoring existing services** - Apply enterprise guardrails to legacy services
- **Comparing approaches** - Evaluate technology stacks and deployment patterns

## Quick Start

```bash
# Scaffold a new enterprise microservice
/scaffold-enterprise-microservice "Create a Java Spring Boot order service with PostgreSQL"

# Debug a microservice issue
/debug-enterprise-microservice "Pod keeps restarting with OOMKilled in staging"

# Refactor to enterprise standards
/refactor-enterprise-microservice "Apply health checks and observability to user-service"

# Generate documentation
/document-enterprise-microservice "Document the payment-service architecture"
```

## Workflows

| Workflow | Purpose |
|----------|---------|
| `/scaffold-enterprise-microservice` | Generate new microservices with enterprise patterns |
| `/debug-enterprise-microservice` | Debug microservice failures across stacks |
| `/refactor-enterprise-microservice` | Apply enterprise standards to existing services |
| `/compare-enterprise-microservice` | Evaluate technology stacks and deployment patterns |
| `/test-enterprise-microservice` | Generate comprehensive multi-stack test suites |
| `/document-enterprise-microservice` | Create architecture and deployment documentation |

## Key Principles

1. **Guardrails, not prescriptions** - Teams choose their stack; enterprise standards apply universally
2. **Extends backend-only** - Inherits all backend-only rules plus enterprise extensions
3. **Multi-stack support** - Java/Spring Boot and Python/FastAPI first-class citizens
4. **Cloud-native by default** - Kubernetes, Helm, Istio, Key Vault built in
5. **Health-first design** - Mandatory health/readiness endpoints and graceful shutdown

## Supported Technology Stacks

### Java/Spring Boot
- Java 17+ (LTS), Spring Boot 3.x
- Maven or Gradle build
- JUnit 5, Mockito, or Spock testing
- Spring MVC or Jersey API layer
- HikariCP connection pooling, Flyway/Liquibase migrations

### Python/FastAPI
- Python 3.11+, FastAPI 0.110+
- Poetry package management
- pytest testing framework
- SQLAlchemy 2.0+ ORM
- Async-first with asyncpg

## Standard Project Structure

```
{service-name}/
├── README.md                    # Documentation with quick-start
├── .gitignore                   # Git ignore patterns
├── docker/
│   └── Dockerfile               # Multi-stage build
├── helm/                        # Kubernetes deployment
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── ci/                          # CI/CD configuration
│   └── pipeline.yaml            # Jenkins/ADO pipeline
├── docs/                        # Architecture docs
└── tests/                       # Test directory
```

## Related Archetypes

- `backend-only` - Base archetype (inherited dependency)
- `aks-devops-deployment` - AKS deployment patterns
- `container-solution-architect` - Container build best practices
- `key-vault-config-steward` - Key Vault configuration
- `microservice-cicd-architect` - CI/CD pipeline patterns
- `observability` - OpenTelemetry and monitoring

## References

- [Constitution](./enterprise-microservice-constitution.md) - Rules and guardrails
- [Changelog](./changelog.md) - Version history
