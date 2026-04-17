---
description: Validate Key Vault configuration for security, reliability, and governance readiness (Key Vault Config Steward)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype key-vault-config-steward --json ` and parse for AZURE_KEYVAULT_URL, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/key-vault-config-steward/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: configuration code location, test scope (unit, integration, security, performance), acceptance criteria, test environment setup. Request clarification if incomplete.

### 4. Analyze Test Requirements

Identify testable components: secret acquisition (Key Vault client initialization, secret retrieval, retry logic, error handling), fallback mechanism (Key Vault → env → .env cascade, fallback priority, error recovery), Pydantic models (field validation, type safety, overrides, redaction), authentication (managed identity flow, access policy validation, credential chain), telemetry (logging structure, metrics emission, context IDs), integration (FastAPI/Functions/worker usage, connection factories, refresh mechanism).

Define test scenarios: unit tests (secret client mocking, fallback logic, Pydantic validation, redaction utilities), integration tests (real Key Vault access, managed identity auth, fallback cascade validation), security tests (no secrets in logs, access policy enforcement, encryption verification), performance tests (secret fetch latency, cache effectiveness, concurrent access), reliability tests (network failure handling, retry behavior, rotation scenarios).

### 5. Generate Test Suite

Create comprehensive test suite with unit tests (mock KeyVault client tests, fallback strategy tests, Pydantic model validation tests, secret name registry tests), integration tests (Key Vault connectivity tests, managed identity auth tests, end-to-end config loading, fallback cascade validation), security tests (secret redaction validation, no secrets in logs verification, access control tests), performance tests (secret fetch latency benchmarks, cache hit rate validation, concurrent access tests), reliability tests (network failure scenarios, retry policy validation, secret rotation handling).

Include test fixtures, mock Key Vault, test secrets, environment setups.

### 6. Add Recommendations

Include testing best practices: automated testing in CI/CD, test Key Vault setup, secret rotation testing, security scanning integration, performance baselining, continuous validation.

Provide test execution commands and expected results.

### 7. Validate and Report


Execute test suite: `pytest tests/ --junitxml=results.xml --cov --cov-report=html`

Generate test report with pass/fail summary, coverage metrics, security validation, performance benchmarks. Report completion.

## Error Handling

**Test Key Vault Unavailable**: Provide setup instructions or use mock service.

**Managed Identity Not Configured**: Test with service principal fallback.

**Secret Not Found**: Create test secrets or use mock responses.

## Examples

**Example 1**: `/test-key-vault Validate FastAPI config with Key Vault integration` - Output: Complete test suite with security and reliability validation

**Example 2**: `/test-key-vault Create integration tests for managed identity auth` - Output: Authentication tests with fallback validation

**Example 3**: `/test-key-vault Generate security tests for secret redaction` - Output: Security test suite ensuring no leakage

## References

