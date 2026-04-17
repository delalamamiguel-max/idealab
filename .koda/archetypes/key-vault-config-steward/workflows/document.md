---
description: Generate comprehensive documentation for Key Vault configuration layer and secret management (Key Vault Config Steward)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype key-vault-config-steward --json ` and parse for AZURE_KEYVAULT_URL, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/key-vault-config-steward/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: configuration code location, target audience (developers, operators, security team), documentation scope (architecture, usage, security, troubleshooting). Request clarification if incomplete.

### 4. Analyze Configuration Architecture

Extract configuration information: Pydantic models (field definitions, validation rules, type hints), secret acquisition (Key Vault client setup, authentication method, retry policies, fallback strategy), integration patterns (FastAPI usage, Azure Functions setup, worker services), security controls (managed identity, access policies, audit logging, redaction), telemetry (structured logging, metrics, health checks).

### 5. Generate Documentation Package

Create comprehensive documentation suite: Architecture Documentation (configuration layer overview, secret acquisition flow, Pydantic model structure, authentication mechanism, fallback cascade logic), Usage Guide (setup and prerequisites, managed identity configuration, Pydantic model usage, environment variables setup, integration with FastAPI/Functions/workers, secret rotation handling), Security Documentation (managed identity best practices, access policy configuration, secret redaction implementation, audit logging setup, compliance considerations, incident response procedures), Operations Guide (health check CLI usage, troubleshooting common issues, monitoring and alerting, secret rotation procedures, performance tuning, local development setup), Development Guide (adding new secrets, extending Pydantic models, testing with mock Key Vault, CI/CD integration, code examples and patterns).

Include supporting artifacts: architecture diagrams, code examples, configuration templates, health check scripts, troubleshooting flowcharts.

### 6. Add Recommendations

Include operational best practices: documentation maintenance (update with changes, version control), security reviews (periodic access audits, secret rotation schedules), monitoring and alerting setup, team onboarding procedures, continuous improvement processes.

### 7. Validate and Report


Generate documentation artifacts organized in docs/ directory. Create index with navigation. Report completion.

## Error Handling

**Incomplete Information**: Request additional configuration and security details.

**Missing Diagrams**: Generate flow diagrams from code structure.

**Security Gaps**: Flag missing security documentation and recommendations.

## Examples

**Example 1**: `/document-key-vault Create complete documentation for FastAPI Key Vault config` - Output: Architecture docs, usage guide, security documentation

**Example 2**: `/document-key-vault Generate security documentation for Key Vault integration` - Output: Security guide with managed identity setup and audit logging

**Example 3**: `/document-key-vault Document troubleshooting guide for Key Vault configuration` - Output: Operations guide with common issues and resolutions

## References

