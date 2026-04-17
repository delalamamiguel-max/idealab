---
description: Refactor evaluation pipeline for improved maintainability, performance, and compliance (Eval Specialist)
---

User input: $ARGUMENTS

## Execution Steps
1. Parse Input - eval path, goal (accuracy, speed, compliance)
2. Analyze current pipeline
3. Identify improvements
4. Apply refactorings
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
**Example**: `/refactor-eval-specialist eval/pipeline.py accuracy`
