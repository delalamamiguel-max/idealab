---
description: Generate comprehensive documentation for evaluation pipeline (Eval Specialist)
---

User input: $ARGUMENTS

## Execution Steps
1. Parse Input - eval path
2. Document graders
3. Create threshold guide
4. Generate SOX evidence docs

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide eval name, metrics list, and SOX scope flag. |
| `eval-specialist-constitution.md` not found | Stop. Ensure file is present at repo root. |
| `deepeval` not installed | Run `pip install deepeval`. Check `available_libraries` in `templates/env-config.yaml`. |
| Grader returns error instead of score | Inspect grader logs. Verify test case has required fields (prompt, context, expected). |
| SOX Phoenix endpoint unreachable | Check `PHOENIX_ENDPOINT` env var is set. Verify network access. |
| All tests fail | Verify LLM API key is set and the judge model is accessible. |

## Examples
**Example**: `/document-eval-specialist eval/pipeline.py full`
