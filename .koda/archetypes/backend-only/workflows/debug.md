---
description: Debug backend API failures, deployment issues, and performance problems (Backend Only)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype backend_only` and parse for debugging tools availability.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: error description, error messages/stack traces, affected endpoints/services, steps to reproduce, environment (dev/nprd/stage/prod), pod/container logs. Request clarification if incomplete.

### 4. Categorize Error Type

Analyze error to determine category:

**API Errors**:
- HTTP 4xx client errors (validation, auth, not found)
- HTTP 5xx server errors (crashes, timeouts)
- Request timeout errors
- Rate limiting issues
- Payload size errors

**Database Errors**:
- Connection failures
- Connection pool exhaustion
- Query timeout errors
- Deadlocks and lock contention
- Migration failures
- Constraint violations

**Infrastructure Errors**:
- Pod crashes and restarts
- OOM (Out of Memory) kills
- CPU throttling
- Liveness/readiness probe failures
- Istio sidecar issues
- Key Vault access failures

**Integration Errors**:
- Redis connection failures
- External API timeouts
- Message queue failures
- Service mesh communication issues

**Deployment Errors**:
- Docker build failures
- Helm deployment failures
- Pipeline failures
- Image pull errors
- Secret mounting issues

**Performance Issues**:
- High latency
- Memory leaks
- CPU spikes
- Slow database queries
- N+1 query problems

### 5. Debug API Errors

**A. HTTP 500 Internal Server Errors**:
```python
# Common issue: Unhandled exceptions

# DEBUG APPROACH:
1. Check FastAPI logs for full stack trace
2. Identify the failing endpoint and line number
3. Add structured logging around the error
4. Check if database connection is available
5. Verify all required environment variables are set

# LOGGING ENHANCEMENT:
import logging
logger = logging.getLogger(__name__)

@app.post("/api/v1/users")
async def create_user(user: UserCreate):
    try:
        logger.info(f"Creating user: {user.email}")
        result = await user_service.create(user)
        return result
    except Exception as e:
        logger.error(f"Failed to create user: {str(e)}", exc_info=True)
        raise
```

**B. Authentication Failures**:
```python
# Common issue: Invalid JWT tokens or Entra ID misconfiguration

# DEBUG APPROACH:
1. Verify token is being sent in Authorization header
2. Check token format: "Bearer <token>"
3. Validate token expiration time
4. Verify JWT secret from Key Vault
5. Check Entra ID tenant and client ID configuration
6. Test token validation with jwt.io

# FIX:
from jose import jwt, JWTError

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=["HS256"]
        )
        return payload
    except JWTError as e:
        logger.error(f"Token validation failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
```

**C. Request Timeout Errors**:
```python
# Common issue: Long-running operations blocking requests

# DEBUG APPROACH:
1. Check if operation is CPU-bound or I/O-bound
2. Identify slow database queries
3. Check for external API calls without timeouts
4. Monitor request duration in Application Insights

# FIX: Add timeouts and async processing
import httpx
from fastapi import BackgroundTasks

async def call_external_api():
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(url)
        return response.json()

# Or use background tasks for long operations
@app.post("/process")
async def process_data(background_tasks: BackgroundTasks):
    background_tasks.add_task(long_running_task)
    return {"status": "processing"}
```

### 6. Debug Database Errors

**A. Connection Pool Exhausted**:
```python
# SYMPTOM: "QueuePool limit exceeded" or connection timeouts

# DEBUG APPROACH:
1. Check current pool size configuration
2. Monitor active connections
3. Verify connections are being closed properly
4. Check for long-running transactions

# FIX: Adjust pool settings
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=20,          # Increase from default 5
    max_overflow=10,       # Allow temporary overflow
    pool_timeout=30,       # Wait time for connection
    pool_recycle=3600,     # Recycle connections hourly
    pool_pre_ping=True,    # Verify connection before use
)

# Always use context managers
async with get_db() as db:
    result = await db.execute(query)
```

**B. Slow Queries**:
```python
# SYMPTOM: High API latency, database CPU spikes

# DEBUG APPROACH:
1. Enable SQLAlchemy query logging
2. Check PostgreSQL slow query log
3. Run EXPLAIN ANALYZE on suspect queries
4. Check for missing indexes

# FIX: Add indexes and optimize queries
# In migration file:
op.create_index('idx_user_email', 'users', ['email'])
op.create_index('idx_order_user_created', 'orders', ['user_id', 'created_at'])

# Use select_related to avoid N+1 queries
from sqlalchemy.orm import selectinload

query = select(Order).options(selectinload(Order.items))
```

**C. Deadlocks**:
```python
# SYMPTOM: "deadlock detected" in PostgreSQL logs

# DEBUG APPROACH:
1. Identify conflicting transactions
2. Check lock acquisition order
3. Review transaction isolation level

