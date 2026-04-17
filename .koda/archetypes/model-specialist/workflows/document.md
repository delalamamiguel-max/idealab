---
description: Generate comprehensive documentation for a model configuration — covering model choices, fallback logic, cost estimates, and usage guidelines (Model Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Config path**: Path to the model config file to document (e.g., `config/models.py` or `templates/model_config_example.py`)
- **Depth**: `summary` | `full` — `summary` produces a one-table overview; `full` produces per-model deep-dives, cost estimates, and a usage guide
- **Output path**: Where to write the generated docs (default: `docs/model-config.md`)

### 2. Introspect the Configuration
- Parse `MODEL_REGISTRY` and extract every `ModelConfig` entry: `provider`, `model_name`, `temperature`, `max_tokens`, `cost_per_1k_tokens`
- Walk every `ModelRouter` instance in the codebase and document its `primary` → `fallback` chain topology
- Flag any model that is referenced in a router but absent from `MODEL_REGISTRY` — this is a documentation gap and a constitution violation

```python
from templates.model_config_example import MODEL_REGISTRY, ModelRouter

print("## Model Registry\n")
print(f"{'Key':<22} | {'Provider':<12} | {'Model Name':<35} | {'Temp':>5} | {'Max Tok':>8} | {'USD per 1k':>12}")
print("-" * 100)
for key, cfg in MODEL_REGISTRY.items():
    print(
        f"{key:<22} | {cfg.provider:<12} | {cfg.model_name:<35} | "
        f"{cfg.temperature:>5.1f} | {cfg.max_tokens:>8} | ${cfg.cost_per_1k_tokens:>7.5f}"
    )
```

### 3. Generate Cost Estimates
- For each model, calculate illustrative per-request costs at three prompt sizes: 500 tokens, 2 000 tokens, 8 000 tokens
- Produce a monthly cost projection at three usage tiers: 1 k requests/day, 10 k/day, 100 k/day
- Highlight which model becomes cost-prohibitive above a certain volume — this is actionable data for capacity planning

```python
PROMPT_SIZES = [500, 2_000, 8_000]
DAILY_VOLUMES = [1_000, 10_000, 100_000]

for key, cfg in MODEL_REGISTRY.items():
    print(f"\n### {key} cost estimates")
    for tokens in PROMPT_SIZES:
        cost_per_call = (tokens / 1_000) * cfg.cost_per_1k_tokens
        for volume in DAILY_VOLUMES:
            monthly = cost_per_call * volume * 30
            print(f"  {tokens:>6} tokens × {volume:>7} daily requests -> USD {monthly:>10,.2f} monthly")
```

### 4. Document Fallback Logic and Routing Rules
- For each `ModelRouter` definition found, render the chain as a numbered list: `1. primary → 2. fallback → 3. final error`
- Document the conditions under which each hop fires: which exception types trigger the next tier
- Note semantic routing rules if `ModelRouter` uses task-type dispatch — explain which task categories route to which model and why

### 5. Write the Documentation File
- Assemble all sections: Registry table, cost estimates, fallback topology, environment variables required, upgrade/deprecation notes
- Write to the `output_path` specified in Step 1
- Add a `## Maintenance` section that lists the model version pinned, the provider deprecation notice URL, and a suggested review cadence (quarterly minimum)

**Checklist:**
- [ ] Every entry in `MODEL_REGISTRY` has a documented description and use-case note
- [ ] Every `ModelRouter` chain is rendered in the docs
- [ ] Cost estimates are present for at least three usage volumes
- [ ] `## Maintenance` section includes provider changelog URLs and review cadence

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide config path and depth (`summary` / `full`). |
| `model-specialist-constitution.md` not found | Stop. Ensure file is present at repo root — it defines the documentation standards to comply with. |
| `OPENAI_API_KEY` not set | Documentation generation does not require live API calls, but include a note in the output that env vars must be set before the config can be exercised. |
| Missing model version in config | A `ModelConfig` entry has a vague `model_name` (e.g., `"gpt-4"` without date suffix). Flag it in the docs with a `⚠ UNVERSIONED` warning and recommend pinning to a dated alias (e.g., `"gpt-4-0125-preview"`). |
| Undocumented fallback logic | A `ModelRouter` is instantiated with a `fallback` parameter but no comment explains why that fallback was chosen. Insert a `# fallback rationale:` comment and document the reasoning in the generated docs. |
| Broken provider links | Provider documentation or changelog URLs are stale (return 404). Replace with the current canonical URL from the provider's official docs site and add a last-verified date. |

## Examples

**Example 1**: `/document-model-specialist config/models.py full`

Agent parses `MODEL_REGISTRY` (4 models), `ModelRouter` instances (3 chains), and generates a `docs/model-config.md` with a registry table, three-tier cost projection, fallback topology diagrams, and a `## Maintenance` section pointing to OpenAI and Anthropic deprecation calendars.

**Example 2**: `/document-model-specialist templates/model_config_example.py summary docs/quick-ref.md`

Agent produces a compact single-table summary in `docs/quick-ref.md`: one row per model, columns = provider / name / temperature / cost-per-1k / recommended-use-case. Flags `"gpt-4"` as unversioned and recommends pinning. Output is under 40 lines — suitable for a README embed.
