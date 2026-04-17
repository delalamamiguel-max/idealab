---
description: Debug observability issues including missing traces, metric gaps, and telemetry pipeline failures (Observability)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json ` and parse for OTEL_COLLECTOR_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/observability/templates/env-config.yaml` for debugging tools

### 3. Parse Input
Extract from $ARGUMENTS: failure type (missing traces, broken correlation, metric gaps, high cardinality), error messages, service name, affected components. Request clarification if incomplete.

### 4. Diagnose Issue

Run diagnostic checks: Trace Issues (W3C context propagation validation, span creation verification, sampling configuration check, collector connectivity test), Metric Problems (RED metrics validation, cardinality analysis, aggregation verification, export configuration check), Log Correlation (trace_id and span_id presence, structured format validation, log level configuration), Telemetry Pipeline (collector health check, export endpoint validation, TLS configuration, batch processing verification), Performance Impact (instrumentation overhead, sampling rate validation, cardinality optimization).

Provide diagnostic report with root cause.

### 5. Generate Fix Recommendations

Provide targeted fixes: for missing traces (fix context propagation, enable instrumentation, adjust sampling), for correlation issues (add trace_id to logs, fix span linkage, validate headers), for metric gaps (add missing instrumentation, fix cardinality, configure aggregation), for pipeline failures (fix collector config, validate endpoints, resolve TLS issues), for performance (optimize sampling, reduce cardinality, adjust batch sizes).

Include code fixes and configuration changes.

### 6. Add Prevention Measures

Recommend improvements: automated telemetry validation, missing signal alerts, cardinality monitoring, pipeline health dashboards, instrumentation testing.

### 7. Validate and Report


Generate debug report with analysis, fixes, prevention measures. Report completion.

## Error Handling

**Collector Unreachable**: Test connectivity and provide network troubleshooting.

**High Cardinality**: Identify problematic labels and provide reduction strategy.

**Trace Sampling Too Aggressive**: Analyze sampling decisions and adjust rates.

## Examples

**Example 1**: `/debug-observability Traces not appearing in backend for payment-service` - Output: Context propagation fix with instrumentation validation

**Example 2**: `/debug-observability High cardinality causing metric explosions` - Output: Label analysis with cardinality reduction strategy

**Example 3**: `/debug-observability Logs missing trace_id correlation` - Output: Log instrumentation fix with structured format

## References

