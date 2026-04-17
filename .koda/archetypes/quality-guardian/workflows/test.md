---
description: Generate test harness for data quality suites (Quality Guardian)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype quality-guardian --json ` and parse for GE_VERSION, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/quality-guardian/templates/env-config.yaml` for test configuration

### 3. Parse Input
Extract from $ARGUMENTS: quality suite file, testing framework (pytest), coverage goals (expectation validation, threshold testing), test scenarios. Request clarification if incomplete.

### 4. Analyze Code

Identify testable components: expectations and validations, thresholds and parameters, data profiling logic, checkpoint configuration. Determine test scenarios: expectation tests (validate logic), threshold tests (boundary values), integration tests (full validation runs), performance tests (validation speed). Report test coverage plan.

### 5. Generate Test Suite

Create pytest test suite with sample data fixtures, expectation validation tests, threshold boundary tests, integration tests with Great Expectations/Deequ, performance tests. Include complete test code.

### 6. Add Recommendations

Include recommendations for test data (create diverse samples, include edge cases), CI/CD integration (validate suites on PR), coverage improvements (test all expectations, validate thresholds), monitoring (track validation performance). Provide summary.

### 7. Validate and Report


## Error Handling

**Insufficient Suite Info**: Request complete quality suite configuration.

**No Test Data**: Provide guidance on creating sample datasets.

**Framework Issues**: Suggest pytest with Great Expectations integration.

## Examples

**Example 1**: `/test-quality Generate tests for sales_suite.yaml` - Output: 15 tests validating expectations

**Example 2**: `/test-quality Create threshold tests for customer_validation.py` - Output: Boundary value tests

**Example 3**: `/test-quality Add integration tests for quality_pipeline.py` - Output: End-to-end validation tests

## References

