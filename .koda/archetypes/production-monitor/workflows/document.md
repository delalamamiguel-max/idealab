---
description: Generate monitoring documentation, alert runbooks, and SOX evidence guides (Production Monitor)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Config path**: Path to `monitoring/config.yaml` (source of truth for all metrics and SLOs)
- **Output scope**: One or more of `metrics`, `runbooks`, `sox-guide`, `api-reference` — or `full` to generate everything
- **Agent name**: Used to namespace generated documents and populate runbook titles

### 2. Document Defined Metrics and SLOs
- Read the monitoring config and emit a human-readable metrics reference:
  ```python
  import yaml, textwrap

  with open(config_path) as f:
      cfg = yaml.safe_load(f)

  lines = ["# Metrics Reference\n"]
  for slo_name, slo_value in cfg.get("slos", {}).items():
      lines.append(f"## `{slo_name}`")
      lines.append(f"- **Threshold**: `{slo_value}`")
      lines.append(f"- **Source**: Phoenix span attribute `{slo_name}`")
      lines.append(f"- **Breach action**: See alert rule `{slo_name}_alert` in runbook\n")

  metrics_reference_path = docs_dir / "metrics-reference.md"
  with open(metrics_reference_path, "w") as f:
      f.write("\n".join(lines))
  print(f"Written: {metrics_reference_path}")
  ```
- Flag any SLO that lacks a human-readable description and emit a `TODO` placeholder for the team to fill.

### 3. Generate Alert Runbooks
- For each defined alert, produce a step-by-step incident response runbook:
  ```python
  RUNBOOK_TEMPLATE = """\
  ## Alert: {name}

  **Condition**: `{condition}`
  **Severity**: {severity}
  **Channel**: {channel}

  ### Response Steps
  1. Acknowledge the alert in {ack_system} (within {ack_sla} minutes for `{severity}` severity).
  2. Open the Phoenix dashboard for project `{project}` and filter spans by the last 30 minutes.
  3. Identify the span(s) where `{metric_key}` exceeds `{threshold}`.
  4. Check for correlated errors: high latency often accompanies upstream API timeouts.
  5. Escalate to on-call engineer if not resolved within {escalate_minutes} minutes.
  6. Post incident summary in `#incidents` Slack channel after resolution.

  ### Rollback
  - If caused by a recent deployment: `git revert <commit>` and redeploy.
  - If caused by upstream degradation: enable circuit breaker and notify vendor.
  """

  for alert in cfg.get("alerts", []):
      runbook_path = runbooks_dir / f"{alert['name']}.md"
      content = RUNBOOK_TEMPLATE.format(
          name=alert["name"],
          condition=alert.get("condition", "—"),
          severity=alert.get("severity", "warning"),
          channel=alert.get("channel", "slack"),
          ack_system="PagerDuty" if alert.get("severity") == "critical" else "Slack",
          ack_sla=5 if alert.get("severity") == "critical" else 30,
          project=cfg.get("agent_name", "<agent_name>"),
          metric_key=alert["name"].replace("_alert", ""),
          threshold=alert.get("threshold", "—"),
          escalate_minutes=15 if alert.get("severity") == "critical" else 60,
      )
      with open(runbook_path, "w") as f:
          f.write(content)
      print(f"Written: {runbook_path}")
  ```

### 4. Generate SOX Evidence Collection Guide
- Produce `docs/sox-evidence-guide.md` describing how auditors export and verify immutable traces:
  ```python
  sox_guide = f"""
  # SOX Evidence Collection Guide — {cfg.get('agent_name', 'Agent')}

  ## Evidence Sources
  | Source | Location | Retention |
  |--------|----------|-----------|
  | Phoenix trace export | `Phoenix export API for the configured agent` | 7 years |
  | Audit JSONL log | `${{AUDIT_LOG_PATH}}` | 7 years |
  | SLO compliance report | `monitoring/test-report.json` | Per audit cycle |

  ## Export Commands
  ```bash
  # Export all traces for a date range
    Run the Phoenix export helper for the configured agent and write the output to the quarterly evidence archive.
    Then compute and store a SHA-256 checksum beside that archive.
  ```

  ## Required Span Fields (SOX Mandatory)
  - `agent_name` — identifies the processing system
  - `user_id` — links to the data subject (GDPR/SOX cross-reference)
  - `timestamp` — UTC ISO-8601
  - `input_hash` — SHA-256 of input payload
  - `output_hash` — SHA-256 of output payload
  """

  sox_guide_path = docs_dir / "sox-evidence-guide.md"
  with open(sox_guide_path, "w") as f:
      f.write(sox_guide)
  print(f"Written: {sox_guide_path}")
  ```

### 5. Build API Reference for Monitoring Hooks
- Document the `ProductionMonitor` class public interface sourced from `templates/monitoring_setup_example.py`:
  - `__init__(config: MonitoringConfig)` — initialises Phoenix tracing and optional SOX dashboard
  - `record_request(latency_ms, success)` — records per-request metrics and triggers SLO checks
  - `get_health_status()` → `{"status": "healthy|degraded|unknown", ...}` — returns current aggregate health

### 6. Validate Completeness and Write Index
- Confirm every alert has a corresponding runbook; surface any undocumented channel or missing SLO description:
  ```python
  import os

  defined_alerts = {a["name"] for a in cfg.get("alerts", [])}
  runbook_files  = {f.replace(".md", "") for f in os.listdir(runbooks_dir) if f.endswith(".md")}
  undocumented   = defined_alerts - runbook_files

  if undocumented:
      print(f"WARNING: Alerts with no runbook: {undocumented}")
  else:
      print("PASS: All alerts have runbooks")
  ```
- Write `docs/README.md` as an index linking metrics reference, all runbooks, and the SOX evidence guide.

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide config path and output scope (`metrics`, `runbooks`, `sox-guide`, `api-reference`, or `full`). |
| Missing SLO definitions in `monitoring/config.yaml` | Emit `TODO` placeholders for undefined SLOs in the metrics reference. Print a warning listing each missing SLO name. Do not abort — partial documentation is better than none. |
| Undocumented alert channels (alert references env var that isn't documented) | Surface the undocumented channel name in the generated runbook as `⚠️ VERIFY: <ENV_VAR> must be set`. Do not hard-code values. |
| Outdated runbook (runbook exists but config has changed) | Detect by comparing `last_modified` of alert config vs. runbook file. Regenerate any runbook older than the config. |
| Runbooks directory does not exist | Create it with a platform-neutral `Path` join before writing runbooks. |
| `production-monitor-constitution.md` not found | Stop. Constitution is used to validate that all mandatory patterns are documented; cannot generate complete docs without it. |

## Examples

**Example 1**: `/document-production-monitor monitoring/config.yaml full`
Generates `docs/metrics-reference.md` (6 SLOs documented), `docs/runbooks/` (4 runbook files, one per alert), `docs/sox-evidence-guide.md`, and `docs/README.md` index — all in under 10 seconds.

**Example 2**: `/document-production-monitor monitoring/config.yaml runbooks`
Discovers 2 alerts with no runbook (`hallucination_rate_alert`, `faithfulness_alert`) added in last sprint; generates both with templated response steps, escalation times, and rollback instructions.
