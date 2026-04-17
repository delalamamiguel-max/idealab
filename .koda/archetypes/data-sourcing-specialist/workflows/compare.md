---
description: Compare data sourcing workflows for catalog, lineage, sampling, and PII guardrail coverage (Data Sourcing Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-sourcing-specialist --json ` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/data-sourcing-specialist/templates/env-config.yaml` for catalog/table patterns

### 3. Parse Input
Extract from $ARGUMENTS: workflow file paths, compare goals (catalog, lineage, sampling, PII). Request clarification if incomplete.

### 4. Compare Workflows
Check for:
- Unmanaged locations
- Missing metadata
- Full dataset loads
- Embedded credentials
- Missing lineage
- PII exposure
- Non-approved exports

### 5. Report Comparison
Summarize:
- Guardrail coverage
- Catalog compliance
- Lineage registration
- Sampling enforcement
- PII controls
- Recommendations for improvement

## Error Handling
- Missing artifacts: Request both workflows, lineage exports, sampling specs; include checklist of required attachments
- Guardrail deltas: Highlight mismatched privacy or retention controls and recommend harmonized policy updates
- Schema divergence: Flag field-level discrepancies (e.g., new PII column) and propose remediation sequence before sign-off
- Tooling gap: Note missing Unity Catalog or Purview connectors and map env-config actions to restore comparability

## Examples
- **Example 1**: `/compare-data-sourcing Evaluate legacy CRM extract against new Delta pipeline` → Outputs guardrail delta table with remediation actions
- **Example 2**: `/compare-data-sourcing Contrast marketing sandbox and certified analytics feed` → Highlights sampling differences, privacy gaps, required approvals
- **Example 3**: `/compare-data-sourcing Benchmark vendor feed with internal golden record` → Flags absent consent lineage and suggests contract updates

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/data-sourcing-specialist/templates/env-config.yaml`
