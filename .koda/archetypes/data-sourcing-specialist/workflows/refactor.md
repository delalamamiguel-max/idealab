---
description: Refactor data sourcing workflow to enforce catalog, lineage, sampling, and PII guardrails (Data Sourcing Specialist)
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
Extract from $ARGUMENTS: workflow file path, refactoring goals (catalog compliance, lineage, sampling, PII controls). Request clarification if incomplete.

### 4. Analyze Existing Workflow
Scan for:
- Unmanaged locations
- Missing stewardship metadata
- Full dataset loads
- Embedded credentials
- Missing lineage capture
- PII exposure
- Non-approved exports

### 5. Generate Refactored Workflow
Apply:
- Secure authentication
- Catalog metadata checks
- Sampling guardrails
- Data contract logging
- Lineage registration
- Parameterization
- Schema validation
- Access audit hooks

### 6. Add Recommendations
- Profile-first workflow
- Query cost estimation
- Reusable utilities
- Tag propagation
- Access review bundles
- Time-boxed sampling
- Glossary links

### 7. Validate and Report

## Error Handling
- Hard-stop persists: Block refactor until stewardship metadata, lineage capture, or sampling guards are restored; cite constitution clause
- Missing artifacts: Request notebook path, config file, or lineage logs; respond with a sample invocation showing required inputs
- Tooling mismatch: Flag absent Purview SDK or sampling utilities and direct to env-config installation notes
- Credentials embedded: Require migration to managed identity or secret scopes before proceeding

## Examples
- **Example 1**: `/refactor-data-sourcing Harden legacy customer360 ingestion notebook for Unity Catalog compliance` → Adds metadata validation, Purview lineage, sampling caps
- **Example 2**: `/refactor-data-sourcing Update fraud investigation extract to remove inline credentials` → Switches to secret scopes, enforces structured logging, revises schema checks
- **Example 3**: `/refactor-data-sourcing Improve marketing sandbox loader with time-boxed sampling and access audits` → Introduces parameter widgets, audit metrics, consent verification

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/data-sourcing-specialist/templates/env-config.yaml`
