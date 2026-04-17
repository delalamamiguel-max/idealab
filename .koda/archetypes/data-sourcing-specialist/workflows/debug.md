---
description: Debug data sourcing workflow for catalog, lineage, sampling, and PII guardrail violations (Data Sourcing Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-sourcing-specialist --json ` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-sourcing-specialist/templates/env-config.yaml` for catalog/table patterns

### 3. Parse Input
Extract from $ARGUMENTS: workflow file path, debug goals (catalog, lineage, sampling, PII). Request clarification if incomplete.

### 4. Analyze Workflow
Check for:
- Unmanaged locations
- Missing metadata
- Full dataset loads
- Embedded credentials
- Missing lineage
- PII exposure
- Non-approved exports

### 5. Debug and Fix
- Secure authentication
- Catalog metadata checks
- Sampling guardrails
- Data contract logging
- Lineage registration
- Parameterization
- Schema validation
- Access audit hooks

### 6. Validate and Report

## Error Handling
- Hard-stop confirmed: Stop execution, document breached rule (e.g., full table extract) and outline remediation before retry
- Missing reproduction data: Request query logs, Unity Catalog lineage, or sample rows; provide template command illustrating required evidence
- Tooling/access issue: Flag Purview API or secret scope access failures and point to env-config onboarding steps
- Consent or PII issue: Escalate unresolved consent violations and require policy approval before rerun

## Examples
- **Example 1**: `/debug-data-sourcing Investigate unmanaged S3 reads in analytics prototype` → Redirects to Unity Catalog, restores stewardship metadata, replays lineage
- **Example 2**: `/debug-data-sourcing Fix sampling overages in finance sandbox extract` → Adjusts sample fraction, enforces limit, documents governance approval
- **Example 3**: `/debug-data-sourcing Resolve PII leak reported by privacy audit` → Applies masking, updates access controls, generates remediation report

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/data-sourcing-specialist/templates/env-config.yaml`
