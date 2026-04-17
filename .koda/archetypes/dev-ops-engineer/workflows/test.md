---
description: Generate integration tests for multi-archetype solution (Dev Ops Engineer)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype dev-ops-engineer --json ` and parse for CI_TOOL, ORCHESTRATOR, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/dev-ops-engineer/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: deployment artifacts location (CI/CD config, DAG, workflow), test scope (unit, integration, E2E, quality gates, performance), acceptance criteria, target environment. Request clarification if incomplete.

### 4. Analyze Test Requirements

Identify testable components: CI/CD pipeline (stage execution, gate validation, artifact generation), orchestration logic (task dependencies, retry behavior, error handling), deployment process (environment promotion, rollback procedures, configuration management), data quality gates (validation rules, schema checks, freshness monitoring), security controls (secret scanning, vulnerability checks, access validation), observability (metrics emission, log structured, alert configuration).

Define test scenarios: unit tests (configuration validation, policy rule testing, script logic), integration tests (end-to-end deployment workflow, orchestration execution, quality gate validation), E2E tests (full pipeline deployment and execution, rollback validation, monitoring verification), performance tests (deployment speed, pipeline execution time, resource utilization), chaos tests (failure injection, recovery validation, rollback effectiveness).

### 5. Generate Test Suite

Create comprehensive test suite with unit tests (pytest for pipeline logic, configuration validation tests, policy gate tests), integration tests (deployment workflow tests, orchestration integration tests, quality gate validation), E2E tests (full deployment scenarios, rollback procedures, disaster recovery), security tests (secret scanning validation, vulnerability assessment, access control tests), performance tests (DORA metrics validation, SLO compliance tests, resource efficiency tests), CI integration (automated test execution, test data management, environment provisioning).

Include test fixtures, mock services, test data generators.

### 6. Add Recommendations

Include testing best practices: automated testing in CI/CD, test environment management, continuous validation, failure simulation, DORA metrics tracking, test coverage monitoring.

Provide test execution commands and expected results.

### 7. Validate and Report


Execute test suite: `pytest tests/ --junitxml=results.xml --cov --cov-report=html`

Generate test report with pass/fail summary, coverage metrics, quality validation, DORA metrics. Report completion.

## Error Handling

**Test Environment Unavailable**: Provide environment setup instructions.

**Quality Gate Failures**: Document violations and remediation steps.

**Performance Issues**: Benchmark and identify bottlenecks.

## Examples

**Example 1**: `/test-dev-ops Validate customer pipeline deployment workflow` - Output: Complete test suite with quality and security validation

**Example 2**: `/test-dev-ops Create E2E tests for analytics DAG deployment` - Output: End-to-end tests with rollback validation

**Example 3**: `/test-dev-ops Generate performance tests for production deployment` - Output: Performance test suite with DORA metrics tracking

## References

