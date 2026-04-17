---
description: Improve existing validation tests for better coverage and accuracy (Agent Validator)
---

User input: $ARGUMENTS

## Execution Steps
1. Parse Input - validation suite path, goal
2. Analyze coverage gaps
3. Add missing test cases
4. Improve threshold calibration
5. Validate changes

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
**Example**: `/refactor-agent-validator tests/validation.py coverage`
