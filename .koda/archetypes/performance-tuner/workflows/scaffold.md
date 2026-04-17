---
description: Analyze query plans or Spark jobs, identify bottlenecks, and recommend optimizations (Performance Tuner)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype performance-tuner --json ` and parse for QUERY_ENGINE, ANALYSIS_TOOLS, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/performance-tuner/templates/env-config.yaml` for performance targets, cost thresholds

### 3. Parse Input
Extract from $ARGUMENTS: query or job to analyze, current performance metrics (runtime/cost/resource usage), performance targets, optimization constraints. Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse analysis without baseline metrics
- ✘ Refuse recommendations without cost/benefit analysis
- ✘ Refuse optimizations that break functionality
- ✘ Refuse changes without testing strategy
If violated, explain clearly and suggest compliant alternative.

### 5. Perform Analysis

Execute performance analysis with phases: collect baseline metrics (runtime, data scanned, shuffle size, memory usage), analyze execution plan (EXPLAIN ANALYZE for SQL, Spark UI for jobs), identify bottlenecks (full table scans, large shuffles, skewed partitions, inefficient joins), calculate cost impact (compute time × cluster cost), prioritize optimizations by ROI.

SQL analysis patterns: identify missing indexes, detect full table scans, find inefficient joins (nested loop vs hash), check partition pruning effectiveness, analyze statistics freshness, detect implicit conversions, find redundant operations.

Spark analysis patterns: identify shuffle bottlenecks, detect data skew in partitions, find broadcast join opportunities, analyze stage dependencies, check caching effectiveness, detect spill to disk, find narrow vs wide transformations.

Optimization recommendations: indexing strategies (B-tree, bitmap, covering), partition pruning (add filters, partition by date), join optimization (broadcast small tables, sort-merge for large), caching strategies (cache reused DataFrames), parallelism tuning (adjust shuffle partitions), resource allocation (executor memory, cores).

Apply mandatory patterns: baseline metrics collection, execution plan analysis, bottleneck identification with evidence, cost-benefit calculation for each recommendation, testing strategy for validation, rollback plan for failures.

### 6. Generate Report

Create analysis report with sections: executive summary (current vs target performance), baseline metrics table, bottleneck analysis with evidence, prioritized recommendations with ROI, implementation plan with testing, cost savings projection, monitoring strategy.

### 7. Validate and Report


Generate optional benchmark scripts for before/after comparison. Report completion with analysis file, top recommendations, estimated savings, next steps.

## Error Handling

**Hard-Stop Violations**: Explain violation (e.g., missing baseline), suggest compliant alternative with metrics collection.

**Incomplete Input**: List missing information (query/job, current metrics, targets), provide well-formed example.

**Environment Failure**: Report missing analysis tools (EXPLAIN, Spark UI), suggest setup steps.

## Examples

**Slow SQL Query**: `/analyze-performance Analyze customer aggregation query taking 10 minutes, target <1 minute, Snowflake warehouse LARGE`
Output: Analysis report with execution plan, identified full table scan, recommendation for clustering key, projected 90% speedup.

**Spark Job Bottleneck**: `/analyze-performance Analyze daily ETL job taking 4 hours, target <1 hour, 100GB data, 10-node cluster`
Output: Analysis report with shuffle bottleneck identified, recommendation for broadcast join and partition tuning, projected 75% speedup.

**Cost Optimization**: `/analyze-performance Analyze monthly reporting queries costing $5000, target <$2000, identify optimization opportunities`
Output: Analysis report with cost breakdown, recommendations for materialized views and query rewrites, projected 60% cost reduction.

## References

