---
description: Fix validation failures, false positives, and gate configuration issues (Agent Validator)
---

User input: $ARGUMENTS

## Execution Steps
1. Parse Input - test path, issue type
2. Diagnose validation failure
3. Adjust thresholds or test logic
4. Add regression test
5. Validate fix

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
**Example**: `/debug-agent-validator tests/safety.py false_positive "Blocking valid requests"`
