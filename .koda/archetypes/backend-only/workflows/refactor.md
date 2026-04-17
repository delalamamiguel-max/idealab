---
description: Refactor backend API to apply security, performance, and DevOps best practices (Backend Only)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype backend_only` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: target files/modules, refactoring goals (performance, security, DevOps compliance, code quality, scalability), specific issues to address. Request clarification if incomplete.

### 4. Analyze Existing Code

Scan target backend service for issues:

**DevOps Compliance**:
- Not following cookiecutter structure
- JFrog auth not using variable groups
- Missing workload identity configuration
- Istio sidecar not configured
- Missing resource limits/requests
- Missing liveness/readiness probes
- Environment variables not using proper prefix
- Secrets hardcoded instead of Key Vault

**Security Issues**:
- Hardcoded credentials or API keys
- Missing input validation (Pydantic)
- SQL injection vulnerabilities
- Missing authentication/authorization
- Weak password hashing
- Missing rate limiting
- Insecure CORS configuration
- Missing security headers
- Unencrypted sensitive data

**Performance Issues**:
- N+1 query problems
- Missing database indexes
- No connection pooling
- Missing caching strategy
- Synchronous blocking operations
- Memory leaks
- Inefficient algorithms
- Large payload responses

**Code Quality**:
- Missing type hints
- Large functions (>50 lines)
- Duplicate code
- Poor error handling
- Missing logging
- No structured logging
- Tight coupling
- Missing tests

**Scalability Issues**:
- Stateful design
- Single point of failure
- No horizontal scaling support
- Missing async operations
- Resource exhaustion risks

Report findings with severity (critical/high/medium/low) and file locations.

### 5. Generate Refactoring Plan

Create prioritized plan:

**Phase 1: Critical Security & Compliance** (Hard-stop violations):
1. Remove hardcoded secrets → Key Vault integration
2. Add input validation → Pydantic models
3. Fix SQL injection → parameterized queries
4. Configure workload identity → Helm charts
5. Add authentication → JWT validation
6. Configure resource limits → Helm values

**Phase 2: DevOps Compliance**:
1. Restructure to cookiecutter pattern
2. Update JFrog auth → ADO variable groups
3. Add Istio sidecar config → Helm annotations
4. Add probes → health check endpoints
5. Fix environment variable naming → {APP_ACRONYM}_ prefix
6. Update Docker build → multi-stage with secrets

**Phase 3: Performance Optimization**:
1. Fix N+1 queries → eager loading
2. Add database indexes → migration files
3. Implement connection pooling → SQLAlchemy config
4. Add Redis caching → cache layer
5. Convert to async → async/await patterns
6. Optimize queries → query analysis

**Phase 4: Code Quality**:
1. Add type hints → full typing coverage
2. Split large functions → smaller focused functions
3. Extract duplicate code → shared utilities
4. Improve error handling → custom exceptions
5. Add structured logging → JSON logs
6. Decouple components → dependency injection

### 6. Apply Refactorings

Execute refactorings in priority order:

**A. Security Refactorings**:
```python
# BEFORE: Hardcoded database password
DATABASE_URL = "postgresql://user:password123@localhost/db"

# AFTER: From Key Vault via environment variable
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # From Key Vault secret
    
    class Config:
        env_prefix = "APPNAME_"

settings = Settings()
```

```python
# BEFORE: No input validation
@app.post("/users")
def create_user(data: dict):
    db.execute(f"INSERT INTO users VALUES ({data['name']})")

# AFTER: Pydantic validation
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8)

@app.post("/users")
async def create_user(user: UserCreate):
    hashed_password = hash_password(user.password)
    result = await db.execute(
        "INSERT INTO users (email, name, password) VALUES (:email, :name, :password)",
        {"email": user.email, "name": user.name, "password": hashed_password}
    )
    return result
```

**B. DevOps Compliance Refactorings**:
```python
# BEFORE: Generic environment variables
API_PORT = os.getenv("PORT", 8000)
REDIS_HOST = os.getenv("REDIS_HOST")

# AFTER: Prefixed environment variables
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_PORT: int = 8000
    REDIS_HOST: str
    REDIS_PASSWORD: str  # From Key Vault
    
    class Config:
        env_prefix = "APPNAME_"  # All vars prefixed

