---
description: Validate the validation suite itself for accuracy and completeness (Agent Validator)
---

User input: $ARGUMENTS

## Execution Steps
1. Parse Input - validation suite path
2. Run meta-validation
3. Check false positive/negative rates
4. Verify gate accuracy
5. Generate report

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
**Example**: `/test-agent-validator tests/validation.py`
