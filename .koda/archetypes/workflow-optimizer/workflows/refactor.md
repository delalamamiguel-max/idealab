---
description: Apply and validate structural optimizations to Workflow Optimizer workflows
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input and Define Optimization Scope
- **Workflow path**: File to refactor (e.g., `graph/workflow.py`)
- **Optimization type**: `caching` | `parallelism` | `model-swap` | `prompt-compression` | `batching`
- **Target metric**: latency reduction % or cost reduction % from `env-config.yaml` defaults (20% / 30%)
- Reject the request if no baseline measurement exists — the constitution hard-stops blind optimization

### 2. Establish Pre-Refactor Baseline (Mandatory Gate)
- Run 30+ samples through the current workflow and record P50/P95 latency and cost per request
- Tag this baseline run in LangSmith with `pre-refactor-<timestamp>` for later diff:

```python
from langsmith import Client, traceable
import time, statistics

@traceable(name="pre-refactor-baseline", tags=["baseline"])
def run_baseline(workflow_fn, inputs: list[dict]) -> dict:
    latencies = []
    for inp in inputs:
        start = time.perf_counter()
        workflow_fn(inp)
        latencies.append((time.perf_counter() - start) * 1000)
    p95 = sorted(latencies)[int(len(latencies) * 0.95)]
    return {"p50": statistics.median(latencies), "p95": p95, "samples": len(latencies)}
```

- **Hard stop**: If the baseline `p95` is already below the stated target, re-evaluate if optimization is needed

### 3. Apply One Refactor Change
- Implement a single, isolated optimization — per the constitution, never stack multiple changes before measuring:
  - **Caching**: Add `langchain.cache.InMemoryCache()` or semantic cache at the LLM call level
  - **Parallelism**: Refactor sequential retrieval + tool calls into `asyncio.gather()` blocks
  - **Prompt compression**: Reduce system prompt tokens while validating the quality gate holds
  - **Model swap**: Downgrade to a cheaper/faster model on low-risk steps only
- Commit this change in isolation — one PR per optimization so rollback is surgical

### 4. Measure Post-Refactor Improvement
- Re-run the same 30+ sample set against the refactored workflow
- Compute improvement ratio and confirm it meets the target:

```python
improvement = (baseline_p95 - refactored_p95) / baseline_p95
if improvement < 0.20:  # latency_reduction_target from env-config.yaml
    raise ValueError(f"Target not met: {improvement:.1%} < 20%. Do not merge.")
print(f"Latency improvement: {improvement:.1%} ✓")
```

- If the target is not met, discard the change and try the next optimization type from Step 3

### 5. Quality Gate Validation
- Run the quality evaluator against the refactored workflow on the same inputs:
  - Faithfulness ≥ pre-refactor score (no tolerance for quality loss)
  - Relevancy ≥ pre-refactor score
  - Any regression triggers a **HARD STOP** and automatic revert
- Document the selected trade-off (cost vs. latency) and rationale in `OPTIMIZATION_LOG.md`

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide workflow path, optimization type, and target metric. |
| No pre-refactor baseline captured | Stop. Per constitution, blind optimization is forbidden. Run baseline measurement first. |
| Quality regression detected (hard stop) | Immediately revert the change. Document regression in `OPTIMIZATION_LOG.md`. Do not retry the same approach. |
| Post-refactor latency target not met | Discard change. Try a different optimization type. Log the failed attempt and measured delta. |
| Post-refactor cost increased vs. baseline | Flag as a cost regression. If the latency win is significant, document the trade-off; human approval required before merging. |
| Constitution file not found | Stop. Ensure `workflow-optimizer-constitution.md` is present at repo root before any refactor. |

## Examples

**Example 1**: `/refactor-workflow-optimizer graph/rag_chain.py caching target=30%cost`
- Adds `InMemoryCache` at embedding call site; baseline 50 samples show 34% cost reduction; quality unchanged — merged

**Example 2**: `/refactor-workflow-optimizer agents/multi_step.py parallelism target=20%latency`
- Discovers retrieval + tool-call are sequential; wraps in `asyncio.gather()`; P95 drops from 14s to 9s (35%) — quality gate passes
