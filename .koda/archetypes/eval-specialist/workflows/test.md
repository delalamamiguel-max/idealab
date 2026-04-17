---
description: Validate evaluation pipeline for quality, fairness, and promotion readiness (Eval Specialist)
---

User input: $ARGUMENTS

## Execution Steps
1. Parse Input - eval path
2. Run evaluation tests
3. Check grader accuracy
4. Validate SOX compliance
5. Generate report

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
**Example**: `/test-eval-specialist eval/pipeline.py`
