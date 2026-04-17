---
description: Debug data quality validation failures (Quality Guardian)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-validation --json ` and parse for VALIDATION_FRAMEWORK, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-validation/templates/env-config.yaml` for debugging tools

### 3. Parse Input
Extract from $ARGUMENTS: validation failure details, affected datasets, expectations failed. Request clarification if incomplete.

### 4. Diagnose Issue
Analyze validation failures, data quality issues, threshold breaches, expectation configuration problems.

### 5. Generate Fix Recommendations
Provide remediation for data issues, expectation adjustments, threshold tuning, pipeline fixes.

### 6. Add Prevention Measures
Recommend proactive quality monitoring, upstream validation, data profiling.

### 7. Validate and Report
Generate debug report. Report completion.

## Error Handling
**Critical Quality Failures**: Escalate and halt downstream processing.
**False Positives**: Adjust expectations based on data characteristics.

## Examples
**Example 1**: `/debug-data-validation Completeness expectation failing` - Output: Analysis with data issue remediation
**Example 2**: `/debug-data-validation Validation suite execution timeout` - Output: Performance optimization

## References
