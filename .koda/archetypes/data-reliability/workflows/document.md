---
description: Package reconciled performance narratives, visuals, and approvals for stakeholder distribution (Data Reliability)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-reliability --json ` and parse for MONITORING_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-reliability/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: framework location, target audience, documentation scope. Request clarification if incomplete.

### 4. Analyze Reliability Framework
Extract: SLO definitions (targets, measurements, error budgets), monitoring configuration (dashboards, alerts, thresholds), quality rules (validation logic, schema contracts, drift detection), lineage maps (provenance, dependencies), incident procedures (runbooks, escalation, post-mortems).

### 5. Generate Documentation Package
Create: Reliability Guide (SLO definitions and measurement, error budget policies, monitoring procedures, quality standards, lineage requirements), Operations Runbook (dashboard usage, alert response, incident procedures, recovery steps, escalation paths), Quality Documentation (validation rules, schema evolution policies, drift detection, remediation procedures), Incident Response Guide (failure mode taxonomy, runbook procedures, post-incident review templates, continuous improvement), Stakeholder Reports (SLO performance dashboards, error budget status, quality metrics, incident summaries).

### 6. Add Recommendations
Include: reliability review schedules, SLO refinement procedures, quality improvement cycles, incident learning processes.

### 7. Validate and Report
Generate documentation artifacts. Report completion.

## Error Handling
**Incomplete Information**: Request SLO details and monitoring configuration.
**Missing Metrics**: Collect historical data and baseline performance.

## Examples
**Example 1**: `/document-data-reliability Create complete reliability documentation` - Output: SLO guide, runbooks, quality documentation
**Example 2**: `/document-data-reliability Generate stakeholder reliability report` - Output: Executive summary with SLO performance and incident trends

## References
