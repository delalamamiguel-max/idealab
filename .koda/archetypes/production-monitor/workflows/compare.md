---
description: Compare monitoring stacks, tool options, or deployment approaches and produce a scored recommendation (Production Monitor)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Candidates**: Two or more monitoring approaches, tools, or configurations to compare (e.g. `"Phoenix vs LangSmith"`, `"config-v1.yaml vs config-v2.yaml"`)
- **Comparison axis**: One or more of `coverage`, `cost`, `sox-compliance`, `latency-overhead`, `drift-detection`
- **Agent context**: Agent name and whether SOX-scoped; affects weighting of compliance criteria

### 2. Define Comparison Matrix
- Construct a structured matrix of evaluation criteria weighted by the agent's requirements:
  ```python
  CRITERIA = {
      "trace_coverage":       {"weight": 0.20, "description": "Spans, evals, LLM quality metrics"},
      "sox_compliance":       {"weight": 0.25, "description": "Immutable logs, 7-yr retention, evidence export"},
      "latency_overhead_ms":  {"weight": 0.15, "description": "Added P99 latency from instrumentation"},
      "drift_detection":      {"weight": 0.15, "description": "Embedding drift, response drift support"},
      "alert_routing":        {"weight": 0.15, "description": "PagerDuty, Slack, or email routing with deduplication"},
      "cost_per_million_req": {"weight": 0.10, "description": "USD cost at one million requests per month"},
  }

  for crit, meta in CRITERIA.items():
      print(f"  {crit} (w={meta['weight']}): {meta['description']}")
  ```
- For config-vs-config comparisons, load both YAML files and diff the SLO thresholds, alert rules, and retention settings side-by-side.

### 3. Collect Baseline Metrics for Each Candidate
- For tool comparisons (e.g. Phoenix vs. LangSmith), query the Phoenix API for observed overhead
  and pull LangSmith cost data from its billing export:
  ```python
  import httpx, os

  # Phoenix: measure instrumentation overhead via trace timing metadata
  resp = httpx.get(
      build_phoenix_metrics_url(os.environ["PHOENIX_ENDPOINT"], "<agent_name>"),
      params={"metric": "instrumentation_overhead_ms", "window": "24h"}
  )
  phoenix_overhead = resp.json().get("value", "unknown")
  print(f"Phoenix instrumentation overhead P99: {phoenix_overhead} ms")
  ```
- For config comparisons, compute coverage score by counting defined SLO keys against `REQUIRED_SLOS` set.

### 4. Score Each Candidate
- Apply weights and produce a normalised score between 0 and 1 for each candidate:
  ```python
  def score_candidate(candidate_data: dict, criteria: dict) -> float:
      total = 0.0
      for crit, meta in criteria.items():
          raw     = candidate_data.get(crit, 0)          # 0–1 normalised value
          total  += raw * meta["weight"]
      return round(total, 3)

  candidates = {
      "arize-phoenix": {"trace_coverage": 0.95, "sox_compliance": 0.90,
                        "latency_overhead_ms": 0.85, "drift_detection": 0.90,
                        "alert_routing": 0.80, "cost_per_million_req": 0.75},
      "langsmith":     {"trace_coverage": 0.80, "sox_compliance": 0.55,
                        "latency_overhead_ms": 0.90, "drift_detection": 0.60,
                        "alert_routing": 0.70, "cost_per_million_req": 0.65},
  }

  for name, data in candidates.items():
      print(f"{name}: {score_candidate(data, CRITERIA)}")
  ```

### 5. Produce Recommendation and Migration Path
- Identify the highest-scoring candidate and surface key differentiators.
- If the winner differs from the current stack, outline a migration path with zero-downtime rollout steps:
  - Week 1: Run both stacks in parallel (shadow mode); compare trace completeness.
  - Week 2: Shift 10% of traffic to new stack; monitor for cardinality spikes.
  - Week 3–4: Full cutover; decommission old stack after 7-day clean run.
- If both candidates are within 5% of each other, recommend deferring the switch (switching cost exceeds benefit).

### 6. Write Comparison Report
- Emit `monitoring/comparison-report.md` with the matrix, scores, rationale, and migration path.

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide at least two candidates and one comparison axis. |
| Incompatible monitoring stacks (different data models) | Map each stack to the canonical criterion set defined in step 2. Use 0.0 for criteria the stack does not support — do not skip the criterion. |
| Insufficient baseline period (< 24 hours of data) | Warn that scores may be unreliable. Proceed with available data; flag all scores derived from < 24h window with an asterisk. |
| Metric cardinality mismatch between candidates | Normalise cardinality to per-million-requests before scoring. A stack with 10× higher cardinality is not 10× better — cap normalised score at 1.0. |
| Only one candidate provided | Re-prompt: comparison requires at least two. Offer to compare against the constitution's recommended baseline (Arize Phoenix defaults). |
| `production-monitor-constitution.md` not found | Stop. Constitution defines mandatory patterns; comparison must validate each candidate's compliance with it. |

## Examples

**Example 1**: `/compare-production-monitor "Phoenix vs LangSmith" sox-compliance`
Matrix shows Phoenix scores 0.90 on SOX compliance (immutable logs, 7-year retention, evidence export) vs. LangSmith at 0.55 (no built-in retention controls). Recommendation: Phoenix for any SOX-scoped agent.

**Example 2**: `/compare-production-monitor "config-v1.yaml vs config-v2.yaml" coverage,thresholds`
Config v2 adds `hallucination_rate_max` and `faithfulness_min` SLOs absent in v1; v2 scores 0.91 vs v1's 0.74 on coverage. Threshold comparison shows v2 tightened `latency_p95_ms` from 3000 to 2000 — cross-validated against 7-day baseline confirming the tighter value is achievable.
