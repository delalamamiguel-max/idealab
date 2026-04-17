---
description: Compare backend API approaches, architectures, and deployment patterns (Backend Only)
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
Extract from $ARGUMENTS: approaches to compare (Approach A vs Approach B), comparison dimensions (performance, scalability, maintainability, cost, DevOps compliance), context (team expertise, deployment target, data volume). Request clarification if incomplete.

### 4. Identify Comparison Type

Determine what is being compared:

**Architecture Comparisons**:
- Monolith vs Microservices
- REST vs GraphQL vs gRPC
- Synchronous vs Asynchronous processing
- Stateless vs Stateful services

**Technology Stack Comparisons**:
- FastAPI vs Flask vs Django
- PostgreSQL vs MongoDB vs Redis
- Celery vs RQ vs Azure Functions
- Uvicorn vs Gunicorn vs Hypercorn

**Deployment Pattern Comparisons**:
- AKS vs Azure App Service vs Container Instances
- Helm vs Terraform vs ARM templates
- Blue-Green vs Canary vs Rolling deployments
- Monorepo vs Polyrepo

**Data Storage Comparisons**:
- Relational vs NoSQL vs Cache
- SQLAlchemy vs Raw SQL vs ORM alternatives
- Connection pooling strategies
- Backup and recovery approaches

### 5. Define Evaluation Criteria

Establish dimensions for comparison:

**Technical Criteria**:
- Performance (throughput, latency, resource usage)
- Scalability (horizontal/vertical, auto-scaling)
- Reliability (uptime, fault tolerance, recovery)
- Security (authentication, authorization, encryption)
- Maintainability (code complexity, debugging)

**DevOps Criteria**:
- CI/CD pipeline complexity
- Deployment automation
- Observability (logging, metrics, tracing)
- Infrastructure as Code compatibility
- Container orchestration fit

**AT&T-Specific Criteria**:
- Cookiecutter template compatibility
- JFrog package management alignment
- Key Vault integration
- Istio service mesh compatibility
- Private endpoint requirements
- AT&T proxy CIDR restrictions
- Workload identity support

**Cost Criteria**:
- Compute costs (CPU, memory)
- Storage costs
- Network egress costs
- Licensing costs
- Operational overhead

### 6. Analyze Approach A

Evaluate first approach across all criteria:

**Example: FastAPI Monolith with PostgreSQL**

**Pros**:
- Simple deployment (single service)
- Easier debugging and tracing
- Lower operational complexity
- Faster development for small teams
- Shared database transactions
- Consistent data model

**Cons**:
- Scaling requires scaling entire app
- Single point of failure
- Tight coupling of features
- Longer deployment times
- Technology lock-in

**Performance**:
- Request latency: 10-50ms (typical)
- Throughput: 1000-5000 req/s per instance
- Database connection pooling: 20-50 connections
- Memory footprint: 256-512MB per pod

**DevOps Fit**:
- Cookiecutter: Excellent (single module)
- Helm deployment: Simple (one deployment)
- CI/CD: Fast builds and tests
- Observability: Centralized logging
- Scaling: Vertical or horizontal pod scaling

**Use Cases**:
- MVP and early-stage products
- Small to medium applications
- Team size: 1-5 developers
- Low to moderate traffic

### 7. Analyze Approach B

Evaluate second approach across same criteria:

**Example: Microservices with FastAPI + Redis + PostgreSQL**

**Pros**:
- Independent scaling per service
- Technology flexibility per service
- Isolated failures (better resilience)
- Parallel development by teams
- Easier to update individual services
- Better resource utilization

**Cons**:
- Complex deployment orchestration
- Distributed tracing required
- Network latency between services
- Data consistency challenges
- Higher operational overhead
- More infrastructure costs

**Performance**:
- Request latency: 20-100ms (with service calls)
- Throughput: Varies per service
- Inter-service communication overhead
- Memory footprint: 128-256MB per service

**DevOps Fit**:
- Cookiecutter: Good (multiple modules)
- Helm deployment: Complex (multiple charts)
- CI/CD: Parallel pipelines per service
- Observability: Distributed tracing needed
- Scaling: Granular per-service scaling

**Use Cases**:
- Large-scale applications
- High traffic with variable load patterns
- Team size: 6+ developers
- Multiple business domains

### 8. Create Comparison Matrix

Generate side-by-side comparison:

```
📊 Comparison: FastAPI Monolith vs Microservices

┌─────────────────────────┬──────────────────────┬──────────────────────┐
│ Criteria                │ Approach A (Monolith)│ Approach B (Micro)   │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ Development Speed       │ Fast ✓              │ Slower              │
│ Deployment Complexity   │ Simple ✓            │ Complex             │
│ Scalability             │ Limited              │ Excellent ✓         │
│ Fault Isolation         │ Poor                 │ Excellent ✓         │
│ Debugging               │ Easy ✓              │ Difficult           │
│ Team Autonomy           │ Low                  │ High ✓              │
│ Infrastructure Cost     │ Lower ✓             │ Higher              │
│ Operational Overhead    │ Low ✓               │ High                │
│ Technology Flexibility  │ Limited              │ High ✓              │
│ Data Consistency        │ Strong ✓            │ Eventual            │
│ Cookiecutter Fit        │ Excellent ✓         │ Good                │
│ Istio Mesh Benefit      │ Minimal              │ High ✓              │
└─────────────────────────┴──────────────────────┴──────────────────────┘

✓ = Better option for this criteria
```

### 9. Provide Implementation Examples

Show key implementation differences:

