---
description: Compare validation approaches and threshold configurations (Agent Validator)
---

User input: $ARGUMENTS

## Execution Steps
1. Parse Input - validation configs to compare
2. Run comparison on test set
3. Measure precision/recall
4. Recommend optimal config

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide agent path, validation type, and scope. |
| `agent-validator-constitution.md` not found | Stop. Ensure file is present at repo root. |
| Environment validation utility unavailable | Manually verify Python ≥3.10, deepeval, playwright are installed. |
| Assertion helper import fails | Check `scripts/assertion_helpers.py` exists in repo and is importable. |
| No test cases generated | Verify agent output format matches expected schema before validation. |
| All tests fail unexpectedly | Check test environment matches production — model versions, API keys, data fixtures. |

## Examples
**Example**: `/compare-agent-validator "strict vs lenient" precision`
