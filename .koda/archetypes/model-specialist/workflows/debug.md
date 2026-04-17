---
description: Diagnose and fix model configuration issues including timeouts, fallback failures, and cost overruns (Model Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Config path**: Path to the model config file under investigation (e.g., `config/models.py`)
- **Issue description**: Human-readable symptom — timeout, fallback not triggering, cost spike, wrong model selected
- **Environment**: `dev` | `staging` | `prod` — determines which env vars and rate-limit tiers to check

### 2. Reproduce the Failure
- Invoke the `ModelRouter` directly against the reported config and capture the raw exception or cost figure
- Attach `get_openai_callback()` to the failing call to see actual token counts vs. expected
- Log the full fallback chain traversal order — confirm `primary → fallback` sequence matches `MODEL_REGISTRY` declaration

```python
from langchain.callbacks import get_openai_callback
from templates.model_config_example import ModelRouter

router = ModelRouter(primary="gpt-4-turbo", fallback="gpt-3.5-turbo")

try:
    with get_openai_callback() as cb:
        model = router.get_model()
        response = model.invoke("Reproduce the failing prompt here.")
        print(f"Tokens used: {cb.total_tokens}, Cost: ${cb.total_cost:.4f}")
except Exception as exc:
    print(f"Primary failed: {exc!r} — attempting fallback")
    model = router.get_model(use_fallback=True)
    response = model.invoke("Reproduce the failing prompt here.")
```

### 3. Isolate Root Cause
- **Timeout**: Check `request_timeout` on the `ChatOpenAI` / `ChatAnthropic` constructor; default is often 60 s — insufficient for complex prompts
- **Fallback not triggering**: Confirm `fallback_config` is not `None` in `ModelRouter.__init__`; verify the exception type is one the router actually catches (e.g., `openai.APITimeoutError`, not a generic `ValueError`)
- **Cost overrun**: Inspect `max_tokens` cap in `ModelConfig`; verify the `cost_per_1k_tokens` in `MODEL_REGISTRY` reflects current provider pricing

### 4. Apply Fix
- For timeout issues: add explicit `request_timeout=120` and `max_retries=3` to the model constructor
- For fallback failures: wrap the primary invocation in a `try/except` that catches provider-specific errors and re-routes to `router.get_model(use_fallback=True)`
- For cost overruns: enforce a hard `max_tokens` ceiling in `ModelConfig` and add a pre-call token estimate guard

```python
from dataclasses import dataclass
from langchain_openai import ChatOpenAI

@dataclass
class ModelConfig:
    provider: str
    model_name: str
    temperature: float = 0.0
    max_tokens: int = 512          # cap enforced here — never unbounded
    cost_per_1k_tokens: float = 0.0
    request_timeout: int = 120     # explicit timeout — no silent hangs
    max_retries: int = 3           # retry before escalating to fallback
```

### 5. Validate the Fix
- Re-run the reproducer from Step 2 — confirm no exception and cost is within budget
- Trigger an intentional primary failure (e.g., pass an invalid API key for the primary) and confirm the fallback fires cleanly
- Check cost callback reports a non-zero figure — a `$0.00` reading means tracking is broken, not that the call was free

**Checklist:**
- [ ] Primary model responds without timeout under normal load
- [ ] Fallback activates when primary raises a provider error
- [ ] `total_cost` in callback is within the per-request budget
- [ ] No hardcoded API keys — all sourced from env vars

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide config path and a one-line description of the symptom. |
| `model-specialist-constitution.md` not found | Stop. Ensure file is present at repo root before debugging config. |
| `OPENAI_API_KEY` not set | Set the environment variable. Check `required_env_vars` in `templates/env-config.yaml` for the full list. |
| Primary model timeout | Increase `request_timeout` in `ModelConfig` and add `max_retries=3`. If timeout persists, route to a faster fallback (e.g., `gpt-3.5-turbo`) for the affected use case. |
| Fallback chain exhausted | All models in the chain have failed. Check provider status pages, verify all API keys are valid, and add a final `raise` with a user-facing error message rather than silently returning `None`. |
| Cost overrun detected | Set a hard `max_tokens` cap in `ModelConfig`. Add a pre-call token estimate check using `tiktoken` and reject requests that would exceed the per-request `budget`. |

## Examples

**Example 1**: `/debug-model-specialist config/models.py "Fallback not triggering on timeout"`

Agent reads `config/models.py`, discovers `ModelRouter` catches only `openai.RateLimitError` but not `openai.APITimeoutError`. Adds `APITimeoutError` to the except clause and raises the `request_timeout` from 30 s to 90 s. Re-runs the reproducer — fallback fires correctly.

**Example 2**: `/debug-model-specialist config/models.py "Cost spiking 10x on summarization tasks"`

Agent attaches `get_openai_callback()`, finds `max_tokens` is unset (defaults to model maximum). Adds `max_tokens=512` to the summarization `ModelConfig` entry and adds a `tiktoken`-based pre-flight check that rejects prompts exceeding 2 000 input tokens. Cost drops to expected range.
