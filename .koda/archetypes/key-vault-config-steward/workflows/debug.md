---
description: Debug Azure Key Vault configuration issues, secret retrieval failures, and authentication problems (Key Vault Config Steward)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype key-vault-config-steward --json ` and parse for AZURE_KEYVAULT_URL, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/key-vault-config-steward/templates/env-config.yaml` for debugging tools

### 3. Parse Input
Extract from $ARGUMENTS: failure type (authentication error, secret not found, timeout, validation failure), error messages and stack traces, configuration code location, environment. Request clarification if incomplete.

### 4. Diagnose Issue

Run diagnostic checks: Authentication Issues (verify managed identity configuration, check RBAC assignments, validate access policies, test DefaultAzureCredential chain), Secret Retrieval Failures (verify secret name spelling, check Key Vault URI, validate secret exists and is enabled, test network connectivity), Validation Errors (check Pydantic model definitions, verify field types and constraints, validate secret format, test environment overrides), Fallback Issues (verify fallback order, check environment variables, validate .env file loading, test fallback cascade logic), Performance Problems (analyze secret fetch latency, check retry policy effectiveness, monitor cache hit rates).

Provide diagnostic report with root cause hypothesis.

### 5. Generate Fix Recommendations

Provide targeted fixes: for authentication (configure managed identity correctly, update access policies, fix RBAC assignments), for secret retrieval (correct secret names, fix vault URI, enable secrets, resolve network issues), for validation (fix Pydantic models, update field constraints, correct secret formats), for fallbacks (adjust fallback order, set environment variables, fix .env file), for performance (implement caching, adjust retry policies, optimize secret fetching).

Include code fixes and configuration changes.

### 6. Add Prevention Measures

Recommend improvements: comprehensive health checks, better error messages with context IDs, monitoring and alerting for secret access, automated validation testing, secret rotation testing.

### 7. Validate and Report


Generate debug report with issue analysis, fixes, prevention measures. Report completion.

## Error Handling

**Authentication Failed**: Provide detailed troubleshooting for managed identity setup.

**Network Issues**: Test connectivity and provide firewall configuration guidance.

**Secret Format Mismatch**: Document expected format and validation rules.

## Examples

**Example 1**: `/debug-key-vault Authentication failed with DefaultAzureCredential` - Output: Managed identity troubleshooting with RBAC fixes

**Example 2**: `/debug-key-vault Secret DATABASE_URL not found in Key Vault` - Output: Secret name analysis with fallback validation

**Example 3**: `/debug-key-vault Pydantic validation error on database config` - Output: Model definition fix with validation constraints

## References

