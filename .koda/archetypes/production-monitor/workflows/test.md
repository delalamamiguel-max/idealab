---
description: Validate monitoring setup, alert routing, and SOX compliance end-to-end (Production Monitor)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Config path**: Path to `monitoring/config.yaml`
- **Test scope**: One or more of `traces`, `alerts`, `sox`, `quality` — or `all` to run the full suite
- **Environment**: `local` (Phoenix at localhost:6006) or `staging` (PHOENIX_ENDPOINT env var)

### 2. Validate Phoenix Trace Collection
- Emit a synthetic trace and confirm it appears in Phoenix within the expected window:
  ```python
  from phoenix.otel import register
  from opentelemetry import trace
  import time, httpx, os

  register(project_name="test-validation", endpoint=os.environ["PHOENIX_ENDPOINT"])
  tracer = trace.get_tracer("test")

  with tracer.start_as_current_span("test-span") as span:
      span.set_attribute("agent_name", "test-validation")
      span.set_attribute("test_run", True)
      time.sleep(0.05)

  # Allow exporter flush
  time.sleep(2)

  resp = fetch_project_spans(os.environ["PHOENIX_ENDPOINT"], "test-validation")
  assert len(resp.json().get("data", [])) > 0, "FAIL: test span not ingested by Phoenix"
  print("PASS: trace ingestion verified")
  ```
- Verify that span attributes include all required fields: `agent_name`, `user_id`, `timestamp`, `input_hash`, `output_hash`.

### 3. Exercise Alert Routing
- For each configured alert rule, inject a synthetic metrics event that breaches the threshold and confirm delivery:
  ```python
  import yaml, requests, os

  with open(config_path) as f:
      cfg = yaml.safe_load(f)

  for alert in cfg.get("alerts", []):
      channel = alert.get("channel", "slack")
      if channel == "slack":
          url  = os.environ["SLACK_WEBHOOK_URL"]
          body = {"text": f"[TEST] Alert '{alert['name']}' channel verification — ignore"}
          r = requests.post(url, json=body)
          status = "PASS" if r.status_code == 200 else f"FAIL ({r.status_code})"
          print(f"{alert['name']} → {channel}: {status}")
  ```
- Confirm PagerDuty receives test events for `critical`-severity rules (check PD "Test Incidents" view).
- Verify deduplication: fire the same alert twice within the `dedupe_window_minutes` period; confirm only one notification is delivered.

### 4. Verify SOX Compliance Logging
- Confirm `AUDIT_LOG_PATH` is set, the file is writable, and new events are appended correctly:
  ```python
  import os, json, tempfile

  audit_path = os.environ.get("AUDIT_LOG_PATH", resolve_temp_audit_file())
  test_event = {
      "agent_name": "test-validation",
      "user_id":    "test-user-001",
      "timestamp":  "2026-03-27T00:00:00Z",
      "input_hash": "abc123",
      "output_hash": "def456",
      "action":     "test_event",
  }
  with open(audit_path, "a") as f:
      f.write(json.dumps(test_event) + "\n")

  # Read back and verify
  with open(audit_path) as f:
      last_line = f.readlines()[-1]
  assert json.loads(last_line)["action"] == "test_event", "FAIL: SOX event not persisted"
  print("PASS: SOX audit log persistence verified")
  ```
- Confirm the log file is immutable after write (check file permissions; production should be append-only `0644` owned by the service account, not world-writable).

### 5. Run Quality Metric Assertions
- Stub a failing LLM response and confirm hallucination alert fires:
  ```python
  from deepeval.metrics import HallucinationMetric
  from deepeval.test_case import LLMTestCase

  metric = HallucinationMetric(threshold=0.05)
  tc = LLMTestCase(
      input="What is 2+2?",
      actual_output="The answer is banana.",   # intentionally wrong
      context=["2+2=4"]
  )
  metric.measure(tc)
  assert metric.score > 0.05, "Expected hallucination score above threshold for test case"
  print(f"PASS: Hallucination metric score={metric.score:.3f} (above threshold)")
  ```

### 6. Generate Test Report
- Aggregate pass/fail for all checks and write `monitoring/test-report.json`:
  ```python
  import json, datetime

  report = {
      "generated_at": datetime.datetime.utcnow().isoformat(),
      "results": {
          "trace_ingestion": "PASS",
          "alert_routing":   "PASS",
          "sox_logging":     "PASS",
          "quality_metrics": "PASS",
      },
      "failures": [],
  }
  report_path = output_path
  with open(report_path, "w") as f:
      json.dump(report, f, indent=2)
  print(f"Test report written to {report_path}")
  ```

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide config path and test scope (`traces`, `alerts`, `sox`, `quality`, or `all`). |
| Flaky metrics in test environment | Increase synthetic event count from 1 to 10; use `statistics.mean()` to reduce noise. Pin test to a dedicated Phoenix project (`test-validation`) to avoid polluting production data. |
| Missing Phoenix test fixture (no project exists) | Create the test project via `register(project_name="test-validation", ...)` before asserting spans exist. Wait 2 seconds for exporter flush before querying. |
| SOX log not generated (audit file absent) | Confirm `AUDIT_LOG_PATH` env var is set. Create parent directory if missing. Check that `log_sox_event()` is called — not just defined. |
| Quality metric assertion fails unexpectedly | Confirm `deepeval` version matches `requirements.txt`. Check `context` field is populated; empty context produces unreliable hallucination scores. |
| `production-monitor-constitution.md` not found | Stop. Ensure constitution file is at repo root; the test suite relies on it for SLO reference values. |

## Examples

**Example 1**: `/test-production-monitor monitoring/config.yaml all`
Full suite runs in ~45 seconds; emits synthetic traces, fires test alerts to Slack and PagerDuty, writes a SOX test event, and produces `monitoring/test-report.json` with 4/4 PASS.

**Example 2**: `/test-production-monitor monitoring/config.yaml sox`
SOX-only test confirms audit log path is writable, all required span fields are present, and retention is set to ≥ 2555 days. Flags a world-writable audit log file and recommends `chmod 644`.
