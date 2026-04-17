---
description: Refactor code to apply performance optimization patterns and eliminate bottlenecks (Performance Tuner)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype performance-tuner --json ` and parse for PROFILER_TOOLS, DB_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/performance-tuner/templates/env-config.yaml` for performance thresholds, optimization targets

### 3. Parse Input
Extract from $ARGUMENTS: existing code file path, performance issue description (slow query, memory leak, high CPU), profiling data if available, optimization goals. Request clarification if incomplete.

### 4. Analyze Existing Code
Load and analyze code for performance issues: identify bottlenecks (N+1 queries, full table scans, missing indexes, inefficient algorithms, memory leaks, excessive I/O), measure baseline performance (execution time, memory usage, CPU utilization, I/O operations), identify optimization opportunities (caching, indexing, query optimization, algorithm improvements, parallelization).

Report findings with line numbers, performance metrics, and estimated impact.

### 5. Generate Refactored Code

Create refactored code applying optimizations: fix bottlenecks (add indexes, optimize queries, fix N+1 problems, improve algorithms, reduce I/O), implement caching strategies, add connection pooling, optimize data structures, implement parallelization where appropriate.

Include performance annotations and measurement hooks.

### 6. Add Recommendations

Include inline comments for monitoring (performance metrics, profiling hooks, alerting thresholds), further optimizations (advanced caching, query plan optimization, hardware scaling), testing strategies (load testing, stress testing, performance regression tests).

Provide summary with baseline vs optimized metrics and cost impact.

### 7. Validate and Report


Generate performance comparison report. Report completion with metrics, improvements, next steps.

## Error Handling

**Insufficient Profiling Data**: Request profiling information or suggest profiling tools to run.

**Incomplete Input**: List missing information, provide well-formed example with performance metrics.

**Environment Failure**: Report missing profiling tools, suggest installation.

## Examples

**Example 1: Query Optimization**
```
/refactor-performance Optimize slow SQL query in customer_report.sql

Input: Query with full table scan, 30s execution time
Output: Refactored with indexes, query rewrite, 2s execution time
```

**Example 2: Memory Optimization**
```
/refactor-performance Fix memory leak in data_processor.py

Input: Process consuming 8GB RAM, growing over time
Output: Refactored with proper cleanup, streaming, 500MB stable memory
```

**Example 3: Algorithm Improvement**
```
/refactor-performance Improve O(n²) algorithm in matching_engine.py

Input: Slow matching taking 5 minutes for 10K records
Output: Refactored with O(n log n) algorithm, 5 seconds for 10K records
```

## References

