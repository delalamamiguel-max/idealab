---
description: Fix prompt issues including poor outputs, format failures, and hallucinations (Prompt Engineer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Prompt path**: Path to problematic prompt
- **Issue type**: poor_output | format_failure | hallucination | inconsistent
- **Sample**: Example of the failure

### 2. Diagnose Issue
- Review prompt structure
- Check examples quality
- Analyze constraint clarity
- Test with variations

### 3. Apply Fix
- Strengthen instructions
- Add negative examples
- Clarify constraints
- Improve output schema

### 4. Validate Fix
- Test with original failure case
- Run regression tests
- Verify no new issues

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
**Example**: `/debug-prompt-engineer prompts/extract.md hallucination "Model made up data not in context"`
