---
description: Generate test harness for REST/GraphQL APIs (Integration Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype integration-specialist --json ` and parse for API_FRAMEWORK, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/integration-specialist/templates/env-config.yaml` for test configuration

### 3. Parse Input
Extract from $ARGUMENTS: API spec or code file, testing framework (pytest, Jest, Postman), coverage goals (unit, integration, contract), test scenarios. Request clarification if incomplete.

### 4. Analyze Code

Identify testable components: API endpoints, request/response schemas, authentication, error handling, rate limiting. Determine test scenarios: unit tests (handler functions), integration tests (API calls), contract tests (schema validation), security tests (auth, input validation), performance tests (response time, load). Report test coverage plan.

### 5. Generate Test Suite

Create test suite with API client fixtures, unit tests for handlers, integration tests for endpoints, contract tests with schema validation, security tests, performance tests. Include complete test code with mocking and assertions.

### 6. Add Recommendations

Include recommendations for test execution (use test API, mock external services), CI/CD integration (run on PR, contract testing), coverage improvements (test all error codes, validate all schemas), monitoring (track API health, test in staging). Provide summary.

### 7. Validate and Report


## Error Handling

**Insufficient Spec**: Request complete API spec or code.

**No Test Environment**: Provide test API setup instructions.

**Missing Schemas**: Suggest schema generation from OpenAPI spec.

## Examples

**Example 1**: `/test-api Generate tests for orders_api.yaml` - Output: 20 tests covering all endpoints

**Example 2**: `/test-api Create contract tests for customer_api.py` - Output: Schema validation tests

**Example 3**: `/test-api Add security tests for payment_api.py` - Output: Auth and input validation tests

## References

