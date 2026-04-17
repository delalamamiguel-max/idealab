---
description: Compare prompt variants for quality, cost, and performance (Prompt Engineer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Prompts**: List of prompt variants to compare
- **Criteria**: quality | cost | latency | all
- **Test set**: Evaluation dataset

### 2. Run Comparison

| Variant | Tokens | Quality | Latency | Cost/1k |
|---------|--------|---------|---------|---------|
| A | {tokens} | {score} | {ms} | ${cost} |
| B | {tokens} | {score} | {ms} | ${cost} |

### 3. Generate Recommendation
- Best for quality: {variant}
- Best for cost: {variant}
- Recommended: {variant}

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide prompt name, purpose, target model, and domain. |
| `prompt-engineer-constitution.md` not found | Stop. Ensure file is present at repo root (not inside a subdirectory). |
| `tiktoken` or `jinja2` not installed | Run `pip install tiktoken jinja2`. |
| Token count exceeds model limit | Reduce few-shot examples or truncate context. Check `token_limits` in `templates/env-config.yaml`. |
| PII detected in prompt template | HARD STOP per constitution. Remove or mask PII before use. Do not proceed with PII-containing prompts. |
| Generated prompt fails golden test | Review constitutional rules for the domain. Adjust template structure, not just wording. |

## Examples
**Example**: `/compare-prompt-engineer "v1.md vs v2.md" quality`
