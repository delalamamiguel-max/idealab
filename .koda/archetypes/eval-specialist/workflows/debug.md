---
description: Debug evaluation pipeline failures, grader errors, and async issues (Eval Specialist)
---

User input: $ARGUMENTS

## Execution Steps
1. Parse Input - eval path, issue type
2. Diagnose failure
3. Fix grader configuration
4. Add error handling
5. Validate

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
**Example**: `/debug-eval-specialist eval/pipeline.py "Grader timeout"`
