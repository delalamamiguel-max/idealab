---
description: Test data sourcing workflow for catalog, lineage, sampling, and PII guardrail compliance (Data Sourcing Specialist)
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
Extract from $ARGUMENTS: workflow file path, test goals (catalog, lineage, sampling, PII). Request clarification if incomplete.

### 4. Test Workflow
Check for:
- Unmanaged locations
- Missing metadata
- Full dataset loads
- Embedded credentials
- Missing lineage
- PII exposure
- Non-approved exports

### 5. Validate and Report

## Error Handling
- Test failure: Document violated assertion (e.g., missing retention policy) and list remediation checklist before retesting
- Insufficient inputs: Request workflow path, sampling thresholds, or consent IDs; include sample invocation showing required arguments
- Tooling discrepancy: Note absence of validation scripts or Purview connectivity and reference env-config actions
- Audit evidence missing: Require upload of lineage or sampling logs prior to final sign-off

## Examples
- **Example 1**: `/test-data-sourcing Certify customer360 extract prior to analyst access` → Produces report confirming stewardship metadata, sampling caps, PII masking
- **Example 2**: `/test-data-sourcing Validate finance regulatory pull for retention and consent coverage` → Confirms retention policy alignment, consent registry linkage, access logs
- **Example 3**: `/test-data-sourcing Regression-test marketing sandbox loader after schema change` → Runs guardrail suite checking schema validation, lineage updates, audit hooks

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/data-sourcing-specialist/templates/env-config.yaml`
