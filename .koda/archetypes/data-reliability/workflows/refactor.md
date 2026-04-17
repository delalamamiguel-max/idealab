---
description: Refactor data reliability workflows to reinforce telemetry, alerting, and lifecycle compliance (Data Reliability)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-reliability --json ` and parse for MONITORING_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-reliability/templates/env-config.yaml` for best practices

### 3. Parse Input
Extract from $ARGUMENTS: current framework location, refactoring goals (SLO coverage, monitoring gaps, quality improvements), specific issues. Request clarification if incomplete.

### 4. Analyze Current State
Assess: SLO coverage (defined vs undefined, measurement accuracy), monitoring (dashboard completeness, alert coverage, adaptive thresholds), quality rules (comprehensiveness, accuracy, schema contracts), lineage integrity (provenance completeness, dependency tracking), incident response (runbook completeness, post-incident reviews).

### 5. Generate Refactoring Plan
Create improvements: enhanced SLOs (additional dimensions, refined targets, error budget tracking), improved monitoring (golden dashboards, adaptive alerts, anomaly detection), strengthened quality (additional rules, schema evolution controls, distribution monitoring), enhanced lineage (complete provenance, impact analysis), better incident response (detailed runbooks, automated recovery, continuous verification).

### 6. Implement Refactorings
Generate refactored framework with improved SLOs, enhanced monitoring, strengthened quality controls, complete lineage, robust incident response, updated documentation.

### 7. Validate and Report
Generate refactoring report with improvements. Report completion.

## Error Handling
**SLO Gaps**: Prioritize critical dimensions and implement incrementally.
**Monitoring Blind Spots**: Add coverage systematically by severity.

## Examples
**Example 1**: `/refactor-data-reliability Add comprehensive SLOs to data platform` - Output: Enhanced framework with multi-dimensional SLOs
**Example 2**: `/refactor-data-reliability Implement adaptive alerting for pipelines` - Output: Monitoring with seasonality-aware thresholds

## References
