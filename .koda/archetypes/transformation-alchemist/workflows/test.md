---
description: Generate test harness for PySpark/Scala transformations (Transformation Alchemist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype transformation-alchemist --json ` and parse for SPARK_VERSION, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/transformation-alchemist/templates/env-config.yaml` for test configuration

### 3. Parse Input
Extract from $ARGUMENTS: PySpark/Scala file path, testing framework (pytest, unittest), coverage goals (unit, integration, data quality), test data requirements. Request clarification if incomplete.

### 4. Analyze Code

Identify testable components: transformation functions, DataFrame operations, data quality checks, merge/upsert logic, aggregations. Determine test scenarios: unit tests (function-level), integration tests (end-to-end), data quality tests (schema, nulls, duplicates), performance tests (execution time, memory). Report test coverage plan.

### 5. Generate Test Suite

Create pytest test suite with Spark session fixtures, sample DataFrames, unit tests for transformations, integration tests for pipelines, data quality assertions, performance benchmarks. Include complete test code with assertions and cleanup.

### 6. Add Recommendations

Include recommendations for test data (use small datasets, create reusable fixtures), CI/CD integration (run on PR, track coverage), performance testing (benchmark critical paths), data quality (validate schemas, check constraints). Provide summary.

### 7. Validate and Report


## Error Handling

**Insufficient Code**: Request complete transformation code.

**No Test Data**: Provide guidance on creating sample DataFrames.

**Framework Issues**: Suggest pytest with pyspark-test or chispa.

## Examples

**Example 1**: `/test-spark Generate tests for customer_transform.py` - Output: 15 tests with DataFrame assertions

**Example 2**: `/test-spark Create data quality tests for sales_pipeline.py` - Output: Schema and quality validation tests

**Example 3**: `/test-spark Add performance tests for aggregation.py` - Output: Benchmark tests with thresholds

## References

