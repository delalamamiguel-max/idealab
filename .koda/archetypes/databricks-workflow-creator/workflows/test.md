---
description: Test Databricks workflow for governance, reproducibility, and collaborative audit trail compliance (Databricks Workflow Creator)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype databricks-workflow-creator --json ` and parse for DATABRICKS_HOST, DATABRICKS_TOKEN, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/databricks-workflow-creator/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: workflow location (job ID, notebooks, DLT pipeline), test scope (unit, integration, E2E, data quality, governance), acceptance criteria, test environment. Request clarification if incomplete.

### 4. Analyze Test Requirements

Identify testable components: notebook logic (transformation functions, business logic, error handling), DLT pipeline (expectations, schema evolution, streaming logic), workflow configuration (task dependencies, retry policies, timeouts), Unity Catalog integration (permissions, lineage, metadata), data quality (expectations, validation rules, anomaly detection), cluster configuration (policies, sizing, cost controls).

Define test scenarios: unit tests (notebook functions, transformation logic, validation rules), integration tests (end-to-end pipeline execution, data quality validation, Unity Catalog integration), governance tests (permission checks, lineage validation, audit logging), performance tests (query optimization, cluster efficiency, cost validation), resilience tests (retry behavior, error recovery, checkpoint management).

### 5. Generate Test Suite

Create comprehensive test suite with unit tests (pytest for notebook functions, data transformation tests, validation logic tests), integration tests (workflow execution in test workspace, DLT pipeline validation, Unity Catalog integration tests), data quality tests (expectation validation, schema evolution tests, anomaly detection validation), governance tests (RBAC validation, secret access tests, audit log verification), performance tests (query performance benchmarks, cost tracking, DBU consumption validation), CI/CD integration (automated test execution, test data management, environment provisioning).

Include test fixtures, mock data, test workspace setup.

### 6. Add Recommendations

Include testing best practices: automated testing in CI/CD, test data management and isolation, staging workspace validation, cost monitoring for tests, continuous governance validation, test coverage metrics.

Provide test execution commands and expected runtime.

### 7. Validate and Report


Execute test suite: `pytest tests/ --junitxml=results.xml --cov --cov-report=html`

Generate test report with pass/fail summary, coverage metrics, data quality results, governance validation, cost analysis. Report completion.

## Error Handling

**Test Workspace Unavailable**: Provide workspace setup instructions.

**Data Quality Failures**: Document expectation violations and remediation.

**Permission Issues**: Verify service principal grants for test execution.

## Examples

**Example 1**: `/test-databricks-workflow Validate customer_data DLT pipeline for production promotion` - Output: Complete test suite with governance and quality validation

**Example 2**: `/test-databricks-workflow Create integration tests for sales analytics workflow` - Output: End-to-end tests with Unity Catalog validation

**Example 3**: `/test-databricks-workflow Generate data quality tests for bronze layer ingestion` - Output: Expectation-based test suite with anomaly detection

## References

