---
description: Benchmark and validate workflow performance against baseline fixtures (Workflow Optimizer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input and Locate Baseline Fixture
- **Workflow path**: Path to the workflow to benchmark (e.g., `graph/workflow.py`)
- **Test mode**: `full` | `quick` (quick = 10 samples; full = 50+ samples across diverse inputs)
- **Baseline fixture path**: Look for `tests/fixtures/baseline_metrics.json`; if absent, create a new baseline before any comparison
- Confirm `LANGSMITH_API_KEY` is exported in the current shell — all LLM cost data requires LangSmith trace data

### 2. Load or Create Baseline Fixture
- If baseline fixture exists, load it and extract `p50_ms`, `p95_ms`, `cost_per_req`, `quality_scores`
- If fixture is missing, run the workflow over the standard input set and record as the new baseline:

```python
import json, statistics, time
from pathlib import Path

def create_baseline_fixture(workflow_fn, inputs: list[dict], path: str | None = None):
    latencies, costs = [], []
    for inp in inputs:
        start = time.perf_counter()
        result = workflow_fn(inp)
        latencies.append((time.perf_counter() - start) * 1000)
        costs.append(result.get("cost_usd", 0))
    fixture = {
        "p50_ms": statistics.median(latencies),
        "p95_ms": sorted(latencies)[int(len(latencies) * 0.95)],
        "avg_cost_usd": sum(costs) / len(costs),
        "sample_count": len(latencies),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(fixture, indent=2))
    print(f"Baseline fixture created: {fixture}")
```

### 3. Run Performance Benchmark
- Execute the target workflow over the same standard input set used for the baseline
- Capture per-run timing with `time.perf_counter()` (not `time.time()` — insufficient precision)
- Pull LangSmith traces to get token counts and cost per run — local timing alone misses LLM cost
- Run at minimum 10 samples for quick mode, 50 for full mode; fewer samples produce non-deterministic results

### 4. Evaluate Against Thresholds
- Load thresholds from `env-config.yaml` (`validation` section) and compare:
  - P95 latency must not exceed baseline P95 (pass if no regression)
  - Cost per request must not exceed baseline cost by more than 5% tolerance
  - Quality scores (faithfulness / relevancy) must meet or exceed baseline values
- Generate a structured report and flag any metric that fails the gate

### 5. Emit Test Report and Gate Decision
- Write the test report to `tests/reports/benchmark_<timestamp>.json`
- Print a summary with PASS/FAIL for each metric
- If all gates pass: the workflow is cleared for merge or deployment
- If any gate fails: block and surface the specific failing metric with delta vs. threshold

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide workflow path and test mode (`full` or `quick`). |
| Baseline fixture not found at `tests/fixtures/baseline_metrics.json` | Auto-create baseline fixture on first run; warn that no comparison is possible until next run. |
| Non-deterministic timing detected (P95 variance > 30% across runs) | Increase sample count to 100; note potential environment instability (GC pauses, network jitter) in report. |
| A/B test inconclusive (p-value > 0.05) | Do not declare optimization valid. Collect additional samples per `ab_test_min_samples` (50 minimum). Log result as "inconclusive". |
| `LANGSMITH_API_KEY` not set | Stop. Token cost data is unavailable without LangSmith. Export the key before running benchmarks. |
| Quality evaluator returns NaN or None | Indicate missing evaluation chain; quality gate defaults to FAIL — do not assume quality is acceptable. |

## Examples

**Example 1**: `/test-workflow-optimizer graph/rag_chain.py quick`
- Runs 10 samples, compares to fixture; P95 is 12s vs 14s baseline (14% improvement) — all quality gates pass; PASS

**Example 2**: `/test-workflow-optimizer agents/multi_step.py full`
- Runs 50 samples; detects P95 variance of 40% — flags timing instability, increases to 100 samples; cost regressed 8% — quality gate blocks merge