settings = Settings()
```

```yaml
# BEFORE: Missing resource limits in Helm
spec:
  containers:
    - name: api
      image: myapp:latest

# AFTER: Resource limits configured
spec:
  containers:
    - name: api
      image: myapp:latest
      resources:
        requests:
          cpu: 500m
          memory: 512Mi
        limits:
          cpu: 1000m
          memory: 1Gi
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
```

**C. Performance Refactorings**:
```python
# BEFORE: N+1 query problem
users = db.query(User).all()
for user in users:
    orders = db.query(Order).filter(Order.user_id == user.id).all()

# AFTER: Eager loading
from sqlalchemy.orm import selectinload

users = db.query(User).options(selectinload(User.orders)).all()
```

```python
# BEFORE: Missing indexes
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    created_at = Column(DateTime)

# AFTER: Indexes added
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, index=True, unique=True)
    created_at = Column(DateTime, index=True)
    
    __table_args__ = (
        Index('idx_user_email_created', 'email', 'created_at'),
    )
```

```python
# BEFORE: No caching
@app.get("/config")
async def get_config():
    config = await db.query(Config).all()
    return config

# AFTER: Redis caching
import redis
from functools import wraps

redis_client = redis.Redis(host=settings.REDIS_HOST)

def cache(ttl: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@app.get("/config")
@cache(ttl=600)
async def get_config():
    config = await db.query(Config).all()
    return config
```

**D. Async Conversion**:
```python
# BEFORE: Synchronous blocking operations
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    external_data = requests.get(f"https://api.example.com/users/{user_id}")
    return {"user": user, "external": external_data.json()}

# AFTER: Async operations
import httpx

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.id == user_id))
    
    async with httpx.AsyncClient() as client:
        external_data = await client.get(
            f"https://api.example.com/users/{user_id}",
            timeout=5.0
        )
    
    return {"user": user, "external": external_data.json()}
```

**E. Code Quality Refactorings**:
```python
# BEFORE: Missing type hints
def process_order(order_id, user_id):
    order = get_order(order_id)
    user = get_user(user_id)
    return calculate_total(order, user)

# AFTER: Full type hints
from typing import Optional

def process_order(order_id: int, user_id: int) -> Optional[OrderTotal]:
    order: Order = get_order(order_id)
    user: User = get_user(user_id)
    return calculate_total(order, user)
```

```python
# BEFORE: Poor error handling
@app.post("/orders")
def create_order(order: OrderCreate):
    result = db.execute("INSERT INTO orders ...")
    return result

# AFTER: Comprehensive error handling
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class OrderCreationError(Exception):
    pass

@app.post("/orders")
async def create_order(order: OrderCreate):
    try:
        logger.info(f"Creating order for user {order.user_id}")
        result = await order_service.create(order)
        logger.info(f"Order created: {result.id}")
        return result
    except IntegrityError as e:
        logger.error(f"Database constraint violation: {e}")
        raise HTTPException(status_code=400, detail="Invalid order data")
    except OrderCreationError as e:
        logger.error(f"Order creation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to create order")
    except Exception as e:
        logger.exception("Unexpected error creating order")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### 7. Add Missing Features

Implement missing mandatory patterns:

**OpenTelemetry Instrumentation**:
```python
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

tracer = trace.get_tracer(__name__)

@app.get("/users")
async def get_users():
    with tracer.start_as_current_span("fetch_users"):
        users = await db.query(User).all()
        return users
```

**Health Check Endpoints**:
```python
@app.get("/monitor/liveness")
async def liveness():
    return {"status": "alive"}

@app.get("/monitor/readiness")
async def readiness():
    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
    }
    
    if all(checks.values()):
        return {"status": "ready", "checks": checks}
    else:
        raise HTTPException(status_code=503, detail=checks)

async def check_database() -> bool:
    try:
        await db.execute("SELECT 1")
        return True
    except Exception:
        return False
```

**Structured Logging**:
```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logging.root.addHandler(handler)
    logging.root.setLevel(logging.INFO)
```

### 8. Update Infrastructure Configuration

