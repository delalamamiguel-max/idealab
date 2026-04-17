---
description: Generate performance test harness and benchmarks (Performance Tuner)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype performance-tuner --json ` and parse for PROFILER_TOOLS, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/performance-tuner/templates/env-config.yaml` for test configuration

### 3. Parse Input
Extract from $ARGUMENTS: code file path, testing framework (pytest-benchmark, locust), performance goals (latency, throughput, resource usage), baseline metrics. Request clarification if incomplete.

### 4. Analyze Code

Identify performance-critical components: hot paths and bottlenecks, resource-intensive operations, I/O operations, algorithms and data structures. Determine test scenarios: benchmark tests (execution time, memory usage), load tests (concurrent requests, throughput), stress tests (resource limits, breaking points), regression tests (compare to baseline). Report test coverage plan.

### 5. Generate Test Suite

Create performance test suite with benchmark fixtures, baseline metrics, unit benchmarks (function-level), load tests (concurrent execution), stress tests (resource limits), regression tests (compare to baseline). Include complete test code with metrics collection.

### 6. Add Recommendations

Include recommendations for test execution (run on consistent hardware, use realistic data), CI/CD integration (track performance trends, alert on regressions), profiling (identify hotspots, optimize critical paths), monitoring (track production metrics). Provide summary.

### 7. Validate and Report


## Error Handling

**No Baseline Metrics**: Suggest establishing baseline first.

**Insufficient Load Specs**: Request expected load characteristics.

**Missing Profiling Data**: Recommend profiling tools.

## Examples

**Example 1**: `/test-performance Generate benchmarks for data_processor.py` - Output: Execution time and memory benchmarks

**Example 2**: `/test-performance Create load tests for api_handler.py` - Output: Concurrent request tests

**Example 3**: `/test-performance Add regression tests for query_engine.py` - Output: Performance comparison tests

## References

