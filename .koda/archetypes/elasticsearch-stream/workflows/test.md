---
description: Validate Elasticsearch streaming pipeline for performance and reliability (Elasticsearch Stream)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype elasticsearch-stream --json ` and parse for ES_ENDPOINT, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/elasticsearch-stream/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: pipeline location, test scope, acceptance criteria. Request clarification if incomplete.

### 4. Analyze Test Requirements
Identify testable components: indexing logic, error handling, performance, reliability.

### 5. Generate Test Suite
Create: unit tests, integration tests, performance tests, load tests, failover tests.

### 6. Add Recommendations
Include testing best practices, continuous validation, performance baselining.

### 7. Validate and Report
Execute: `pytest tests/ --junitxml=results.xml --cov --cov-report=html`
Generate report. Report completion.

## Error Handling
**Test Cluster Unavailable**: Use test Elasticsearch instance or Docker.
**Performance Variance**: Run multiple iterations and average results.

## Examples
**Example 1**: `/test-elasticsearch-stream Validate streaming pipeline performance` - Output: Performance test suite with benchmarks
**Example 2**: `/test-elasticsearch-stream Test error handling and retries` - Output: Reliability test suite with failure scenarios

## References