**Dockerfile Multi-Stage Build**:
```dockerfile
# BEFORE: Single stage, token in layer
FROM python:3.11
COPY . .
RUN pip install poetry && poetry install

# AFTER: Multi-stage with secret mount
FROM cerebroacr.azurecr.io/aaa/python-poetry:3.11 AS builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN --mount=type=secret,id=jfrog_token \
    JFROG_TOKEN=$(cat /run/secrets/jfrog_token) && \
    python -m poetry config repositories.aaa-py-stage <url> && \
    python -m poetry config http-basic.aaa-py-stage _token $JFROG_TOKEN && \
    poetry install --no-root --only main && \
    poetry config --unset http-basic.aaa-py-stage

FROM cerebroacr.azurecr.io/aaa/python-poetry-slim:3.11
WORKDIR /app
RUN groupadd -r appuser && useradd -r -g appuser appuser
COPY --from=builder /app/.venv /app/.venv
COPY app_api ./app_api
USER appuser
CMD ["uvicorn", "app_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Helm Chart Updates**:
```yaml
# Add workload identity labels
metadata:
  labels:
    azure.workload.identity/use: "true"

# Add Istio sidecar annotation
annotations:
  sidecar.istio.io/inject: "true"

# Add probes
livenessProbe:
  httpGet:
    path: /monitor/liveness
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /monitor/readiness
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 15
```

### 9. Validate Refactorings

Run validation checks:
- `poetry run pytest` - Run test suite
- `poetry run ruff check .` - Lint code
- `poetry run black --check .` - Check formatting
- `poetry run mypy .` - Type checking

### 10. Generate Refactoring Report

```
🔧 Refactoring Report

📊 Issues Identified: <count>
   Critical: <count>
   High: <count>
   Medium: <count>
   Low: <count>

✅ Refactorings Applied:
   Security: <count> fixes
   DevOps Compliance: <count> fixes
   Performance: <count> optimizations
   Code Quality: <count> improvements

🔒 Security Improvements:
   ✓ Removed hardcoded secrets
   ✓ Added input validation
   ✓ Fixed SQL injection risks
   ✓ Configured Key Vault integration
   ✓ Added authentication

📦 DevOps Compliance:
   ✓ Cookiecutter structure applied
   ✓ JFrog auth via variable groups
   ✓ Workload identity configured
   ✓ Resource limits set
   ✓ Probes configured
   ✓ Environment variable prefix added

⚡ Performance Gains:
   ✓ Fixed N+1 queries
   ✓ Added database indexes
   ✓ Implemented caching
   ✓ Converted to async
   ✓ Optimized queries

📈 Metrics:
   Before: <baseline metrics>
   After: <improved metrics>
   Improvement: <percentage>

✅ Next Steps:
   1. Review refactored code
   2. Run full test suite
   3. Deploy to NPRD for validation
   4. Monitor performance metrics
   5. Update documentation
```

## Error Handling

**Breaking Changes**: Identify backward compatibility issues and provide migration guide.

**Test Failures**: Fix tests to match refactored code or identify regression issues.

**Complex Refactoring**: Break into smaller incremental changes.

## Common Refactoring Patterns

**Pattern 1: Hardcoded Secrets → Key Vault**
- Identify all hardcoded credentials
- Add to Key Vault
- Update Helm SecretProviderClass
- Use environment variables

**Pattern 2: Synchronous → Async**
- Convert database operations to async
- Use httpx for external calls
- Add async/await throughout
- Update dependencies to async versions

**Pattern 3: N+1 Queries → Eager Loading**
- Identify N+1 patterns
- Use selectinload/joinedload
- Add appropriate indexes
- Measure query performance

**Pattern 4: Missing Validation → Pydantic**
- Create Pydantic models for all inputs
- Add field validators
- Use in endpoint signatures
- Add error handling

## Examples

**Example 1**: `/refactor-backend Fix security issues in user authentication module`

**Example 2**: `/refactor-backend Optimize database queries for order processing`

**Example 3**: `/refactor-backend Apply DevOps compliance to entire backend service`

**Example 4**: `/refactor-backend Convert synchronous API to async for better performance`

## References

Constitution: (pre-loaded above)
DevOps Standards: `vibe_cdo/2025.12.04-DevOpsArchetypeNotes.md`
