---
description: Generate Azure Key Vault configuration layer with typed fallbacks and observability (Key Vault Config Steward)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype key-vault-config-steward --json ` and parse for AZURE_KEYVAULT_URL, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/key-vault-config-steward/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: application type (FastAPI, Azure Functions, worker service), required secrets (database, API keys, certificates), fallback strategy, environment requirements. Request clarification if incomplete.

### 4. Generate Configuration Layer

Create comprehensive configuration artifacts: Pydantic Models (AppConfig with BaseSettings, typed secret fields with validation, environment-specific overrides, redaction helper for logging), Secret Acquisition (DefaultAzureCredential with managed identity, SecretClient with retry policies, fallback cascade (Key Vault → env vars → .env), secret name registry as enum, error handling with context IDs), Connector Management (SQLAlchemy URL builder, Redis connection pool, API client factories, rotation-aware refresh method), Operational Controls (structured JSON logging with metadata, telemetry hooks for secret fetch metrics, health check CLI command, unit tests for all paths).

### 5. Generate Supporting Code

Create helper utilities: validation hooks for connectors, type-safe overrides mechanism, configuration dump utilities, mock Key Vault for testing, example integrations for FastAPI/Functions/workers.

### 6. Add Recommendations

Include best practices: managed identity configuration, secret rotation procedures, monitoring and alerting setup, local development with fallbacks, security scanning integration, documentation and examples.

### 7. Validate and Report


Generate configuration layer with tests and examples. Report completion.

## Error Handling

**Managed Identity Missing**: Provide setup instructions for Azure resources.

**Key Vault Access Denied**: Verify access policies and RBAC assignments.

**Secret Not Found**: Implement fallback strategy with clear error messages.

## Examples

**Example 1**: `/scaffold-key-vault Generate config layer for FastAPI with database secrets` - Output: Complete Pydantic config with Key Vault integration

**Example 2**: `/scaffold-key-vault Create Azure Functions config with API key management` - Output: Config layer with managed identity and fallbacks

**Example 3**: `/scaffold-key-vault Build configuration with secret rotation support` - Output: Rotation-aware config with refresh mechanism

## References