**Approach A: Monolith API Structure**
```python
# Single FastAPI app with all endpoints
from fastapi import FastAPI
from app.api.v1 import users, orders, products

app = FastAPI()
app.include_router(users.router, prefix="/api/v1/users")
app.include_router(orders.router, prefix="/api/v1/orders")
app.include_router(products.router, prefix="/api/v1/products")

# Shared database session
from app.core.database import get_db
```

**Approach B: Microservices Structure**
```python
# User Service (separate app)
from fastapi import FastAPI
app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return await user_service.get(user_id)

# Order Service (separate app, calls User Service)
import httpx

async def create_order(user_id: int, items: list):
    # Inter-service call
    user = await httpx.get(f"http://user-service/users/{user_id}")
    # Process order
```

### 10. Analyze Trade-offs

Identify key trade-offs:

**Simplicity vs Scalability**:
- Monolith: Simple to develop and deploy, limited scaling
- Microservices: Complex to manage, scales independently

**Consistency vs Availability**:
- Monolith: Strong consistency with ACID transactions
- Microservices: Eventual consistency, higher availability

**Development Speed vs Operational Maturity**:
- Monolith: Faster initial development
- Microservices: Requires mature DevOps practices

**Cost vs Performance**:
- Monolith: Lower infrastructure cost, may over-provision
- Microservices: Higher cost, optimized resource allocation

### 11. Provide Recommendations

**Recommendation Based on Context**:

**Choose Approach A (Monolith) if**:
- Team size < 5 developers
- MVP or early-stage product
- Simple business domain
- Limited DevOps resources
- Budget constraints
- Need fast time-to-market
- Traffic is predictable and moderate

**Choose Approach B (Microservices) if**:
- Team size > 6 developers
- Multiple business domains
- Variable scaling requirements
- High availability critical
- Independent deployment cycles needed
- Mature DevOps team available
- Long-term scalability priority

**Hybrid Approach (Modular Monolith)**:
- Start with well-structured monolith
- Use clear module boundaries
- Design for future extraction
- Extract to microservices when needed

### 12. DevOps Compliance Check

Validate against AT&T standards:

**Approach A Compliance**:
- ✓ Cookiecutter structure: Single module
- ✓ JFrog publishing: One package
- ✓ Helm chart: Simple deployment
- ✓ Key Vault: Single secret provider
- ✓ Workload identity: One service account
- ✓ Istio: Optional (single service)

**Approach B Compliance**:
- ✓ Cookiecutter structure: Multiple modules
- ✓ JFrog publishing: Per-service packages
- ⚠ Helm chart: Complex multi-service chart
- ⚠ Key Vault: Multiple secret providers
- ✓ Workload identity: Per-service accounts
- ✓ Istio: Required for service mesh

### 13. Generate Comparison Report

```
📋 Comparison Report: <Approach A> vs <Approach B>

🎯 Context:
   Application Type: <type>
   Expected Traffic: <volume>
   Team Size: <size>
   Timeline: <timeline>
   Budget: <constraints>

📊 Summary:
   Winner: <Approach> (by <X> criteria)
   
   Approach A Wins: <count> criteria
   Approach B Wins: <count> criteria
   Tie: <count> criteria

🏆 Recommended Approach: <Approach>

Rationale:
<Detailed explanation considering team size, traffic patterns,
DevOps maturity, budget, and AT&T compliance requirements>

⚠️ Considerations:
- <DevOps consideration>
- <Scalability consideration>
- <Cost consideration>

💰 Cost Analysis (Monthly):
   Approach A: 
   - Compute: $<X> (AKS pods)
   - Database: $<Y> (PostgreSQL)
   - Total: $<Z>
   
   Approach B:
   - Compute: $<X> (multiple services)
   - Database: $<Y> (per service)
   - Service mesh: $<Z> (Istio overhead)
   - Total: $<W>

⏱️ Development Time Estimate:
   Approach A: <X> weeks
   Approach B: <Y> weeks

🔧 DevOps Complexity:
   Approach A: Low (single pipeline)
   Approach B: High (multiple pipelines)

✅ Next Steps:
   1. <Action based on recommendation>
   2. <Infrastructure setup>
   3. <Team training if needed>
```

## Error Handling

**Insufficient Context**: Request details about team size, traffic patterns, budget, timeline.

**Incomparable Approaches**: Explain why comparison is invalid (e.g., comparing storage to compute).

**No Clear Winner**: Provide hybrid approach or phased migration strategy.

## Common Comparisons

**Comparison 1: FastAPI vs Flask**
- FastAPI: Modern, async, auto-docs, type hints, better performance
- Flask: Mature, simpler, more libraries, easier learning curve

**Comparison 2: PostgreSQL vs MongoDB**
- PostgreSQL: ACID, relational, complex queries, strong consistency
- MongoDB: Flexible schema, horizontal scaling, document model

**Comparison 3: Celery vs Azure Functions**
- Celery: More control, cheaper, self-hosted, complex setup
- Azure Functions: Serverless, auto-scaling, managed, higher cost

**Comparison 4: AKS vs App Service**
- AKS: Full control, Kubernetes ecosystem, complex, cost-effective at scale
- App Service: Managed, simpler, faster setup, higher cost per instance

## Examples

**Example 1**: `/compare-backend Compare FastAPI monolith vs microservices for order processing system`

**Example 2**: `/compare-backend Compare PostgreSQL vs Redis for session storage`

**Example 3**: `/compare-backend Compare AKS deployment vs Azure App Service for our API`

**Example 4**: `/compare-backend Compare REST vs GraphQL for mobile app backend`

## References

Constitution: (pre-loaded above)
DevOps Standards: `vibe_cdo/2025.12.04-DevOpsArchetypeNotes.md`
