---
description: Optimize existing prompts for token efficiency, clarity, and model compatibility (Prompt Engineer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Prompt path**: Path to existing prompt
- **Goal**: token_reduction | clarity | compatibility | all

### 2. Analyze Current Prompt
- Count tokens
- Check model compatibility
- Identify redundancies
- Assess clarity

### 3. Generate Optimizations
- Remove redundant instructions
- Consolidate examples
- Optimize for target model
- Improve instruction clarity

### 4. Validate Changes
- Run existing tests
- Compare outputs
- Verify token reduction

### 5. Update Version
- Bump version number
- Document changes in changelog

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
**Example**: `/refactor-prompt-engineer prompts/response.md token_reduction`
