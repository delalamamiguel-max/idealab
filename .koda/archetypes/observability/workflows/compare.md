---
description: Compare observability platforms, instrumentation approaches, and telemetry strategies (Observability)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json ` and parse for OTEL_COLLECTOR_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/observability/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type (observability platforms, instrumentation methods, telemetry backends, sampling strategies), candidate options, evaluation criteria (cost, capabilities, complexity, vendor lock-in). Request clarification if incomplete.

### 4. Generate Comparison Framework

Based on comparison type, evaluate: Observability Platforms (Datadog vs Grafana/Prometheus vs Azure Monitor vs Dynatrace - features, cost, OpenTelemetry support, query capabilities), Instrumentation Approaches (auto-instrumentation vs manual spans vs hybrid - coverage, control, overhead, maintainability), Telemetry Backends (commercial SaaS vs self-hosted vs hybrid - cost, scalability, retention, integration), Sampling Strategies (head-based vs tail-based vs adaptive - cost, coverage, complexity, signal quality).

### 5. Create Comparison Matrix

Generate detailed comparison with quantitative metrics (cost per service, query performance, data retention, ingestion rate limits), qualitative assessments (ease of use, vendor support, community ecosystem, feature maturity), trade-off analysis (cost vs capabilities, complexity vs control), use case recommendations.

Include TCO analysis for different scales.

### 6. Add Recommendations

Recommend approach with comprehensive justification: requirements alignment, cost-benefit analysis, team capabilities, migration complexity, vendor strategy, long-term scalability.

Provide implementation roadmap and pilot plan.

### 7. Validate and Report


Generate comparison report with decision matrix, TCO analysis, recommendations. Report completion.

## Error Handling

**Insufficient Data**: Request workload characteristics and telemetry volume estimates.

**Unclear Requirements**: Facilitate requirements gathering on observability needs.

**Cost Uncertainty**: Provide detailed pricing models and projections.

## Examples

**Example 1**: `/compare-observability Datadog vs Grafana for microservices observability` - Output: Platform comparison with cost and feature analysis

**Example 2**: `/compare-observability Head-based vs tail-based sampling strategies` - Output: Sampling comparison with cost and signal quality trade-offs

**Example 3**: `/compare-observability Auto-instrumentation vs manual spans for FastAPI` - Output: Instrumentation approach comparison with overhead analysis

## References

