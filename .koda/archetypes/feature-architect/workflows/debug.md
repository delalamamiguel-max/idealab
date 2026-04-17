---
description: Diagnose feature engineering defects and reinstate governed contracts, quality checks, and lineage (Feature Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype feature-architect --json ` and require ENV_VALID. Stop if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/feature-architect/templates/env-config.yaml` for quality thresholds, lineage tooling, and store settings

### 3. Parse Input
Gather from $ARGUMENTS: failing feature name/table, error symptoms (data drift, contract breach, skew), runtime environment, downstream consumers, incident severity. Request notebooks, job logs, feature store metadata, and lineage exports if absent.

### 4. Reproduce Failure
Investigate by:
- Re-running source validation and freshness checks
- Inspecting joins/windows for temporal leakage
- Comparing feature distributions vs baselines for drift or skew
- Checking feature contract metadata for missing or inconsistent definitions
- Reviewing privacy controls (hashing/tokenization) for sensitive fields
- Confirming feature store registration status and version history
- Auditing quality tests, unit tests, and monitoring alerts for failures
- Tracing lineage graph for upstream schema changes

### 5. Implement Fixes
Recommend corrective actions:
- Patch validation scripts and enforce SLA enforcement
- Rebuild temporal logic with proper `as_of_ts` handling
- Update feature contract and metadata fields in store
- Reinforce privacy transforms and document compliance evidence
- Regenerate quality/monitoring suites and adjust thresholds
- Re-register versions with proper tags and retention metadata
- Document remediation in change log and notify consumers

### 6. Prevent Recurrence
Propose safeguards:
- Automated schema evolution tests in CI/CD pipelines
- Scheduled skew detection jobs with alert routing
- Modularize transformations for reuse and central governance
- Add cost/performance telemetry to monitor job health
- Enhance documentation templates with remediation history

### 7. Validate and Report

## Error Handling
- Missing telemetry: Request job logs, feature store snapshots, lineage exports; share example command listing required inputs
- Hard-stop unresolved: Refuse to continue if temporal leakage, privacy breaches, or unregistered features remain
- Tooling gap: Flag absence of Purview/Unity connectors or quality libraries; reference env-config setup
- Stakeholder impact: Escalate to data owners if contract breach affected SLAs

## Examples
- **Example 1**: `/debug-feature Skew detection firing for online feature table`
- **Example 2**: `/debug-feature Feature contract mismatch after upstream schema change`
- **Example 3**: `/debug-feature PII exposure flagged in marketing propensity features`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/feature-architect/templates/env-config.yaml`
