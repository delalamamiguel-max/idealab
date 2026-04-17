---
description: Diagnose and fix monitoring gaps, missing traces, and misfiring alerts (Production Monitor)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Agent name / config path**: Target agent or path to `monitoring/config.yaml`
- **Issue description**: Free-text symptom (e.g. "Alerts not firing", "Traces missing in Phoenix")
- **SOX scope**: Whether the agent is SOX-scoped — affects which compliance checks run

### 2. Verify Phoenix Connectivity and Trace Ingestion
- Confirm `PHOENIX_ENDPOINT` is set and the server is reachable:
  ```bash
  Use an HTTP client to query the Phoenix health endpoint and confirm it returns `ok`.
  ```
- Query the Phoenix API to check whether recent traces exist for the agent project:
  ```python
  import httpx, os, datetime

  endpoint = os.environ["PHOENIX_ENDPOINT"]
  project  = "<agent_name>"
  since    = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat()

  resp = fetch_project_spans(endpoint, project, start_time=since)
  spans = resp.json().get("data", [])
  print(f"Spans in last hour: {len(spans)}")
  if not spans:
      print("WARNING: No traces received — check LangChainInstrumentor is active")
  ```
- Confirm `LangChainInstrumentor().instrument()` is called before the first LangChain invocation; missing this call is the #1 cause of empty Phoenix dashboards.

### 3. Diagnose Alert Misfires
- Pull the active alert rules from the monitoring config and cross-check against current metric values:
  ```python
  import yaml, json

  with open(config_path) as f:
      cfg = yaml.safe_load(f)

  for alert in cfg.get("alerts", []):
      print(f"Rule: {alert['name']} | Condition: {alert['condition']} | Channel: {alert['channel']}")
  ```
- For each silent alert, verify:
  - The metric name in the condition matches the span attribute key emitted by the instrumentor (exact string match — Phoenix is case-sensitive).
  - The alert channel webhook (`SLACK_WEBHOOK_URL`, `PAGERDUTY_ROUTING_KEY`) is populated and not expired.
  - The eval pipeline runs frequently enough (cron/streaming) to generate the metric Phoenix evaluates against.
- Manually inject a threshold-breaching event to confirm the alert channel fires:
  ```python
  import requests, os

  payload = {"text": "[DEBUG TEST] Latency alert channel verification — ignore"}
  r = requests.post(os.environ["SLACK_WEBHOOK_URL"], json=payload)
  print(r.status_code)  # expect 200
  ```

### 4. Inspect SOX Trace Completeness (if SOX scope)
- Verify required fields are present on every span; missing fields break SOX audit exports:
  ```python
  required = {"agent_name", "user_id", "timestamp", "input_hash", "output_hash"}
  for span in spans:
      attrs = set(span.get("attributes", {}).keys())
      missing = required - attrs
      if missing:
          print(f"Span {span['span_id']} MISSING: {missing}")
  ```
- Confirm `AUDIT_LOG_PATH` is writable and that `log_sox_event()` is invoked on every request completion.

### 5. Apply Fixes and Validate
- Fix identified issues: update metric names, re-instrument with `LangChainInstrumentor`, patch env vars, or flush the OTLP exporter:
  ```python
  from opentelemetry.sdk.trace.export import SimpleSpanProcessor
  from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

  exporter = OTLPSpanExporter(endpoint=build_phoenix_traces_url(os.environ["PHOENIX_ENDPOINT"]))
  tracer_provider.add_span_processor(SimpleSpanProcessor(exporter))
  ```
- Re-run step 2 connectivity check; confirm spans appear in Phoenix within 30 seconds.
- Trigger a synthetic trace and verify the corrected alert fires end-to-end.

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide agent name/config path and symptom description. |
| Phoenix endpoint unreachable | Verify `PHOENIX_ENDPOINT` env var. Confirm Phoenix server is running (`docker ps` or process check). Fall back to local OTLP collector at `http://localhost:4318`. |
| Missing traces in Phoenix dashboard | Confirm `LangChainInstrumentor().instrument()` runs before first LangChain call. Check `OTEL_EXPORTER_OTLP_ENDPOINT` is not overriding `PHOENIX_ENDPOINT`. |
| Alert not firing despite threshold breach | Verify metric name exact-matches span attribute key. Confirm webhook env var is set. Test channel directly with synthetic POST. |
| SOX span missing required fields | Add missing attributes in `log_sox_event()`. Re-deploy agent and re-run trace completeness check. |
| `production-monitor-constitution.md` not found | Stop. Ensure file is present at repo root before proceeding with any config edits. |

## Examples

**Example 1**: `/debug-production-monitor support-agent "No traces in Phoenix for last 2 hours"`
Agent determines `LangChainInstrumentor().instrument()` was called after the first chain invocation; moves call to module load time; traces appear in Phoenix within one minute.

**Example 2**: `/debug-production-monitor fraud-detector "PagerDuty alert silent when latency > 3000ms"`
Agent inspects alert config, finds metric key is `latency_ms_p95` but Phoenix span attribute is `latency.p95_ms`; renames key in config; injects synthetic slow trace; PagerDuty alert fires correctly.
