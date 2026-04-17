---
description: Debug performance issues and bottlenecks (Performance Tuner)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype performance-tuner --json ` and parse for PROFILER_TOOLS, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/performance-tuner/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: code file path, performance issue description (slow, high CPU, memory leak), baseline metrics, profiling data, context. Request clarification if incomplete.

### 4. Analyze Problem

Identify performance issue category: CPU bottlenecks (inefficient algorithms, excessive computation), memory issues (leaks, excessive allocation, fragmentation), I/O bottlenecks (disk, network, database), concurrency issues (locks, race conditions, thread starvation). Analyze profiling data, metrics, and code patterns. Report findings with hotspots, resource usage, root cause.

### 5. Generate Fix

Create optimized code addressing bottleneck: optimize algorithms (better complexity, caching), fix memory issues (proper cleanup, streaming, pooling), optimize I/O (batching, async, connection pooling), fix concurrency (reduce locks, optimize parallelism). Include complete fixed code with performance annotations and measurement hooks.

### 6. Add Recommendations

Include recommendations for prevention (performance testing, profiling, monitoring), testing (load tests, stress tests, benchmarks), monitoring (performance metrics, alerting, dashboards). Provide summary with baseline vs optimized metrics, cost impact.

### 7. Validate and Report


## Error Handling

**Insufficient Profiling Data**: Request profiling information or suggest profiling tools.

**Cannot Reproduce**: Request environment details, load characteristics, and test data.

**Multiple Bottlenecks**: Prioritize by impact and provide systematic optimization approach.

## Examples

**Example 1: Slow Query**
```
/debug-performance Database query taking 30 seconds

Root Cause: Full table scan on 50M rows, missing index
Fix: Added composite index, query rewrite, reduced to 2 seconds
```

**Example 2: Memory Leak**
```
/debug-performance Application memory growing from 500MB to 8GB over 24 hours

Root Cause: Cache not evicting old entries, unbounded growth
Fix: Implemented LRU cache with size limit, memory stable at 800MB
```

**Example 3: High CPU**
```
/debug-performance CPU at 100% during data processing

Root Cause: O(n²) algorithm for matching, inefficient for large datasets
Fix: Replaced with hash-based O(n) algorithm, CPU reduced to 20%
```

## References

