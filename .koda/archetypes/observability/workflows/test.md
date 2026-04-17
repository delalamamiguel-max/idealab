---
description: Generate test harness for observability implementation validation and telemetry quality (Observability)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json ` and parse for OTEL_COLLECTOR_ENDPOINT, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/observability/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: instrumented code location, test scope (unit, integration, E2E, signal quality, compliance), acceptance criteria, test environment. Request clarification if incomplete.

### 4. Analyze Test Requirements

Identify testable components: instrumentation (trace span creation, metric emission, log correlation, resource attributes), trace propagation (W3C context injection, cross-service correlation, span parent-child relationships), telemetry pipeline (export configuration, collector connectivity, batch processing, retry logic), signal quality (RED metrics completeness, span semantics, log structure, cardinality), compliance (PII redaction, required metadata, structured format).

Define test scenarios: unit tests (span creation logic, metric instrumentation, log formatting, resource attributes), integration tests (trace propagation across services, end-to-end correlation, telemetry export validation), signal quality tests (RED metrics validation, semantic convention compliance, cardinality checks, sampling effectiveness), compliance tests (PII redaction verification, metadata completeness, structured format validation), performance tests (instrumentation overhead, export latency, concurrent telemetry generation).

### 5. Generate Test Suite

Create comprehensive test suite with unit tests (mock span processor tests, metric instrument tests, log formatter tests, attribute validation), integration tests (multi-service trace propagation, collector export tests, backend ingestion validation), signal quality tests (RED metrics verification, span semantic tests, cardinality validation, sampling coverage), compliance tests (PII scanner tests, metadata presence checks, format validation), performance tests (overhead benchmarks, export performance, load testing).

Include test fixtures, mock collector, telemetry validators.

### 6. Add Recommendations

Include testing best practices: automated telemetry validation, signal quality gates in CI/CD, compliance scanning, performance baselining, continuous monitoring of test coverage.

Provide test execution commands.

### 7. Validate and Report


Execute test suite: `pytest tests/ --junitxml=results.xml --cov --cov-report=html`

Generate test report with pass/fail summary, signal quality metrics, compliance validation, performance benchmarks. Report completion.

## Error Handling

**Collector Unavailable**: Use mock collector or provide setup instructions.

**Signal Quality Issues**: Document gaps and provide remediation.

**Performance Overhead**: Benchmark and optimize instrumentation.

## Examples

**Example 1**: `/test-observability Validate OpenTelemetry instrumentation for order-service` - Output: Complete test suite with trace, metric, and log validation

**Example 2**: `/test-observability Test trace propagation across React and FastAPI` - Output: End-to-end correlation tests with W3C header validation

**Example 3**: `/test-observability Validate PII redaction in telemetry` - Output: Compliance test suite ensuring no sensitive data leakage

## References

