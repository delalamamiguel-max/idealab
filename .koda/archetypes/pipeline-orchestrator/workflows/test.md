---
description: Generate test harness for Airflow/TWS DAGs (Pipeline Orchestrator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype pipeline-orchestrator --json ` and parse for AIRFLOW_VERSION, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/pipeline-orchestrator/templates/env-config.yaml` for test configuration

### 3. Parse Input
Extract from $ARGUMENTS: DAG file path, testing framework (pytest), coverage goals (DAG structure, task execution, dependencies), test scenarios. Request clarification if incomplete.

### 4. Analyze Code

Identify testable components: DAG structure and configuration, task definitions, dependencies and order, operators and parameters, callbacks and SLAs. Determine test scenarios: DAG validation tests, task unit tests, dependency tests, integration tests, failure scenario tests. Report test coverage plan.

### 5. Generate Test Suite

Create pytest test suite with Airflow test fixtures, DAG validation tests, task unit tests with mocking, dependency verification, integration tests, failure handling tests. Include complete test code.

### 6. Add Recommendations

Include recommendations for test execution (use test DAG runs, mock external dependencies), CI/CD integration (validate DAGs on PR, test backfills), coverage improvements (test all failure paths, validate SLAs). Provide summary.

### 7. Validate and Report


## Error Handling

**Insufficient Code**: Request complete DAG file.

**No Test Environment**: Provide Airflow test setup instructions.

**Missing Mocks**: Suggest mocking strategies for operators.

## Examples

**Example 1**: `/test-pipeline Generate tests for etl_dag.py` - Output: 12 tests covering DAG structure and tasks

**Example 2**: `/test-pipeline Create integration tests for data_pipeline_dag.py` - Output: End-to-end DAG execution tests

**Example 3**: `/test-pipeline Add failure tests for critical_dag.py` - Output: Tests for error handling and retries

## References