# FIX: Consistent lock ordering
# Always acquire locks in same order across transactions
async def transfer_funds(from_id: int, to_id: int, amount: float):
    # Lock accounts in consistent order (by ID)
    account_ids = sorted([from_id, to_id])
    accounts = await db.execute(
        select(Account)
        .where(Account.id.in_(account_ids))
        .with_for_update()
    )
```

### 7. Debug Infrastructure Errors

**A. Pod Crashes and OOM Kills**:
```bash
# SYMPTOM: Pod restarts frequently, "OOMKilled" status

# DEBUG APPROACH:
1. Check pod logs: kubectl logs <pod-name> -n <namespace>
2. Check previous logs: kubectl logs <pod-name> -n <namespace> --previous
3. Check resource usage: kubectl top pod <pod-name> -n <namespace>
4. Review memory limits in Helm values

# FIX: Adjust resource limits
# In helm values.yaml:
api:
  resources:
    requests:
      memory: "512Mi"    # Increase from 256Mi
    limits:
      memory: "1Gi"      # Increase from 512Mi

# Add memory profiling
import tracemalloc
tracemalloc.start()
# ... application code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
```

**B. Liveness/Readiness Probe Failures**:
```python
# SYMPTOM: Pod marked as unhealthy, traffic not routed

# DEBUG APPROACH:
1. Test health endpoints manually
2. Check if database connection is blocking probe
3. Verify probe timeout settings

# FIX: Improve health checks
@app.get("/monitor/liveness")
async def liveness():
    # Simple check - just return if app is running
    return {"status": "alive"}

@app.get("/monitor/readiness")
async def readiness():
    # Check dependencies
    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
    }
    
    if all(checks.values()):
        return {"status": "ready", "checks": checks}
    else:
        raise HTTPException(status_code=503, detail=checks)

# Adjust probe settings in Helm
readinessProbe:
  httpGet:
    path: /monitor/readiness
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 15
  timeoutSeconds: 5
  failureThreshold: 3
```

**C. Istio Sidecar Issues**:
```bash
# SYMPTOM: CronJob never completes, pod stuck terminating

# DEBUG APPROACH:
1. Check if Istio sidecar is injected
2. Verify quitquitquit trap is configured
3. Check Istio proxy logs

# FIX: Add Istio cleanup for jobs
command: ["/bin/bash", "-c"]
args:
  - |
    echo "Waiting for Istio sidecar..."
    trap "curl --max-time 2 -s -f -XPOST http://127.0.0.1:15020/quitquitquit" EXIT
    while ! curl -s -f http://127.0.0.1:15020/healthz/ready; do sleep 1; done
    echo "Ready!"
    poetry run python -m app_jobs.main
```

**D. Key Vault Access Failures**:
```bash
# SYMPTOM: "Failed to get secret" errors, pod can't start

# DEBUG APPROACH:
1. Verify workload identity is configured
2. Check service account has correct labels
3. Verify Key Vault access policies
4. Check SecretProviderClass configuration

# FIX: Verify workload identity setup
# Check pod labels:
kubectl get pod <pod-name> -n <namespace> -o yaml | grep azure.workload.identity

# Check service account:
kubectl get sa workload-identity-sa -n <namespace> -o yaml

# Verify SecretProviderClass:
kubectl get secretproviderclass -n <namespace>
kubectl describe secretproviderclass <name> -n <namespace>
```

### 8. Debug Deployment Errors

**A. Docker Build Failures**:
```bash
# SYMPTOM: Pipeline fails at Docker build step

# DEBUG APPROACH:
1. Check ADO pipeline logs for error details
2. Verify JFrog token is available
3. Test build locally with same Dockerfile
4. Check for dependency conflicts

# FIX: Common issues
# Issue 1: JFrog auth failure
RUN --mount=type=secret,id=jfrog_token \
    JFROG_TOKEN=$(cat /run/secrets/jfrog_token) && \
    python -m poetry config repositories.aaa-py-stage <url> && \
    python -m poetry config http-basic.aaa-py-stage _token $JFROG_TOKEN && \
    poetry install --no-root --only main && \
    poetry config --unset http-basic.aaa-py-stage

# Issue 2: Poetry lock file out of sync
RUN poetry lock --no-update && poetry install
```

**B. Helm Deployment Failures**:
```bash
# SYMPTOM: Helm upgrade fails, rollback triggered

# DEBUG APPROACH:
1. Check Helm release status: helm status <release> -n <namespace>
2. Check deployment events: kubectl get events -n <namespace>
3. Verify values.yaml has correct image tag
4. Check for resource conflicts

# FIX: Debug Helm deployment
# Dry-run to validate:
helm upgrade <release> ./helm/<app> \
  --dry-run --debug \
  --set image.version=<tag> \
  -n <namespace>

