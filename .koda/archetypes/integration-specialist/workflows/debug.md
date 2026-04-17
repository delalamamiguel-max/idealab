---
description: Debug REST/GraphQL API errors and failures (Integration Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype integration-specialist --json ` and parse for API_FRAMEWORK, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/integration-specialist/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: API endpoint, error message (HTTP status codes, error responses), symptoms (timeout, 500 errors, authentication failures), context (request payload, headers, environment). Request clarification if incomplete.

### 4. Analyze Problem

Identify error category: authentication errors (401, 403), client errors (400, 404, 422), server errors (500, 502, 503), timeout errors, rate limiting (429), validation errors. Analyze error responses, logs, and API code. Check against constitution for violations. Report findings with endpoint, error type, root cause.

### 5. Generate Fix

Create fixed API code addressing root cause: fix authentication (token validation, scope checks), fix validation (request schema, input sanitization), fix error handling (proper status codes, error messages), fix performance (caching, connection pooling), fix rate limiting (proper headers, backoff). Include complete fixed code with proper error responses.

### 6. Add Recommendations

Include recommendations for prevention (API testing, contract validation, monitoring), testing (unit tests, integration tests, load tests), monitoring (error rates, latency, availability). Provide summary with root cause, fix, and prevention.

### 7. Validate and Report


## Error Handling

**Insufficient Error Information**: Request complete error response, request details, and logs.

**Cannot Reproduce**: Request environment, authentication details, and request payload.

**Multiple Possible Causes**: Provide systematic debugging steps.

## Examples

**Example 1: 500 Internal Server Error**
```
/debug-api POST /orders returning 500 error

Root Cause: Unhandled exception when processing invalid date format
Fix: Added input validation, proper error handling, returns 400 with clear message
```

**Example 2: Authentication Failure**
```
/debug-api Getting 401 Unauthorized on valid token

Root Cause: Token expiration check using wrong timezone
Fix: Corrected timezone handling, added token refresh logic
```

**Example 3: Timeout**
```
/debug-api API timing out after 30 seconds

Root Cause: Synchronous database query blocking request thread
Fix: Implemented async processing, added timeout configuration, connection pooling
```

## References

