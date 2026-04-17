---
description: Run a structured head-to-head comparison of two or more models for a specific use case, producing a decision matrix and recommendation (Model Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Models**: Two or more model keys from `MODEL_REGISTRY` (e.g., `"gpt-4-turbo vs claude-3-opus"`)
- **Use case**: Task category that drives evaluation rubric — `summarization` | `code-gen` | `reasoning` | `extraction` | `chat`
- **Sample size**: Number of evaluations per model (default 15 — minimum for statistical significance)
- **Budget cap**: Maximum total spend for the comparison run (prevents runaway cost on large models)

### 2. Normalize the Comparison Setup
- Instantiate each candidate via `ModelRouter` with identical parameters: `temperature=0.0`, same `max_tokens`, same system prompt
- Confirm both models are present in `MODEL_REGISTRY` before invoking anything — reject unknown keys immediately
- Generate or load `sample_size` prompts representative of the `use case`; ensure prompts are neither trivially easy nor pathologically hard

```python
from templates.model_config_example import MODEL_REGISTRY, ModelRouter

MODELS_TO_COMPARE = ["gpt-4-turbo", "claude-3-opus"]
USE_CASE = "summarization"
SAMPLE_SIZE = 15

for key in MODELS_TO_COMPARE:
    if key not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model key '{key}' — add it to MODEL_REGISTRY first.")

routers = {
    key: ModelRouter(primary=key, fallback="gpt-3.5-turbo")
    for key in MODELS_TO_COMPARE
}
```

### 3. Run Blind Evaluation
- Invoke each model on every prompt with `get_openai_callback()` to capture cost and token counts
- Store responses without model labels — use a neutral evaluator (LLM-as-judge or human) to score each response on the rubric before revealing which model produced it
- Score each response on three axes: **correctness** (0–10), **conciseness** (0–10), **instruction-following** (0–5)

```python
import time
from langchain.callbacks import get_openai_callback

comparison_log = {key: [] for key in MODELS_TO_COMPARE}

for prompt in eval_prompts:
    for key, router in routers.items():
        model = router.get_model()
        t0 = time.perf_counter()
        with get_openai_callback() as cb:
            resp = model.invoke(prompt)
        comparison_log[key].append({
            "prompt": prompt,
            "response": resp.content,
            "latency_s": time.perf_counter() - t0,
            "cost_usd": cb.total_cost,
            "tokens": cb.total_tokens,
        })
```

### 4. Build the Decision Matrix
- Compute per-model aggregates: mean quality score, mean latency, total cost, P95 latency
- Produce a Markdown decision matrix with rows = models, columns = metric axes
- Highlight the winner per column; declare an overall winner only if it leads on ≥ 2 of 3 axes
- If costs are tied within 10% and quality scores within 0.5 points, declare the comparison inconclusive and recommend increasing `sample_size`

### 5. Deliver Recommendation
- Select the model that best fits the stated use-case priority (quality / cost / latency)
- Document the recommendation in `MODEL_REGISTRY` as a comment: `# recommended for: <use_case>`
- If the result is inconclusive on cost or quality, recommend a longer A/B test in staging before production promotion

**Checklist:**
- [ ] Both models invoked with identical `temperature`, `max_tokens`, and system prompt
- [ ] Budget cap enforced — abort if `total_cost_usd` exceeds cap mid-run
- [ ] Blind scoring completed before model labels are revealed
- [ ] Decision matrix saved to `compare-results/model-compare-<use_case>-<date>.md`

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide model list, use case, and optional sample size. |
| `model-specialist-constitution.md` not found | Stop. Ensure file is present at repo root before running comparison. |
| `OPENAI_API_KEY` not set | Set the environment variable. For Anthropic models also set `ANTHROPIC_API_KEY`. Check `templates/env-config.yaml`. |
| Insufficient samples for comparison | `sample_size` < 10 produces unreliable means. Warn user, increase to minimum 10, or stop if budget cap prevents it. Never report a winner from fewer than 10 samples. |
| Cost tied between models | Both models fall within 10% cost of each other. Flag as tie on cost axis. Base the recommendation on quality delta or latency delta instead — do not flip a coin. |
| Quality ambiguous | Quality scores differ by < 0.5 / 10 across `sample_size` prompts. Declare quality a tie, recommend increasing sample size to 30+ or using a human evaluation panel before making a production decision. |

## Examples

**Example 1**: `/compare-model-specialist "gpt-4-turbo vs claude-3-sonnet" summarization`

Agent runs 15 news article summarization prompts blind. `gpt-4-turbo` scores 8.6 quality / 2.1 s latency / `$0.0380` total; `claude-3-sonnet` scores 8.4 quality / 1.7 s latency / `$0.0045` total. Agent recommends `claude-3-sonnet` as cost-dominant (8.4× cheaper, near-identical quality, faster).

**Example 2**: `/compare-model-specialist "gpt-4o vs claude-3-opus" reasoning budget=2.00`

Agent runs 15 multi-step reasoning prompts. Budget cap triggers at 12 `claude-3-opus` calls. Agent reports partial results (12/15), flags budget exhaustion, and recommends reducing `max_tokens` from 2 048 to 512 for this use case before re-running the full comparison.