# Check rendered templates:
helm template <release> ./helm/<app> --set image.version=<tag>
```

### 9. Debug Performance Issues

**A. High API Latency**:
```python
# DEBUG APPROACH:
1. Enable OpenTelemetry tracing
2. Identify slow operations in Application Insights
3. Profile database queries
4. Check for N+1 query problems

# FIX: Add caching and optimize queries
from functools import lru_cache
import redis

redis_client = redis.Redis(host=settings.REDIS_HOST)

@lru_cache(maxsize=100)
def get_config(key: str):
    return settings.get(key)

# Cache expensive operations
async def get_user_with_orders(user_id: int):
    cache_key = f"user:{user_id}:orders"
    cached = redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    user = await db.execute(
        select(User)
        .options(selectinload(User.orders))
        .where(User.id == user_id)
    )
    
    redis_client.setex(cache_key, 300, json.dumps(user))
    return user
```

**B. Memory Leaks**:
```python
# SYMPTOM: Memory usage grows over time, eventually OOM

# DEBUG APPROACH:
1. Monitor memory usage in Application Insights
2. Use memory profiler to identify leaks
3. Check for unclosed connections
4. Review global variables and caches

# FIX: Proper resource cleanup
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect()
    yield
    # Shutdown
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# Clear caches periodically
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('interval', hours=1)
def clear_cache():
    cache.clear()
```

### 10. Provide Debugging Guidance

For each identified issue:

**Issue Description**: Clear explanation of the problem

**Root Cause**: Why the error occurred (code, config, infrastructure)

**Fix**: Specific changes needed with code examples

**Verification**: How to test the fix

**Prevention**: How to avoid in future (monitoring, tests, guardrails)

### 11. Generate Debug Report

```
🐛 Backend Debugging Report

📍 Error Type: <category>
📍 Severity: <critical/high/medium/low>
📍 Affected Services: <list>
📍 Environment: <dev/nprd/stage/prod>

🔍 Root Cause Analysis:
<Detailed explanation of why error occurred>

🛠️ Fixes Applied:
1. <Fix description> - <file>:<line>
2. <Configuration change> - <helm/values.yaml>
3. <Infrastructure change> - <terraform/k8s>

✅ Verification Steps:
1. Test endpoint: curl <url>
2. Check logs: kubectl logs <pod>
3. Monitor metrics: Application Insights query
4. Run tests: poetry run pytest

🚫 Prevention Measures:
- Add integration test: <test description>
- Add monitoring alert: <metric threshold>
- Update documentation: <location>
- Add validation: <where>

📊 Performance Impact:
- Before: <metric>
- After: <metric>
- Improvement: <percentage>

💡 Useful Debug Commands:
- Check pod status: kubectl get pods -n <namespace>
- View logs: kubectl logs <pod> -n <namespace> --tail=100
- Check events: kubectl get events -n <namespace> --sort-by='.lastTimestamp'
- Port forward: kubectl port-forward <pod> 8000:8000 -n <namespace>
- Exec into pod: kubectl exec -it <pod> -n <namespace> -- /bin/bash
```

### 12. Validate Fix

Run tests to verify fix: `cd {app_acronym}-api && poetry run pytest -v`

Check deployment health and report confirmation.

## Error Handling

**Cannot Reproduce**: Request pod logs, Application Insights traces, exact request details.

**Multiple Root Causes**: Prioritize by severity and impact, address systematically.

**Infrastructure Issue**: Identify if Terraform, Helm, or AKS config needs update.

## Common Debug Patterns

**Pattern 1: Connection Pool Exhausted**
- Symptom: Intermittent 500 errors under load
- Root Cause: Connections not released properly
- Fix: Use context managers, adjust pool size

**Pattern 2: OOM Kills**
- Symptom: Pod restarts, OOMKilled status
- Root Cause: Memory leak or insufficient limits
- Fix: Profile memory, increase limits, fix leaks

**Pattern 3: Slow Queries**
- Symptom: High P95 latency
- Root Cause: Missing indexes, N+1 queries
- Fix: Add indexes, use eager loading

**Pattern 4: Key Vault Access Denied**
- Symptom: Pod fails to start, secret mount errors
- Root Cause: Workload identity misconfigured
- Fix: Verify service account, access policies

**Pattern 5: Istio Sidecar Blocking**
- Symptom: CronJob never completes
- Root Cause: Sidecar not terminated
- Fix: Add quitquitquit trap

## Examples

**Example 1**: `/debug-backend API returns 500 error when creating orders`

**Example 2**: `/debug-backend Pod keeps restarting with OOMKilled status`

**Example 3**: `/debug-backend Helm deployment fails with ImagePullBackOff`

**Example 4**: `/debug-backend High latency on user search endpoint`

## References

Constitution: (pre-loaded above)
DevOps Standards: `vibe_cdo/2025.12.04-DevOpsArchetypeNotes.md`
