---
description: Validate prompt quality with golden tests, token counting, and output verification (Prompt Engineer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Prompt path**: Path to prompt
- **Test scope**: unit | golden | integration | all

### 2. Run Tests

**Unit Tests:**
- Prompt renders correctly
- Parameters validated
- Token count within limits

**Golden Tests:**
- Compare against expected outputs
- Check format compliance
- Verify consistency

**Integration Tests:**
- Test with actual model
- Verify output quality
- Check latency

### 3. Generate Report
```markdown
## Prompt Test Report

### Summary
- Tests: {total}
- Passed: {passed}
- Failed: {failed}

### Token Analysis
- Base: {base_tokens}
- Typical: {typical_tokens}
- Max: {max_tokens}

### Quality Scores
- Format compliance: {score}%
- Consistency: {score}%
```

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
**Example**: `/test-prompt-engineer prompts/response.md all`
