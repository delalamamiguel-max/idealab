---
description: Benchmark models for quality, cost, and latency across realistic prompts (Model Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Models to test**: Comma-separated list from `MODEL_REGISTRY` keys (e.g., `"gpt-4-turbo, gpt-4o-mini, claude-3-sonnet"`)
- **Test suite**: Path to a JSONL file of `{"prompt": "...", "expected": "..."}` records, or `"auto"` to generate 10 prompts from the use case
- **Metrics**: One or more of `quality` | `cost` | `latency` — determines what the test harness measures

### 2. Build the Test Harness
- Load the test suite and validate each record has `prompt` and `expected` fields
- Instantiate a `ModelRouter` for each candidate model, with a neutral shared fallback (e.g., `gpt-3.5-turbo`) to prevent cross-contamination between test subjects
- Wire `get_openai_callback()` around every invocation to capture per-call cost and token counts

```python
import time
from langchain.callbacks import get_openai_callback
from templates.model_config_example import ModelRouter

CANDIDATES = ["gpt-4-turbo", "gpt-4o-mini", "claude-3-sonnet"]
TEST_PROMPTS = [
    {"prompt": "Summarize in one sentence: The quick brown fox.", "expected": "fox jumps"},
    {"prompt": "What is 2 + 2?", "expected": "4"},
]

results = {}
for model_key in CANDIDATES:
    router = ModelRouter(primary=model_key, fallback="gpt-3.5-turbo")
    model = router.get_model()
    latencies, costs = [], []
    for record in TEST_PROMPTS:
        t0 = time.perf_counter()
        with get_openai_callback() as cb:
            resp = model.invoke(record["prompt"])
        latencies.append(time.perf_counter() - t0)
        costs.append(cb.total_cost)
    results[model_key] = {
        "avg_latency_s": sum(latencies) / len(latencies),
        "total_cost_usd": sum(costs),
    }
```

### 3. Measure Quality
- For each response, compute an exact-match score where `expected` is a substring check, and a semantic-similarity score using an embedding model
- Optionally run LLM-as-judge: send `(prompt, response)` pairs to a cheap evaluator model (e.g., `gpt-4o-mini`) with a 1–10 rubric
- Record pass/fail per prompt per model — flag any model that fails more than 20% of the test suite

### 4. Aggregate and Report
- Produce a Markdown table with columns: `model`, `avg_latency_s`, `total_cost_usd`, `quality_score`, `pass_rate`
- Highlight the Pareto-optimal model for each metric axis (cheapest, fastest, highest quality)
- Flag any model that returned non-deterministic results across identical prompts — set `temperature=0.0` to reduce variance before comparing

```python
print(f"{'Model':<20} | {'Avg Latency':>12} | {'Total Cost':>12} | {'Pass Rate':>10}")
print("-" * 62)
for key, r in sorted(results.items(), key=lambda x: x[1]["total_cost_usd"]):
    print(f"{key:<20} | {r['avg_latency_s']:>10.2f}s | USD {r['total_cost_usd']:>10.4f} | {r.get('pass_rate', 'unknown'):>10}")
```

### 5. Make a Recommendation
- If `priority=cost`: recommend the model with the lowest `total_cost_usd` that still meets a minimum `pass_rate` threshold (default 80%)
- If `priority=latency`: recommend the lowest `avg_latency_s` model that meets the cost budget
- If `priority=quality`: recommend the highest `quality_score` model; flag if the cost delta vs. second place exceeds 5×
- Write results to `test-results/model-benchmark-<date>.json` for audit trail

**Checklist:**
- [ ] All candidate models successfully invoked at least once
- [ ] `get_openai_callback()` returned non-zero cost for every OpenAI call
- [ ] Temperature set to `0.0` for determinism during comparative testing
- [ ] Benchmark results saved to `test-results/` — not discarded after display

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide model list, test suite path (or `"auto"`), and metrics to measure. |
| `model-specialist-constitution.md` not found | Stop. Ensure file is present at repo root before running benchmarks. |
| `OPENAI_API_KEY` not set | Set the environment variable. For Anthropic models also set `ANTHROPIC_API_KEY`. Check `templates/env-config.yaml`. |
| Non-deterministic responses | Set `temperature=0.0` on all candidate models before comparing. If variance persists at `temperature=0.0`, use a larger sample (≥20 prompts) and compare means, not individual responses. |
| Rate limit during test | Implement exponential back-off between test calls (`time.sleep(2**attempt)`). Reduce test parallelism or spread calls across multiple API keys if the suite is large. |
| Missing API key fixture | A candidate model's provider key is absent. Skip that model, log a `SKIP` result in the report, and proceed with remaining candidates rather than aborting the full suite. |

## Examples

**Example 1**: `/test-model-specialist "gpt-4-turbo, gpt-4o-mini" quality`

Agent runs 10 auto-generated summarization prompts against both models. `gpt-4-turbo` scores 9.1/10 quality at `$0.0420/run`; `gpt-4o-mini` scores 8.3/10 at `$0.0009/run`. Agent flags `gpt-4o-mini` as Pareto-optimal for cost-sensitive deployments with acceptable quality.

**Example 2**: `/test-model-specialist "claude-3-sonnet, claude-3-opus" latency test_suites/legal_qa.jsonl`

Agent benchmarks both Anthropic models on a 25-prompt legal Q&A suite. `claude-3-sonnet` averages 1.8 s latency vs. 4.2 s for `claude-3-opus`. Quality scores are within 0.4 points. Agent recommends `claude-3-sonnet` for latency-sensitive legal chatbot, `claude-3-opus` for async batch analysis only.
