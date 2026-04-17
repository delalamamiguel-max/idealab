---
description: Generate REST/GraphQL API endpoints with authentication, rate limiting, and contract testing (Integration Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype integration-specialist --json ` and parse for FRAMEWORK, API_TYPE, AUTH_METHOD, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/integration-specialist/templates/env-config.yaml` for framework (Flask/Express), auth config, rate limits

### 3. Parse Input
Extract from $ARGUMENTS: API purpose, endpoints needed (GET/POST/PUT/DELETE), data models, authentication requirements (OAuth2/JWT/API key), rate limiting needs. Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse endpoints without authentication
- ✘ Refuse missing input validation
- ✘ Refuse no rate limiting for public endpoints
- ✘ Refuse missing error handling with proper status codes
If violated, explain clearly and suggest compliant alternative.

### 5. Generate API Scaffold

Create API application with structure: framework initialization with CORS and security headers, authentication middleware (OAuth2/JWT/API key validation), rate limiting configuration (requests per minute/hour), request validation using schemas (Pydantic/Joi), endpoint definitions with proper HTTP methods, response formatting with consistent structure, error handling with appropriate status codes (400/401/403/404/500), logging middleware for request/response tracking.

Security patterns: authentication on all endpoints (except health check), input sanitization and validation, SQL injection prevention, XSS protection headers, HTTPS enforcement, secrets management (environment variables), CORS configuration for allowed origins.

API patterns: RESTful resource naming (plural nouns), versioning in URL (/api/v1/), pagination for list endpoints, filtering and sorting support, consistent error response format, OpenAPI/Swagger documentation, health check endpoint.

Apply mandatory patterns: authentication middleware, input validation schemas, rate limiting per endpoint, structured error responses, request/response logging, OpenAPI spec generation, contract testing setup.

### 5.5. Validate Dependencies and Data Models

**Python Dependency Validation**:
Run `${ARCHETYPES_BASEDIR}/integration-specialist/scripts/validate-dependencies.py --requirements requirements.txt --json` to check for version compatibility.

**If violations found**:
- Report incompatible package combinations (FastAPI + Pydantic + SQLAlchemy)
- Suggest compatible versions from constitutional rules
- Halt until resolved or user acknowledges risk

**Data Model Validation** (if database models generated):
Run `${ARCHETYPES_BASEDIR}/integration-specialist/scripts/validate-sql-keywords.py --identifiers <extracted_field_names> --engine sqlalchemy --json` to check Pydantic model fields.

**If violations found**:
- Report fields conflicting with ORM reserved attributes
- Auto-fix by applying prefixes:
  - `metadata` → `workflow_metadata`
  - `query` → `search_query`
  - `session` → `api_session`
- Update Pydantic models with corrected field names

**Validation Report**:
```
✓ Python Dependencies: FastAPI 0.104.1 + Pydantic 2.9.2 + SQLAlchemy 2.0.35
✓ Data Models: No reserved keyword conflicts in Pydantic fields
```

### 6. Add Recommendations

Include comments for: caching strategies (Redis), async processing for long operations, webhook support for events, API gateway integration, monitoring and metrics.

### 7. Validate and Report


Generate optional contract tests (Pact/Postman). Report completion with file paths, endpoint documentation, testing commands, next steps.

## Error Handling

**Hard-Stop Violations**: Explain violation (e.g., missing authentication), suggest compliant alternative with auth middleware example.

**Incomplete Input**: List missing information (endpoints, data models, auth requirements), provide well-formed example.

**Environment Failure**: Report missing framework or dependencies, suggest installation steps.

## Examples

**Customer API**: `/scaffold-api Create REST API for customer data: GET /customers, POST /customers, PUT /customers/{id}, use JWT auth, rate limit 100 req/min`
Output: Flask/Express API with CRUD endpoints, JWT middleware, rate limiting, validation, OpenAPI docs.

**Webhook Service**: `/scaffold-api Create webhook receiver for payment events, validate signatures, process async, return 200 immediately`
Output: API with webhook endpoint, signature validation, async processing, retry logic.

**GraphQL API**: `/scaffold-api Create GraphQL API for product catalog, queries for products/categories, mutations for cart, use OAuth2`
Output: GraphQL server with schema, resolvers, OAuth2 middleware, query complexity limits.

## References

