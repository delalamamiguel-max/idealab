---
description: Create validation test cases and quality gates for agents (Agent Validator)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Agent path**: Path to agent to validate
- **Validation type**: trajectory | adversarial | safety | regression | all
- **Gate thresholds**: Pass/fail thresholds

### 2. Generate Validation Suite

**Trajectory Tests:**
```python
def evaluate_trajectory(run, example):
    trajectory = run.outputs.get("intermediate_steps", [])
    return {
        "tool_selection": score_tool_selection(trajectory),
        "reasoning": score_reasoning(trajectory),
        "efficiency": len(example.optimal) / len(trajectory),
    }
```

**Adversarial Tests:**
- Prompt injection attempts
- Jailbreak attempts
- Edge cases

**Safety Tests:**
- PII handling
- Toxicity checks
- Bias detection

### 3. Generate CI/CD Gate

```yaml
quality_gate:
  task_completion: 0.8
  tool_correctness: 0.9
  safety_score: 0.95
  block_on_failure: true
```

### 4. Validate and Report

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
**Example**: `/scaffold-agent-validator ./my-agent all thresholds=strict`
