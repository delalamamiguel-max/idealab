---
description: Generate test harness for data quality suites (Quality Guardian)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-validation --json ` and parse for VALIDATION_FRAMEWORK, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-validation/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: validation suite location, test scope, acceptance criteria. Request clarification if incomplete.

### 4. Analyze Test Requirements
Identify testable components: expectations, thresholds, execution logic, alerting, reporting.

### 5. Generate Test Suite
Create validation tests: expectation unit tests, integration tests, performance tests, threshold validation.

### 6. Add Recommendations
Include testing best practices, continuous validation, quality regression detection.

### 7. Validate and Report
Execute: `pytest tests/ --junitxml=results.xml --cov --cov-report=html`
Generate report. Report completion.

## Error Handling
**Test Data Unavailable**: Use synthetic data or data samples.
**Validation Failures**: Document and remediate quality issues.

## Examples
**Example 1**: `/test-data-validation Validate quality suite for customer data` - Output: Test suite with expectation validation
**Example 2**: `/test-data-validation Test validation threshold configuration` - Output: Threshold tests with tuning recommendations

## References
