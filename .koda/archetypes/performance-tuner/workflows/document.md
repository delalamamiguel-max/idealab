---
description: Generate documentation for performance optimizations and architecture (Performance Tuner)
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
Extract from $ARGUMENTS: system/code to document, target audience, documentation scope (performance guide, architecture, tuning guide). Request clarification if incomplete.

### 4. Analyze Code/System

Analyze performance: identify performance characteristics, document optimization strategies, explain architecture decisions, note bottlenecks and solutions, identify monitoring metrics, document scaling strategies.

### 5. Generate Documentation

Create comprehensive documentation with: performance overview and benchmarks, architecture diagrams with performance considerations, optimization guide, monitoring and alerting setup, capacity planning guide, troubleshooting performance issues.

Include README.md, architecture diagrams, performance runbook, tuning guide.

### 6. Add Recommendations

Include recommendations for documentation maintenance, performance monitoring, capacity planning, optimization opportunities, load testing procedures.

### 7. Validate and Report


Generate documentation artifacts. Report completion.

## Error Handling

**Insufficient Metrics**: Request baseline performance data and requirements.

**Complex System**: Break documentation by component or layer.

**Missing Benchmarks**: Request performance testing results.

## Examples

**Example 1**: `/document-performance Create docs for caching strategy` - Output: Architecture docs with caching patterns and performance impact

**Example 2**: `/document-performance Generate performance tuning guide` - Output: Tuning guide with optimization techniques and benchmarks

**Example 3**: `/document-performance Document scaling architecture` - Output: Architecture docs with scaling strategies and capacity planning

## References

