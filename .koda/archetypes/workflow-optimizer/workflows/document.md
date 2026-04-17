---
description: Generate comprehensive optimization documentation for a Workflow Optimizer workflow
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input and Discover Documentation Scope
- **Workflow path**: Path to the workflow to document (e.g., `graph/workflow.py`)
- **Documentation mode**: `full` | `summary` | `changelog`
  - `full`: complete performance guide + optimization history + current metrics
  - `summary`: one-page snapshot of current performance vs. baseline
  - `changelog`: structured log of all optimizations applied with before/after metrics
- Check for existing `OPTIMIZATION_LOG.md` — if absent, flag it as a documentation gap to be created
- Check `tests/fixtures/baseline_metrics.json` — if absent, note that no certified baseline exists

### 2. Extract Current Metrics and Optimization History
- Pull the last 50 LangSmith traces for the target workflow and compute current P50/P95 latency and average cost:

```python
from langsmith import Client
import statistics, json

client = Client()
runs = list(client.list_runs(project_name="workflow-optimizer", run_type="chain", limit=50))
latencies = [(r.end_time - r.start_time).total_seconds() * 1000 for r in runs if r.end_time]
token_costs = [r.total_cost for r in runs if r.total_cost is not None]
metrics = {
    "p50_ms": round(statistics.median(latencies), 1),
    "p95_ms": round(sorted(latencies)[int(len(latencies) * 0.95)], 1),
    "avg_cost_usd": round(sum(token_costs) / len(token_costs), 5) if token_costs else None,
    "sample_count": len(latencies)
}
print(json.dumps(metrics, indent=2))
```

- Read `OPTIMIZATION_LOG.md` to enumerate all applied optimizations and their recorded before/after deltas

### 3. Generate Performance Baseline Summary
- Format the `## Baseline Metrics` section with values from `tests/fixtures/baseline_metrics.json`
- Format the `## Current Metrics` section from Step 2 output
- Compute cumulative improvement since baseline: latency delta %, cost delta %, quality delta
- If no baseline fixture exists: write a `⚠ Warning: No certified baseline found` block and recommend running `test-workflow-optimizer` first

### 4. Document Optimization History
- For each entry in `OPTIMIZATION_LOG.md`, generate a structured changelog entry:
  - Optimization type (caching / parallelism / model-swap / prompt-compression)
  - Date applied, PR reference
  - Before/after P95 latency and cost
  - Quality gate result (pass/fail)
  - Rollback notes if applicable
- Highlight the single largest latency win and the single largest cost win achieved to date

### 5. Write Documentation Artifact
- Write the completed documentation to `docs/optimization-guide.md` (create file if absent)
- If mode is `changelog`, also append to `OPTIMIZATION_LOG.md` with today's snapshot
- Ensure all metric links reference actual LangSmith run IDs or trace URLs — no dead/placeholder links

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide workflow path and documentation mode (full/summary/changelog). |
| `OPTIMIZATION_LOG.md` not found | Create the file with a blank template. Warn that no optimization history has been recorded yet. |
| Baseline fixture missing (`tests/fixtures/baseline_metrics.json`) | Document with a warning block; recommend running `test-workflow-optimizer` to establish baseline before publishing docs. |
| Broken metric links (LangSmith run IDs not resolvable) | Omit the specific run links; use aggregate statistics only. Log the gap as "run data unavailable for period X". |
| Undocumented optimization history detected (code changed but no log entry) | Flag the gap: "Optimization applied without log entry detected between commit A and B." Add placeholder for human review. |
| Constitution file not found | Stop. Ensure `workflow-optimizer-constitution.md` is present at repo root. Documentation must reference the governing constraints. |

## Examples

**Example 1**: `/document-workflow-optimizer graph/rag_chain.py full`
- Generates `docs/optimization-guide.md` with baseline vs. current metrics, 3 changelog entries, and quality gate history

**Example 2**: `/document-workflow-optimizer agents/multi_step.py changelog`
- Appends current P95 snapshot (11.2s) and cost ($0.0042/req) to `OPTIMIZATION_LOG.md`; flags one optimization applied without a log entry
