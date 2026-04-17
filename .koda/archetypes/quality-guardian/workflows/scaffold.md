---
description: Generate data quality validation suite with Great Expectations/Deequ and threshold enforcement (Quality Guardian)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype quality-guardian --json ` and parse for QUALITY_FRAMEWORK, DATA_SOURCE, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/quality-guardian/templates/env-config.yaml` for framework (GE/Deequ), thresholds, alert channels

### 3. Parse Input
Extract from $ARGUMENTS: data source and schema, quality rules (nullability/uniqueness/range/pattern), thresholds for failures, alerting requirements. Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse quality checks without fail-fast on critical breaches
- ✘ Refuse missing baseline expectations
- ✘ Refuse no alerting on quality failures
- ✘ Refuse checks without documentation
If violated, explain clearly and suggest compliant alternative.

### 5. Generate Quality Suite

Create quality validation suite with structure: framework initialization (Great Expectations or Deequ), data source configuration, expectation suite definition with rules, validation execution with threshold checking, result reporting with pass/fail status, alerting integration for failures, documentation generation.

Quality check patterns: schema validation (column presence, types), nullability checks (expect_column_values_to_not_be_null), uniqueness checks (expect_column_values_to_be_unique), range checks (expect_column_values_to_be_between), pattern checks (expect_column_values_to_match_regex), referential integrity (expect_column_values_to_be_in_set), statistical checks (mean, stddev, distribution), custom business rules.

Threshold enforcement: critical checks (fail immediately on breach), warning checks (log but continue), trend monitoring (compare to baseline), anomaly detection (statistical outliers), data profiling (automatic expectation generation).

Apply mandatory patterns: fail-fast on critical breaches, baseline expectations from profiling, structured result reporting, alert integration (email/Slack/PagerDuty), documentation with check descriptions, threshold configuration from YAML, execution logging with metrics.

### 6. Add Recommendations

Include comments for: automated expectation generation from profiling, incremental validation for large datasets, checkpoint configuration for state management, data docs generation, integration with CI/CD.

### 7. Validate and Report


Generate optional pytest integration tests. Report completion with file paths, check summary, execution commands, next steps.

## Error Handling

**Hard-Stop Violations**: Explain violation (e.g., missing fail-fast), suggest compliant alternative with threshold configuration.

**Incomplete Input**: List missing information (data schema, quality rules, thresholds), provide well-formed example.

**Environment Failure**: Report missing Great Expectations or Deequ setup, suggest installation steps.

## Examples

**Customer Data**: `/scaffold-quality Validate customer table: no null IDs, unique emails, age 18-120, valid phone patterns, fail on critical breaches`
Output: GE suite with 5 expectations, threshold config, fail-fast logic, alert integration.

**Sales Metrics**: `/scaffold-quality Check daily sales: revenue >$0, order count >0, avg order $10-$10000, compare to 7-day baseline`
Output: GE suite with range checks, statistical validation, baseline comparison, trending.

**ML Features**: `/scaffold-quality Validate feature store: no nulls in required features, distributions match training, detect drift >10%`
Output: Deequ suite with completeness checks, distribution validation, drift detection.

## References

