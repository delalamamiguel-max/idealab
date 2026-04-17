---
description: Configure LLM models with fallback chains, cost tracking, and optimization (Model Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Use case**: Task type for model selection
- **Priority**: quality | cost | latency
- **Budget**: Cost constraints

### 2. Generate Model Configuration

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

class ModelConfig:
    primary = ChatOpenAI(model="gpt-4-turbo", temperature=0)
    fallback = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    @classmethod
    def get_model(cls, task_complexity: str):
        if task_complexity == "high":
            return cls.primary
        return cls.fallback
```

### 3. Add Cost Tracking

```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = model.invoke(prompt)
    print(f"Cost: ${cb.total_cost:.4f}")
```

### 4. Validate

Run these checks before declaring the model config production-ready:

```python
# Run with the active environment interpreter
# Test API connectivity for primary model
from langchain_openai import ChatOpenAI
m = ChatOpenAI(model="gpt-4-turbo")
print(m.invoke("ping").content)
```

```python
# Run with the active environment interpreter
# Test fallback model connectivity
from langchain_openai import ChatOpenAI
m = ChatOpenAI(model="gpt-3.5-turbo")
print(m.invoke("ping").content)
```

**Checklist:**
- [ ] Primary model responds within latency target (check `priority` setting from Step 1)
- [ ] Fallback model responds when primary is unavailable
- [ ] Cost callback reports non-zero cost (confirms tracking is active)
- [ ] If `priority=latency`: verify P95 response time ≤ configured threshold
- [ ] If `priority=cost`: verify cost per call is within `budget` from Step 1
- [ ] If `priority=quality`: verify response passes a spot-check LLM-as-judge evaluation
- [ ] No hardcoded API keys in generated config — all come from environment variables

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide use case, priority (quality/cost/latency), and budget. |
| `model-specialist-constitution.md` not found | Stop. Ensure file is present at repo root. |
| `OPENAI_API_KEY` not set | Set the environment variable before running. Check `required_env_vars` in `templates/env-config.yaml`. |
| Primary model rate-limited | Fallback chain will activate automatically if configured. Otherwise set `max_retries=3` on the model. |
| Cost callback shows $0.00 | Verify you are using `get_openai_callback()` correctly and the model is not cached. For Anthropic models, use a compatible callback instead of `get_openai_callback()`. |
| Latency target not met | Switch `priority` to `cost` or `quality` tier, or add streaming to reduce time-to-first-token. |

## Examples
**Example**: `/scaffold-model-specialist reasoning quality budget=1.0`

