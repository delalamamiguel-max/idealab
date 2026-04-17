---
description: Debug data quality validation failures (Quality Guardian)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype quality-guardian --json ` and parse for GE_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/quality-guardian/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: quality suite file, expectation name, error message (validation failed, unexpected values), symptoms (checks failing, false positives), context (data source, validation run). Request clarification if incomplete.

### 4. Analyze Problem

Identify error category: expectation failures (data quality issues vs expectation issues), configuration errors (wrong thresholds, incorrect expectations), data issues (schema changes, data anomalies), framework errors (Great Expectations/Deequ errors). Analyze validation results, data samples, and expectation configuration. Report findings with expectation name, failure details, root cause.

### 5. Generate Fix

Create fix addressing root cause: fix data issues (data cleaning, transformation fixes), fix expectations (adjust thresholds, correct logic), fix configuration (update parameters, fix suite setup), add missing validations (new expectations, edge cases). Include complete fixed suite with proper thresholds and documentation.

### 6. Add Recommendations

Include recommendations for prevention (data profiling, expectation testing, monitoring), testing (test with historical data, edge cases, schema changes), monitoring (quality dashboards, trend analysis, alerts). Provide summary with root cause, fix, data quality impact.

### 7. Validate and Report


## Error Handling

**Insufficient Error Information**: Request validation results, data samples, and expectation configuration.

**Cannot Reproduce**: Request data source, validation environment, and configuration.

**Multiple Possible Causes**: Provide systematic debugging with data profiling.

## Examples

**Example 1: False Positive**
```
/debug-quality Null check failing but data looks valid

Root Cause: Expectation checking wrong column due to typo
Fix: Corrected column name in expectation configuration
```

**Example 2: Threshold Too Strict**
```
/debug-quality Max value check failing on legitimate data

Root Cause: Threshold set to 1000 but valid values go to 5000
Fix: Adjusted threshold to 10000 based on data profiling, added monitoring
```

**Example 3: Schema Change**
```
/debug-quality All expectations failing after data source update

Root Cause: Column renamed in source system
Fix: Updated expectation suite with new column names, added schema validation
```

## References

