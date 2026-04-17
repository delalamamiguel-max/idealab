---
description: Compare Key Vault configuration approaches and secret management patterns (Key Vault Config Steward)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype key-vault-config-steward --json ` and parse for AZURE_KEYVAULT_URL, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/key-vault-config-steward/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type (secret management approaches, authentication methods, configuration frameworks, fallback strategies), candidate options, evaluation criteria (security, complexity, cost, reliability). Request clarification if incomplete.

### 4. Generate Comparison Framework

Based on comparison type, evaluate: Secret Management (Key Vault vs Azure App Configuration vs environment variables - security, rotation, audit, cost), Authentication Methods (managed identity vs service principal vs connection strings - security, operations, cloud-native fit), Configuration Frameworks (Pydantic vs dataclasses vs plain dicts - type safety, validation, maintainability), Fallback Strategies (Key Vault-first vs env-first vs hybrid - reliability, development experience, security posture).

### 5. Create Comparison Matrix

Generate detailed comparison with quantitative metrics (cost analysis, performance impact, security posture scores), qualitative assessments (complexity, learning curve, team capability requirements), trade-off analysis, use case recommendations.

Include security risk analysis for each approach.

### 6. Add Recommendations

Recommend approach with comprehensive justification: security requirements alignment, operational feasibility, cost-benefit analysis, team capability, migration path, compliance requirements.

Provide implementation roadmap and adoption strategy.

### 7. Validate and Report


Generate comparison report with decision matrix, security analysis, recommendations. Report completion.

## Error Handling

**Insufficient Security Context**: Request compliance and security requirements.

**Unclear Use Case**: Facilitate requirements gathering for secret management needs.

**Cost Uncertainty**: Provide pricing models and usage projections.

## Examples

**Example 1**: `/compare-key-vault Managed Identity vs Service Principal for Key Vault auth` - Output: Authentication comparison with security and operational analysis

**Example 2**: `/compare-key-vault Pydantic vs dataclasses for typed configuration` - Output: Framework comparison with type safety and validation assessment

**Example 3**: `/compare-key-vault Key Vault-first vs environment-first fallback strategy` - Output: Strategy comparison with reliability and security trade-offs

## References

