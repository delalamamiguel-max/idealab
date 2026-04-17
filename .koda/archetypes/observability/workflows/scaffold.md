---
description: Generate end-to-end observability layer with OpenTelemetry for React and FastAPI services (Observability)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json ` and parse for OTEL_COLLECTOR_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/observability/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: application stack (React frontend, FastAPI backend), deployment environment, telemetry requirements (traces, metrics, logs), SLO definitions, alert requirements. Request clarification if incomplete.

### 4. Generate Observability Layer

Create comprehensive instrumentation: Backend Instrumentation (FastAPI auto-instrumentation setup, explicit span creation for critical operations, structured logging with trace correlation, database and HTTP client instrumentation, health and readiness probe instrumentation, RED metrics emission (request rate, error rate, duration), resource attributes (service.name, version, environment)), Frontend Instrumentation (OTel Web SDK configuration, navigation and interaction spans, network request tracing with context propagation, error boundary integration, user action tracking, performance metrics), Telemetry Pipeline (OTLP export configuration over TLS, trace propagation with W3C traceparent, log correlation with trace_id and span_id, metric aggregation and export, sampling configuration), Observability Infrastructure (collector configuration, backend integration (Datadog/Grafana/Azure Monitor), dashboard templates, alert rule definitions, SLO configurations with error budgets).

### 5. Generate Monitoring Configuration

Implement observability: SLO Definitions (availability, latency percentiles, error rates, error budget calculations), Dashboards (golden signals dashboard, service health overview, trace analysis views, RED+USE metrics), Alert Rules (high latency alerts, error spike detection, saturation warnings, missing telemetry alerts, SLO burn rate alerts), Telemetry Parser (schema-less payload handling, dynamic field access with safe defaults, error event emission, batch and streaming support).

### 6. Add Recommendations

Include best practices: adaptive sampling strategies, exemplar linking, PII redaction, cost optimization, incident correlation, continuous profiling integration.

### 7. Validate and Report


Generate complete observability layer with instrumentation code, dashboards, and alerts. Report completion.

## Error Handling

**Collector Unavailable**: Provide setup instructions or fallback configuration.

**Trace Propagation Broken**: Validate W3C headers and context injection.

**High Cardinality**: Identify and fix unbounded labels.

## Examples

**Example 1**: `/scaffold-observability Instrument order-service with OpenTelemetry` - Output: Complete instrumentation with traces, metrics, and logs

**Example 2**: `/scaffold-observability Create observability for React+FastAPI app with SLOs` - Output: End-to-end telemetry with SLO monitoring

**Example 3**: `/scaffold-observability Generate monitoring with RED metrics and dashboards` - Output: Observable service with golden signals

## References

