---
description: Restructure and improve monitoring coverage, SLO thresholds, and alert routing (Production Monitor)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Config path**: Path to `monitoring/config.yaml` or equivalent monitoring definition file
- **Refactor goal**: One of `coverage` (add missing metrics), `thresholds` (tune SLO values), `routing` (improve alert delivery), or `retention` (fix log retention policy)
- **SOX scope**: Whether the agent is SOX-scoped — affects retention and audit trail requirements

### 2. Audit Current Monitoring Coverage
- Load existing config and map covered vs. missing SLO dimensions:
  ```python
  import yaml

  REQUIRED_SLOS = {"latency_p95_ms", "error_rate", "eval_pass_rate",
                   "hallucination_rate_max", "faithfulness_min", "answer_relevancy_min"}

  with open(config_path) as f:
      cfg = yaml.safe_load(f)

  defined = set(cfg.get("slos", {}).keys())
  missing = REQUIRED_SLOS - defined
  print(f"Missing SLOs: {missing}")
  ```
- Identify alerts with no corresponding SLO (orphaned rules) and SLOs with no alert rule (silent violations).
- Flag alert channels that route all severities to the same destination — `critical` should page on-call (PagerDuty), `warning` should go to Slack.

### 3. Tune SLO Thresholds Against Baseline Data
- Pull 7-day P95 latency and error rate from Phoenix to set realistic baselines before tightening thresholds:
  ```python
  import httpx, os, statistics

  endpoint = os.environ["PHOENIX_ENDPOINT"]
  project  = "<agent_name>"
  resp = fetch_project_metrics(endpoint, project,
                   params={"metric": "latency_ms", "percentile": 95, "window": "7d"})
  p95_baseline = resp.json()["value"]
  # Add 20% headroom above baseline for a non-noisy threshold
  recommended_threshold = round(p95_baseline * 1.20)
  print(f"Recommended latency_p95_ms threshold: {recommended_threshold}")
  ```
- Apply similar logic for quality metrics: set `hallucination_rate_max` 1.5× observed mean, not an arbitrary 5%.

### 4. Restructure Alert Routing by Severity
- Refactor routing so severity maps deterministically to channel:
  ```yaml
  alert_routing:
    critical:
      channels: [pagerduty]
      env_var: PAGERDUTY_ROUTING_KEY
      escalation_minutes: 15
    warning:
      channels: [slack]
      env_var: SLACK_WEBHOOK_URL
    info:
      channels: [email]
      env_var: ALERT_EMAIL
  ```
- Remove any hard-coded webhook URLs from config; all credentials must come from env vars to pass secret scanning.
- Add a `dedupe_window_minutes` field to prevent alert storms when a threshold is breached repeatedly.

### 5. Fix Retention Policy and SOX Alignment
- Verify retention settings satisfy the 7-year SOX requirement for SOX-scoped agents:
  ```python
  REQUIRED_RETENTION_DAYS = 2555  # 7 years

  current = cfg.get("retention_days", 0)
  if cfg.get("sox_scope") and current < REQUIRED_RETENTION_DAYS:
      cfg["retention_days"] = REQUIRED_RETENTION_DAYS
      print(f"Updated retention_days from {current} to {REQUIRED_RETENTION_DAYS}")
  ```
- Write the updated config back and commit; include a comment block documenting the rational for each threshold change.

### 6. Validate Refactored Config
- Run a dry-run diff to confirm only intended fields changed:
  ```bash
  git diff monitoring/config.yaml
  ```
- Inject synthetic metrics at the new thresholds and verify routing lands on the correct channel.
- Re-run coverage audit from step 2 to confirm zero missing SLOs and zero orphaned alert rules.

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide config path and refactor goal (`coverage`, `thresholds`, `routing`, or `retention`). |
| SLO threshold too tight causing false alerts | Pull 7-day baseline from Phoenix; set threshold at 1.2× P95 baseline. Never set below observed p50. |
| Metric naming collision (same name, different units) | Rename one metric using dot-notation convention: `latency.p95_ms` vs `latency.p50_ms`. Update all alert rules referencing the old name. |
| Retention policy conflict (SOX vs. storage cost) | SOX requirement wins — set `retention_days: 2555`. Implement tiered storage: hot for 90 days, cold archive for remainder. |
| Hard-coded credentials found in config | Replace with env var references immediately. Rotate the exposed credential. Add pre-commit hook to block future occurrences. |
| `production-monitor-constitution.md` not found | Stop. Ensure constitution file is at repo root before any config rewrite. |

## Examples

**Example 1**: `/refactor-production-monitor monitoring/config.yaml thresholds`
Agent pulls 7-day Phoenix baseline (P95 = 1,240 ms), recommends threshold of 1,488 ms, updates config, and confirms the previously noisy latency alert drops from 47 fires/day to 3.

**Example 2**: `/refactor-production-monitor monitoring/config.yaml routing`
Agent finds all severities routing to the same Slack channel; restructures routing block to send `critical` to PagerDuty and `warning` to Slack; verifies with synthetic alert injection.
