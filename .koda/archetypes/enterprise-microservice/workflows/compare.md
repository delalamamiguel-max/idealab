---
description: Compare enterprise microservice technology stacks, architectures, and deployment approaches (Enterprise Microservice)
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
- Read `${ARCHETYPES_BASEDIR}/enterprise-microservice/enterprise-microservice-constitution.md` for evaluation criteria and multi-stack standards
- Read `${ARCHETYPES_BASEDIR}/backend-only/backend-only-constitution.md` for inherited evaluation criteria

### 3. Parse Input
Extract from $ARGUMENTS: approaches to compare (Approach A vs Approach B), comparison dimensions (performance, scalability, maintainability, cost, enterprise compliance), context (team expertise, deployment target, data volume). Request clarification if incomplete.

### 4. Identify Comparison Type

Determine what is being compared:

**Technology Stack Comparisons**:
- Java/Spring Boot vs Python/FastAPI
- Spring MVC vs Spring WebFlux (reactive)
- Maven vs Gradle
- JUnit 5 vs Spock
- SQLAlchemy vs Spring Data JPA

**Architecture Comparisons**:
- Monolith vs Microservices
- REST vs GraphQL vs gRPC
- Synchronous vs Event-driven
- CQRS vs Traditional CRUD

**Database Comparisons**:
- PostgreSQL vs MySQL vs MongoDB
- JPA/Hibernate vs JDBC Template vs MyBatis
- SQLAlchemy vs Raw SQL vs Tortoise ORM
- Redis vs Caffeine (local cache)

**Messaging Comparisons**:
- Kafka vs RabbitMQ
- Spring Cloud Stream vs direct client
- Celery vs Spring Async

**Deployment Comparisons**:
- AKS vs Azure App Service
- Helm vs Terraform
- Blue-Green vs Canary vs Rolling

### 5. Define Evaluation Criteria

**Technical Criteria**:
- Performance (throughput, latency, memory footprint)
- Scalability (horizontal/vertical, startup time)
- Reliability (uptime, fault tolerance, recovery)
- Developer productivity (IDE support, debugging, testing)
- Ecosystem maturity (libraries, community, documentation)

**Enterprise Criteria**:
- Health check support (Actuator vs custom endpoints)
- Graceful shutdown support
- Observability (OpenTelemetry, Micrometer, structured logging)
- Security (authentication frameworks, vulnerability scanning)
- Configuration management (profiles, environment variables)

**DevOps Criteria**:
- Container image size and startup time
- CI/CD pipeline complexity
- Deployment automation (Helm compatibility)
- Kubernetes resource requirements
- AT&T cookiecutter compatibility

**Cost Criteria**:
- Compute costs (JVM memory vs Python memory)
- Developer hiring/training costs
- Licensing costs
- Operational overhead

### 6. Analyze Approach A

Evaluate first approach across all criteria.

**Example: Java/Spring Boot**

**Pros**:
- Mature ecosystem with extensive enterprise libraries
- Strong type safety and compile-time checks
- Excellent IDE support (IntelliJ, Eclipse)
- Spring Security for comprehensive auth
- Actuator for production-ready health/metrics
- JPA/Hibernate for database abstraction
- Large talent pool

**Cons**:
- Higher memory footprint (JVM overhead)
- Slower startup time
- Verbose syntax
- Complex configuration
- Longer build times

**Performance**:
- Request latency: 5-30ms (typical, after warmup)
- Throughput: 2000-10000 req/s per instance
- Memory footprint: 512MB-1GB per pod
- Startup time: 10-30 seconds

**Enterprise Fit**:
- Health checks: Actuator (built-in)
- Graceful shutdown: Native support
- Observability: Micrometer + OpenTelemetry
- Security: Spring Security (comprehensive)

### 7. Analyze Approach B

Evaluate second approach across same criteria.

**Example: Python/FastAPI**

**Pros**:
- Faster development speed
- Lower memory footprint
- Automatic API documentation (OpenAPI)
- Async-first design
- Easy to learn
- Data science ecosystem integration

**Cons**:
- Weaker type safety (runtime vs compile-time)
- GIL limitations for CPU-bound work
- Fewer enterprise-grade libraries
- Less mature observability tooling

