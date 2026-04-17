---
description: Scaffold governed data sourcing workflow for exploratory analysis, enforcing Unity Catalog, lineage, and sampling guardrails (Data Sourcing Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-sourcing-specialist --json ` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-sourcing-specialist/templates/env-config.yaml` for catalog names, schemas, table patterns

### 3. Parse Input
Extract from $ARGUMENTS: dataset name, purpose, sampling budget, retention policy, lineage requirements, PII controls. Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse unmanaged locations if Unity Catalog asset exists
- ✘ Refuse tables lacking stewardship metadata, retention, or SLA tags
- ✘ Refuse full dataset loads; enforce sampling limits
- ✘ Refuse embedded credentials
- ✘ Refuse missing lineage capture
- ✘ Refuse PII exposure without controls
- ✘ Refuse non-approved exports
If violated, explain and suggest compliant alternatives.

### 5. Generate Workflow
- Secure authentication (Managed Identity/secret scopes)
- Catalog metadata checks (ownership, quality, freshness)
- Sampling guardrails (`limit`, `sample`, profile jobs)
- Data contract logging (structured logs)
- Lineage registration (Purview SDK)
- Parameterization (external config)
- Schema validation (information_schema)
- Access audit hooks (Azure Monitor/Databricks metrics)

### 6. Add Recommendations
- Profile-first workflow (counts, nulls, freshness)
- Query cost estimation
- Reusable discovery utilities
- Tag propagation
- Access review bundles
- Time-boxed sampling widgets
- Automated glossary links

### 7. Validate and Report

## Error Handling
- Hard-stop violation: Cite the breached rule (e.g., unmanaged location requested) and prescribe remediation before continuing
- Missing context: Request catalog identifiers, sampling budget, or retention policy; share a well-formed command illustrating required details
- Tooling gap: Note absent Unity Catalog or Purview access and reference env-config for onboarding steps
- Credential risk: Refuse workflows attempting to embed secrets and redirect to managed identity or secret scopes

## Examples
- **Example 1**: `/scaffold-data-sourcing Sample subscriber_usage_daily with 2GB cap and full lineage logging` → Outputs notebook with sampling widgets, Purview registration, audit hooks
- **Example 2**: `/scaffold-data-sourcing Prepare governed extract of marketing_leads for sandbox analysis` → Generates workflow with stewardship validation, PII masking, structured logging
- **Example 3**: `/scaffold-data-sourcing Build notebook for finance_compliance feed with consent verification` → Includes consent registry checks, access audit hooks, time-boxed sampling

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/data-sourcing-specialist/templates/env-config.yaml`
