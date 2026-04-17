---
description: Optimize model configuration for cost, quality, or latency — including provider migration and fallback restructuring (Model Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Config path**: File to refactor (e.g., `config/models.py` or `templates/model_config_example.py`)
- **Goal**: One of `cost` | `quality` | `latency` — determines which optimization axis drives the refactor
- **Scope**: `primary-only` | `full-chain` — whether to touch only the primary model or restructure the entire fallback chain

### 2. Audit the Current Configuration
- List every `ModelConfig` entry in `MODEL_REGISTRY` and annotate each with its current `cost_per_1k_tokens`, `temperature`, and `max_tokens`
- Identify any hardcoded model name strings outside of `MODEL_REGISTRY` — these are violations of the constitution's "no hardcoded models" rule
- Check whether temperatures are task-appropriate: factual retrieval should be `0.0`, creative generation `0.7–1.0`, general Q&A `0.2–0.4`

```python
from templates.model_config_example import MODEL_REGISTRY

for name, cfg in MODEL_REGISTRY.items():
    print(
        f"{name:20s} | provider={cfg.provider:10s} | "
        f"temp={cfg.temperature} | max_tokens={cfg.max_tokens} | "
        f"USD {cfg.cost_per_1k_tokens} per 1k tokens"
    )
```

### 3. Apply Goal-Specific Optimizations

**If `goal=cost`:**
- Downgrade the primary to a cheaper model (e.g., `gpt-4-turbo` → `gpt-4o-mini`) when quality metrics allow
- Set `max_tokens` to the tightest value that still satisfies the use case
- Enable request caching for idempotent prompts — duplicate calls should not cost anything

**If `goal=quality`:**
- Upgrade the primary to the highest-capability model (`gpt-4o`, `claude-3-opus`)
- Add a second fallback tier so failure does not silently degrade to a weak model
- Lower `temperature` to `0.0` for structured outputs; add `response_format={"type": "json_object"}` where applicable

**If `goal=latency`:**
- Switch primary to a low-latency model (e.g., `gpt-4o-mini`, `claude-3-haiku`)
- Enable streaming on the model constructor and return first token ASAP
- Raise `max_tokens` slightly to avoid mid-response truncation that forces retries

```python
from dataclasses import dataclass, replace
from templates.model_config_example import MODEL_REGISTRY, ModelConfig

# Example: cost refactor — swap gpt-4 for gpt-4o-mini
MODEL_REGISTRY["gpt-4-turbo"] = replace(
    MODEL_REGISTRY["gpt-4-turbo"],
    model_name="gpt-4o-mini",
    cost_per_1k_tokens=0.00015,
    max_tokens=512,
)
```

### 4. Restructure Fallback Chain if Needed
- Verify the fallback order in `ModelRouter` matches the optimization goal: cheapest or fastest model should be the final fallback
- If a provider has deprecated a model referenced in `MODEL_REGISTRY`, update the `model_name` field and add a `# deprecated: <old_name>` comment
- After restructuring, serialize the updated registry to `MODEL_REGISTRY` and confirm no entry references a sunset model name

### 5. Validate Refactored Config
- Run `get_openai_callback()` side-by-side against old vs. new config on the same prompt set
- Confirm the optimization goal is met: cost ↓ / quality score ↑ / P95 latency ↓
- Assert no constitution violations remain: no bare model strings, no missing fallbacks, no unbounded `max_tokens`

**Checklist:**
- [ ] All model names sourced from `MODEL_REGISTRY` — no inline string literals
- [ ] At least one fallback defined per `ModelRouter` instance
- [ ] `max_tokens` explicitly set on every `ModelConfig` entry
- [ ] Cost callback confirms optimization goal is achieved vs. baseline

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide config path and optimization goal (`cost` / `quality` / `latency`). |
| `model-specialist-constitution.md` not found | Stop. Ensure the constitution file is at repo root — it defines non-negotiable refactoring guardrails. |
| `OPENAI_API_KEY` not set | Set the environment variable before validating the refactored config. Check `required_env_vars` in `templates/env-config.yaml`. |
| Model deprecation | The model name in `MODEL_REGISTRY` is no longer available from the provider. Update `model_name` to the current equivalent and add a migration comment. Re-run validation. |
| Breaking API change in provider | Provider has changed request schema or response format. Check provider changelog, update `ChatOpenAI` / `ChatAnthropic` constructor kwargs, and pin the SDK version in `requirements.txt`. |
| Fallback order change | Reordering the fallback chain can alter cost and quality characteristics. Document the change reason in a comment and re-run the side-by-side cost/quality comparison before committing. |

## Examples

**Example 1**: `/refactor-model-specialist config/models.py cost`

Agent audits `MODEL_REGISTRY`, finds `gpt-4-turbo` used for a simple FAQ retrieval task. Swaps to `gpt-4o-mini` (98% cost reduction), sets `max_tokens=256`, adds response caching. Side-by-side callback confirms cost drops from `$0.0600/call` to `$0.0009/call` with no quality regression on the benchmark set.

**Example 2**: `/refactor-model-specialist config/models.py quality full-chain`

Agent finds `claude-3-sonnet` as primary for a complex legal analysis agent. Upgrades primary to `claude-3-opus`, adds `gpt-4o` as a second-tier fallback (cross-provider resilience), sets `temperature=0.0` and `response_format=json_object`. LLM-as-judge score improves from 7.1 → 8.9 / 10.
