---
description: Diagnose experiment failures, restore statistical integrity, and unblock governance approvals (Experiment Scientist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype experiment-scientist --json ` and ensure ENV_VALID is true. Stop if validation fails.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/experiment-scientist/templates/env-config.yaml` for metric thresholds, fairness libraries, notification hooks

### 3. Parse Input
Collect from $ARGUMENTS: failing experiment ID, symptom (metric drift, failed test, approval rejection), environment, impacted cohorts, governance ticket. Request MLflow run link, datasets, and stats output as needed.

### 4. Reproduce Issue
Investigate by:
- Verifying control/treatment definitions and baseline stability
- Re-running power analysis and sample sufficiency checks
- Inspecting KPI calculations for omissions or cherry-picking
- Recomputing statistical tests and confirming p-values/credible intervals
- Reviewing MLflow artifacts for missing lineage or stale datasets
- Checking fairness metrics and protected cohort diagnostics
- Inspecting Azure DevOps or approval logs for gating failures
- Comparing metrics to `metric_tolerance_delta` thresholds

### 5. Apply Fixes
Recommend targeted remediation:
- Restore proper cohort mappings and deterministic splits
- Update experiment notebooks with corrected metrics and statistical routines
- Regenerate fairness reports with required cohorts and documentation
- Re-log MLflow artifacts, linking dataset versions and git SHAs
- Patch Azure DevOps pipeline gates, approvals, and notifications
- Draft remediation summary for governance boards with decision log updates

### 6. Guard Against Recurrence
Implement preventative measures:
- Schedule automated validation notebooks pre- and post-experiment
- Enable drift alerts for experiment telemetry tables
- Document learnings in shared experiment playbook
- Add checklists to design doc template for future runs
- Trigger notification channels for future policy threshold breaches

### 7. Validate and Report

## Error Handling
- Insufficient context: Request detailed failure logs, MLflow artifacts, dataset snapshot; supply example command showing expected fields
- Hard-stop unresolved: Halt assistance until control groups, sample sufficiency, or governance approvals restored
- Tooling issues: Flag missing statistical or fairness libraries and reference env-config setup steps
- Unauthorized override attempts: Escalate to governance leads before proceeding

## Examples
- **Example 1**: `/debug-experiment Approval blocked due to missing power analysis for uplift test`
- **Example 2**: `/debug-experiment Fairness audit failing on protected cohort disparity`
- **Example 3**: `/debug-experiment MLflow lineage mismatch triggering governance rejection`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/experiment-scientist/templates/env-config.yaml`
