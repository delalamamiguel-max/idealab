---
description: Refactor REST/GraphQL API to apply security, performance, and contract best practices (Integration Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype integration-specialist --json ` and parse for API_FRAMEWORK, OPENAPI_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/integration-specialist/templates/env-config.yaml` for rate limits, auth config, pagination defaults

### 3. Parse Input
Extract from $ARGUMENTS: existing API spec or code file path, refactoring goals (authentication, rate limiting, pagination, error handling, versioning), constraints. Request clarification if incomplete.

### 4. Analyze Existing Code
Load and analyze existing API:
- Identify hard-stop rule violations (missing authentication, no rate limiting, missing error responses, hardcoded secrets, no request validation, missing CORS config, no API versioning, missing pagination)
- Identify missing mandatory patterns (OAuth2/JWT authentication, rate limit headers, comprehensive error responses, request/response validation, CORS configuration, semantic versioning, pagination support, circuit breakers)
- Identify opportunities for preferred patterns (OpenAPI 3.x spec, response caching, compression, health endpoints, metrics endpoints, API documentation, contract testing)

Report findings with endpoint paths and severity.

### 5. Generate Refactored API

Create refactored API applying hard-stop fixes (add OAuth2/JWT authentication, implement rate limiting with headers, define comprehensive error responses, move secrets to environment, add request validation, configure CORS, implement versioning, add pagination), mandatory patterns (complete OpenAPI spec, circuit breaker pattern, retry logic, structured logging, monitoring hooks), and preferred patterns (response caching, compression, health/metrics endpoints, comprehensive documentation).

Include complete code example with authentication middleware, rate limiting, error handlers, and endpoint implementations.

### 6. Add Recommendations

Include inline comments for security (API key rotation, request signing, TLS 1.3), performance (caching strategies, connection pooling, async processing), scalability (load balancing, horizontal scaling), and observability (distributed tracing, metrics collection).

Provide summary of improvements with security enhancements and performance impact.

### 7. Validate and Report


Generate optional contract tests and API documentation. Report completion with file paths, applied improvements, security enhancements, next steps.

## Error Handling

**Hard-Stop Violations in Original**: Explain each violation clearly (e.g., "Missing authentication on POST /orders"), show compliant alternative with OAuth2 configuration.

**Incomplete Input**: List missing information (API spec or code path, refactoring goals, constraints), provide well-formed example.

**Environment Failure**: Report missing API framework or tools, suggest installation and configuration steps.

## Examples

**Example 1: Add Authentication**
```
/refactor-api Add OAuth2 authentication to orders_api.yaml

Input: API spec without authentication
Output: Refactored with OAuth2 security scheme, bearer token validation, scope definitions
```

**Example 2: Implement Rate Limiting**
```
/refactor-api Add rate limiting with headers to customer_api.py

Input: API without rate limiting
Output: Refactored with rate limit middleware, X-RateLimit headers, 429 responses
```

**Example 3: Improve Error Handling**
```
/refactor-api Enhance error responses in payment_api.yaml with detailed error codes

Input: API with basic error responses
Output: Refactored with comprehensive error schema, error codes, troubleshooting hints
```

## References

