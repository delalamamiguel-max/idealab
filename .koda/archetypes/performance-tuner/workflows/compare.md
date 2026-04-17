---
description: Compare performance optimization approaches and architectures (Performance Tuner)
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
Extract from $ARGUMENTS: performance problem, comparison criteria (latency, throughput, cost, complexity), baseline metrics, constraints. Request clarification if incomplete.

### 4. Generate Alternatives

Create 2-3 optimization approaches: Caching strategy, Algorithm optimization, Architecture scaling. Each with implementation details, performance projections, cost implications.

### 5. Generate Comparison Matrix

Compare on: performance improvement, cost, implementation complexity, operational overhead, scalability, risk. Provide metrics and ROI analysis.

### 6. Add Recommendations

Recommend approach with justification. Include implementation plan, performance testing strategy, rollback plan, monitoring setup.

### 7. Validate and Report


## Error Handling

**Insufficient Metrics**: Request baseline performance data and requirements.

**Unclear Bottleneck**: Suggest profiling to identify root cause.

**Cost Ambiguity**: Clarify budget constraints and ROI expectations.

## Examples

**Example 1**: `/compare-performance Compare caching vs database optimization` - Output: Strategy comparison with cost-benefit analysis

**Example 2**: `/compare-performance Vertical vs horizontal scaling for API` - Output: Architecture comparison with cost projections

**Example 3**: `/compare-performance Compare indexing strategies for query performance` - Output: Index comparison with query pattern analysis

## References

