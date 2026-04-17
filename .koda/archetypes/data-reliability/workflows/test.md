---
description: Validate data reliability workflows for SLO coverage, monitoring readiness, and incident preparedness (Data Reliability)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-reliability --json ` and parse for MONITORING_ENDPOINT, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-reliability/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: framework location, test scope (SLOs, monitoring, quality, lineage, incident response), acceptance criteria. Request clarification if incomplete.

### 4. Analyze Test Requirements
Identify components: SLO definitions (target validation, measurement accuracy, error budget calculation), monitoring (dashboard completeness, alert coverage, adaptive thresholds), quality rules (validation accuracy, schema contracts, drift detection), lineage integrity (provenance capture, dependency tracking), incident response (runbook completeness, recovery procedures).

### 5. Generate Test Suite
Create: unit tests (SLO calculation logic, quality rule validation, alert threshold tests), integration tests (end-to-end monitoring, quality validation pipelines, lineage tracking), SLO tests (error budget burn validation, breach detection, recovery tracking), quality tests (rule execution, schema evolution, anomaly detection), incident tests (runbook execution, recovery procedures, escalation workflows), synthetic probes (deliberate failures, delay injection, quality violations).

### 6. Add Recommendations
Include: continuous SLO monitoring, automated quality validation, incident drills, capacity planning, performance baselining.

### 7. Validate and Report
Execute: `pytest tests/ --junitxml=results.xml --cov --cov-report=html`
Generate test report. Report completion.

## Error Handling
**SLO Test Failures**: Document gaps and define missing targets.
**Quality Rule Failures**: Fix validation logic or data issues.

## Examples
**Example 1**: `/test-data-reliability Validate SLO framework for data platform` - Output: Complete test suite with error budget validation
**Example 2**: `/test-data-reliability Test data quality rules for production tables` - Output: Quality validation suite with schema contract tests

## References
