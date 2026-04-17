---
description: Generate comprehensive documentation for prompt templates (Prompt Engineer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Prompt path**: Path to prompt
- **Doc type**: full | api | changelog

### 2. Generate Documentation

**README:**
- Purpose and usage
- Parameters reference
- Examples
- Token estimates

**API Reference:**
- Function signatures
- Parameter types
- Return values

**Changelog:**
- Version history
- Breaking changes
- Migration notes

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
**Example**: `/document-prompt-engineer prompts/response.md full`