**Performance**:
- Request latency: 5-20ms (typical)
- Throughput: 1000-5000 req/s per instance
- Memory footprint: 128-512MB per pod
- Startup time: 2-5 seconds

**Enterprise Fit**:
- Health checks: Custom endpoints required
- Graceful shutdown: Lifespan events
- Observability: OpenTelemetry instrumentation
- Security: fastapi-azure-auth, custom middleware

### 8. Create Comparison Matrix

Generate side-by-side comparison:

```
📊 Enterprise Microservice Comparison

┌───────────────────────────┬────────────────────────┬────────────────────────┐
│ Criteria                  │ Approach A             │ Approach B             │
├───────────────────────────┼────────────────────────┼────────────────────────┤
│ Development Speed         │                        │                        │
│ Type Safety               │                        │                        │
│ Memory Footprint          │                        │                        │
│ Startup Time              │                        │                        │
│ Throughput                │                        │                        │
│ Enterprise Libraries      │                        │                        │
│ Health Checks             │                        │                        │
│ Graceful Shutdown         │                        │                        │
│ Observability             │                        │                        │
│ Security Framework        │                        │                        │
│ Testing Ecosystem         │                        │                        │
│ Container Image Size      │                        │                        │
│ CI/CD Complexity          │                        │                        │
│ Team Expertise            │                        │                        │
│ Operational Cost          │                        │                        │
└───────────────────────────┴────────────────────────┴────────────────────────┘

✓ = Better option for this criteria
```

### 9. Analyze Trade-offs

Identify key trade-offs specific to enterprise context:

**Type Safety vs Development Speed**
**Memory Cost vs Startup Time**
**Ecosystem Maturity vs Modern Patterns**
**Enterprise Library Support vs Simplicity**
**JVM Warmup vs Consistent Performance**

### 10. Provide Recommendations

**Choose Java/Spring Boot if**:
- Existing Java expertise on team
- Heavy enterprise integration needs
- Complex security requirements
- Need for compile-time safety
- Large-scale transaction processing

**Choose Python/FastAPI if**:
- Rapid development priority
- Data science/ML integration
- Memory-constrained environments
- Smaller team or startup phase
- API-first design focus

**Hybrid Approach**:
- Use both stacks for different services
- Java for core business logic
- Python for data processing / ML APIs
- Unified Helm and CI/CD patterns

### 11. Enterprise Compliance Check

Validate both approaches against enterprise hard-stop rules:
- ✓ Health endpoints: How each stack implements
- ✓ Graceful shutdown: Native vs custom
- ✓ Authentication: Framework support
- ✓ Key Vault integration: Both supported
- ✓ Helm deployment: Both compatible
- ✓ Resource limits: Stack-specific recommendations

### 12. Generate Comparison Report

```
📋 Enterprise Microservice Comparison Report

🎯 Context:
   Service Type: <type>
   Team Expertise: <Java/Python/Both>
   Performance Requirements: <volume>
   Integration Needs: <list>

📊 Summary:
   Winner: <Approach> (by <X> criteria)

🏆 Recommended Approach: <Approach>

Rationale:
<Detailed explanation considering team, performance, enterprise compliance>

⚠️ Considerations:
- <Enterprise consideration>
- <Cost consideration>
- <Team consideration>

💰 Cost Comparison (Monthly per Instance):
   Approach A: <compute + memory>
   Approach B: <compute + memory>

✅ Next Steps:
   1. <Action based on recommendation>
   2. <Team training if needed>
   3. <Prototype validation>
```

## Error Handling

**Insufficient Context**: Request details about team expertise, performance requirements, integration needs.

**Incomparable Approaches**: Explain why comparison is invalid and suggest valid alternatives.

**No Clear Winner**: Provide hybrid approach or phased adoption strategy.

## Examples

**Example 1**: `/compare-enterprise-microservice Compare Java Spring Boot vs Python FastAPI for order processing service`

**Example 2**: `/compare-enterprise-microservice Compare PostgreSQL vs MongoDB for user profile storage`

**Example 3**: `/compare-enterprise-microservice Compare Kafka vs RabbitMQ for event-driven microservice communication`

## References

Constitution: `${ARCHETYPES_BASEDIR}/enterprise-microservice/enterprise-microservice-constitution.md`
Backend-Only Constitution: `${ARCHETYPES_BASEDIR}/backend-only/backend-only-constitution.md`
