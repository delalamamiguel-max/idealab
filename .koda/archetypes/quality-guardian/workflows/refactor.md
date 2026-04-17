---
description: Refactor data quality suite to enhance validation coverage and enforcement (Quality Guardian)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype quality-guardian --json ` and parse for GE_VERSION, DEEQU_VERSION, PYTHON_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/quality-guardian/templates/env-config.yaml` for thresholds, validation rules, alert settings

### 3. Parse Input
Extract from $ARGUMENTS: existing quality suite file path or inline config, refactoring goals (add checks, enhance thresholds, improve coverage, add profiling), constraints. Request clarification if incomplete.

### 4. Analyze Existing Code
Load and analyze existing quality suite:
- Identify hard-stop rule violations (missing schema validation, no null checks on critical fields, missing uniqueness constraints, no referential integrity checks, missing range validations, no pattern matching, missing completeness checks)
- Identify missing mandatory patterns (comprehensive expectation suite, parameterized thresholds, failure action configuration, data profiling, checkpoint configuration, validation result storage, alert integration)
- Identify opportunities for preferred patterns (statistical checks, distribution analysis, anomaly detection, custom expectations, data lineage tracking, quality dashboards)

Report findings with expectation names and coverage gaps.

### 5. Generate Refactored Quality Suite

Create refactored quality suite applying hard-stop fixes (add schema expectations, implement null checks, add uniqueness constraints, validate referential integrity, add range validations, implement pattern matching, add completeness checks), mandatory patterns (comprehensive expectation suite, parameterized thresholds from config, failure actions, profiling configuration, checkpoint setup, result storage), and preferred patterns (statistical validations, distribution checks, anomaly detection, custom expectations, quality metrics).

Include complete code example with Great Expectations or Deequ configuration, expectation definitions, and validation execution.

### 6. Add Recommendations

Include inline comments for coverage (additional field validations, cross-field checks, temporal validations), automation (CI/CD integration, scheduled validation, auto-remediation), monitoring (quality dashboards, trend analysis, alerting rules), and optimization (sampling strategies, incremental validation, performance tuning).

Provide summary of improvements with coverage enhancements and quality impact.

### 7. Validate and Report


Generate optional data profiling report and quality dashboard config. Report completion with file paths, applied improvements, coverage metrics, next steps.

## Error Handling

**Hard-Stop Violations in Original**: Explain each violation clearly (e.g., "Missing null check on customer_id field"), show compliant alternative with expectation configuration.

**Incomplete Input**: List missing information (suite file path or config, refactoring goals, constraints), provide well-formed example.

**Environment Failure**: Report missing Great Expectations or Deequ installation, suggest setup steps and configuration.

## Examples

**Example 1: Add Statistical Checks**
```
/refactor-quality Add min/max range checks to sales_suite.yaml for amount fields

Input: Basic suite with schema checks only
Output: Refactored with statistical expectations, parameterized thresholds, distribution checks
```

**Example 2: Enhance Coverage**
```
/refactor-quality Add regex pattern validation and uniqueness checks to customer_suite.yaml

Input: Suite with limited field coverage
Output: Refactored with pattern matching, uniqueness constraints, referential integrity checks
```

**Example 3: Improve Enforcement**
```
/refactor-quality Configure failure actions and alerting in order_validation.py

Input: Suite without failure handling
Output: Refactored with critical failure actions, alert integration, validation result storage
```

## References

