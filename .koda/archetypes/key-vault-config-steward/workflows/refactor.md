---
description: Refactor Key Vault configuration to apply security, type safety, and observability best practices (Key Vault Config Steward)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype key-vault-config-steward --json ` and parse for AZURE_KEYVAULT_URL, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/key-vault-config-steward/templates/env-config.yaml` for best practices

### 3. Parse Input
Extract from $ARGUMENTS: configuration code location, refactoring goals (type safety, security, observability, performance), specific issues (raw dicts, hard-coded secrets, missing validation). Request clarification if incomplete.

### 4. Analyze Current State

Assess configuration: security posture (secret storage, authentication method, access controls, audit logging), type safety (Pydantic usage, validation rules, type hints), observability (structured logging, telemetry, error handling), reliability (fallback strategy, retry policies, error recovery), code quality (modularity, reusability, testing).

Identify refactoring opportunities and security risks.

### 5. Generate Refactoring Plan

Create improvements: Security Enhancements (migrate to managed identity, externalize all secrets to Key Vault, implement access policies, enable audit logging, add secret redaction), Type Safety Improvements (replace raw dicts with Pydantic models, add field validators, implement type-safe overrides, add comprehensive validation), Observability Additions (structured JSON logging with metadata, telemetry for secret fetch operations, context IDs for errors, health check CLI), Reliability Enhancements (implement fallback cascade, add retry policies, create rotation-aware refresh, improve error handling), Code Quality (modular design, reusable components, comprehensive testing, clear documentation).

### 6. Implement Refactorings

Generate refactored code: updated configuration models with Pydantic, secure secret acquisition with managed identity, enhanced observability with logging and telemetry, improved reliability with fallbacks and retries, comprehensive test suite.

Include migration guide with backward compatibility strategy.

### 7. Validate and Report


Generate refactoring report with before/after comparison, security improvements, type safety gains, observability enhancements. Report completion.

## Error Handling

**Breaking Changes**: Provide gradual migration path with feature flags.

**Secret Migration**: Plan careful migration to Key Vault with rollback.

**Performance Impact**: Benchmark and optimize secret fetching.

## Examples

**Example 1**: `/refactor-key-vault Migrate env-file config to Key Vault with Pydantic` - Output: Type-safe config with Key Vault integration

**Example 2**: `/refactor-key-vault Add observability to existing Key Vault config` - Output: Enhanced config with logging and telemetry

**Example 3**: `/refactor-key-vault Implement managed identity for Key Vault access` - Output: Secure authentication with zero secrets in code

## References

