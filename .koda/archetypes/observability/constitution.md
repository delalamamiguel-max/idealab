# Observability (OpenTelemetry) Archetype Constitution

## Purpose
Provide a consistent, secure, low-overhead, end-to-end observability layer (traces, metrics, logs, profiles) for React (frontend) + FastAPI (backend) services using OpenTelemetry, enabling rapid root-cause analysis, SLO tracking, and actionable insights.

## I. Hard-Stop Rules (Non-Negotiable)
- ✘ No production service without trace propagation (W3C traceparent) across all hops.
- ✘ No logs without correlation (trace_id and span_id where request-scoped).
- ✘ No PII or secrets in logs, spans, events, metrics, exemplars.
- ✘ No custom metrics lacking: name, unit, description, aggregation intent.
- ✘ No unbounded high‑cardinality labels (e.g., user_id, raw URLs with IDs).
- ✘ No disabled error instrumentation (errors must emit spans + structured error fields).
- ✘ No frontend network requests without automatic trace context injection.
- ✘ No backend deployment without health (/healthz) & readiness (/readyz) probes instrumented.
- ✘ No divergent service.name/version naming (must follow agreed convention: domain-component-tier).
- ✘ No telemetry parser that swallows errors, drops required metadata, or assumes rigid schemas.

## II. Mandatory Patterns (Must Apply)

### Cross-Cutting
- ✔ OTLP export over TLS to central collector.
- ✔ Consistent resource attributes: service.name, service.version, deployment.environment, region, runtime.
- ✔ Standard span semantic conventions (HTTP, DB, messaging).
- ✔ RED + USE core metrics: request_rate, error_rate, duration/latency (p50, p90, p95, p99), utilization, saturation signals.
- ✔ Unified error envelope includes trace_id returned to clients.
- ✔ Log format: structured JSON; fields: timestamp, level, message, trace_id, span_id, env.
- ✔ Metrics units follow OpenTelemetry guidelines (seconds, bytes, dimensionless).
- ✔ Alert routing with severity tiers.

### Telemetry Ingestion
- ✔ Accept schema-less telemetry payloads (JSON, newline-delimited text) through resilient parsers.
- ✔ Normalize timestamps to UTC and retain source identifiers for every record.
- ✔ Provide dynamic field access with safe defaults; no assumption that optional fields exist.
- ✔ Emit structured error events when parsing fails, including offending payload context and exception details.
- ✔ Support batch and streaming ingestion paths with shared validation logic and retry policies.
- ✔ Trim unsafe whitespace, coerce numeric strings to numbers, and quarantine unparseable fields for replay.

### Backend (FastAPI)
- ✔ Auto-instrument: ASGI, HTTP client, SQLAlchemy.
- ✔ Explicit spans around business-critical operations (payment, scoring, enrichment).
- ✔ DB metrics: connection_pool_in_use, query_duration histogram.
- ✔ Query parameter redaction before span/log recording.
- ✔ Background tasks wrapped in root spans with linkage to triggering request (span links).

### Frontend (React)
- ✔ OTel Web SDK + Resource: app.name, app.version, deployment.environment.
- ✔ Navigation + interaction spans (route change, major user actions).
- ✔ Network request spans with injected trace context headers.
- ✔ Error boundary reports React component stack + trace_id.
- ✔ User identifiers hashed & only if classification allows.

### Governance & Quality
- ✔ SLOs: (e.g., p95 latency < 400ms, availability > 99.9%) codified in repo (slo.yaml).
- ✔ CI check: schema lint (metric name format: namespace.metric_name; lowercase, snake_case).
- ✔ Dashboards: one golden dashboard per service (Latency, Errors, Saturation, Top N slow spans).
- ✔ Runbooks linked from alerts (annotation: runbook_url).
- ✔ Weekly drift review: unused metrics & spans pruned.

## III. Preferred Patterns (Recommended)
- ➜ Adaptive sampling scaling with traffic bands.
- ➜ Exemplars linking high-latency metrics to representative spans.
- ➜ eBPF-based auto profiling (CPU, wall time) correlated with traces.
- ➜ Business KPIs (e.g., conversion_rate) tagged with trace correlation window.
- ➜ Scenario replay traces for performance regression analysis.
- ➜ Synthetic probes emitting synthetic_user trace set.
- ➜ Cost attribution: estimate telemetry ingestion cost per service & optimize cardinality.
- ➜ Implement configurable field mappings, external metadata enrichment, and adaptive sampling for telemetry parsers.
- ➜ Maintain parser health dashboards (throughput, error rate, latency) alongside core service views.

## IV. Minimal Service Naming Convention
Pattern: domain-component-tier[-environment]  
Example: commerce-checkout-api, analytics-insights-web, defender-dev-api

Including an optional environment suffix (e.g., `-dev`, `-staging`) is acceptable for non-production deployments to aid clarity and separation, but production services should omit the environment unless required by platform constraints.

## V. Required Outputs per Release
- Updated service.version propagated to resource attributes.
- CHANGELOG entry listing observability-impacting changes.
- SLO error budget burn report (rolling 7d).

## VI. Alert Baseline (Example)
- High latency: p95_latency_seconds > 0.4 for 5m
- Error spike: error_rate > 2% for 5m
- Saturation: cpu_utilization > 80% for 10m
- Missing signals: no traces ingested 3m (critical)

## VII. Anti-Patterns (Reject)
- Raw stack traces in customer-visible messages.
- Embedding dynamic IDs in metric names.
- Logging entire payloads (truncate + hash).
- Silent span suppression to “reduce noise” without review.

## VIII. Success Indicators
- MTTR reduction quarter over quarter.
- <5% of alerts classified as noise.
- 95% of production requests carry trace context end-to-end.
- 100% SLO definitions version-controlled & linked to dashboards.

## IX. Appendix: Schema-less Telemetry Parser Example

```python
import json
from datetime import datetime, timezone
from typing import Any, Dict


def normalize_timestamp(raw_ts: str | None) -> str:
	try:
		return datetime.fromisoformat(raw_ts).astimezone(timezone.utc).isoformat()
	except Exception:
		return datetime.now(timezone.utc).isoformat()


def parse_telemetry(raw_payload: str) -> Dict[str, Any]:
	try:
		parsed = json.loads(raw_payload)
	except json.JSONDecodeError as exc:
		raise ValueError("telemetry_parse_error") from exc

	return {
		"timestamp": normalize_timestamp(parsed.get("timestamp")),
		"source_id": parsed.get("source_id", "unknown"),
		"event_type": parsed.get("event_type", "unspecified"),
		"payload": parsed.get("payload", {}),
		"raw": parsed,
	}
```

Version: 0.2.0  
Last Updated: 2025-10-27
