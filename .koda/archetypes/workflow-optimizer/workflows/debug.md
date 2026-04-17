---
description: Debug performance regressions and profiling anomalies in Workflow Optimizer
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input and Establish Debug Context
- **Workflow path**: Path to the workflow file exhibiting the regression (e.g., `graph/workflow.py`)
- **Symptom description**: Specific regression — e.g., "P95 latency increased from 8s to 22s after parallelization refactor"
- **Baseline reference**: Identify the last known-good LangSmith run ID or timestamp to diff against
- **Environment check**: Confirm `LANGSMITH_API_KEY` is set and the project slug matches the target environment

### 2. Capture Current Performance Profile
- Open the LangSmith dashboard for the affected project and filter traces to the regression window
- Use the profiling helper to capture current P95 / P50 latency and cost per request:

```python
from langsmith import Client
import statistics

client = Client()
# Pull last 50 traces for the affected run name
runs = list(client.list_runs(project_name="workflow-optimizer", limit=50, run_type="chain"))
latencies = [(r.end_time - r.start_time).total_seconds() * 1000 for r in runs if r.end_time]
p50 = statistics.median(latencies)
p95 = sorted(latencies)[int(len(latencies) * 0.95)]
print(f"P50: {p50:.1f}ms  P95: {p95:.1f}ms  Samples: {len(latencies)}")
```

- Record token usage per run: `total_tokens`, `prompt_tokens`, `completion_tokens`
- Flag any runs with zero-ms duration — these indicate broken LangSmith instrumentation, not genuine sub-millisecond speed

### 3. Isolate Root Cause via Trace Diff
- Compare the current trace tree against the baseline run ID in LangSmith:
  - Identify which span (retrieval, LLM call, tool invocation) gained the most latency delta
  - Look for new sequential spans that could be parallelised, or newly added LLM calls not present before
  - Check if any caching layer that previously hit is now missing (cache miss rate spike)
- If the bottleneck is in an LLM call: verify model name and temperature haven't silently changed
- If the bottleneck is in retrieval: check vector store index health and embedding batch sizes

### 4. Apply Targeted Fix
- Implement precisely the minimum change needed to address the identified span:
  - Sequential → parallel: wrap independent steps with `asyncio.gather()`
  - Cache miss: restore or fix the semantic cache key computation
  - Model regression: pin the model name and log the change with rationale
- Re-run the profile snippet from Step 2 immediately after the fix (do NOT skip this)
- Compare new P95 against the baseline — the fix is only valid if P95 returned to ≤ baseline + 5% tolerance

### 5. Validate and Lock Down
- Run the full quality gate: faithfulness, relevancy, and groundedness scores must not have regressed
- Document the root cause, fix applied, and before/after latency in the repo's `OPTIMIZATION_LOG.md`
- If latency is restored but quality has regressed: **HARD STOP** — revert the fix and escalate

### 6. Document and Rollback-Proof
- Write a rollback entry in `OPTIMIZATION_LOG.md` with the revert command (e.g., `git revert <sha>`) so the fix can be undone in < 5 minutes if a production incident surfaces post-deploy
- Tag the LangSmith run that represents the post-fix baseline so future debug sessions have a clean reference point
- If the fix required a dependency version change, pin it explicitly in `requirements.txt` and document the minimum compatible version

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide workflow path, symptom description, and baseline run ID or timestamp. |
| `LANGSMITH_API_KEY` not set | Stop. Export the key: `export LANGSMITH_API_KEY=<key>`. All profiling requires LangSmith tracing to be active. |
| Baseline run ID not found in LangSmith | Ask user for a valid run ID or time window; without a baseline, diff-based debugging is impossible. |
| All latency samples return 0ms | LangSmith instrumentation is broken — not a performance win. Verify `langsmith.traceable` decorator is applied and `LANGCHAIN_TRACING_V2=true` is set. |
| Profiling timeout exceeded (>30s per run) | Reduce `limit` to 10 samples; if still timing out, the workflow itself may be the regression — profile with a minimal input first. |
| `LANGSMITH_API_KEY` valid but project not found | Confirm project name matches exactly; LangSmith project names are case-sensitive. |

## Examples

**Example 1**: `/debug-workflow-optimizer graph/workflow.py "P95 jumped from 6s to 18s after caching PR merged"`
- Pulls last 50 traces, diffs against pre-merge run, discovers semantic cache key changed — fix: restore prior key format

**Example 2**: `/debug-workflow-optimizer agents/rag_agent.py "Cost per request tripled overnight"`
- Profile reveals a new fallback LLM chain added that fires on every request — fix: gate it behind the failure condition
