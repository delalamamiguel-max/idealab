---
description: Generate comprehensive test suite for agents including unit, integration, and golden tests (Agent Developer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Environment Setup

// turbo
Verify pytest and testing dependencies.
Run the cross-platform environment validation utility for `agent-developer` in JSON mode and halt if `ENV_VALID` is false.

### 2. Load Configuration

- Read `agent-developer-constitution.md` for test requirements

### 3. Parse Input

Extract from $ARGUMENTS:
- **Agent path**: Path to agent code
- **Test scope**: unit | integration | golden | all
- **Coverage target**: Minimum coverage percentage

### 4. Generate Test Suite

**Unit Tests:**
- Test each node function in isolation
- Mock external dependencies
- Test error handling paths

**Integration Tests:**
- Test full graph execution
- Test with mock tools
- Test state transitions

**Golden Tests:**
- Create expected input/output pairs
- Test for regression

**Edge Case Tests:**
- Test iteration limits
- Test timeout handling
- Test invalid inputs

### 5. Run Tests

// turbo
```bash
pytest tests/ -v --cov=graph --cov-report=html
```

### 6. Generate Coverage Report

Report test coverage and identify gaps.
Run the cross-platform guardrails validation utility against `output/` in JSON mode for `agent-developer`.

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user for required arguments. |
| `agent-developer-constitution.md` not found | Stop. Ensure repo is at root with constitution file present. |
| Environment validation utility unavailable | Manually verify Python ≥3.10, langgraph, langchain-openai are installed. |
| Tool import fails | Check `available_libraries` in `templates/env-config.yaml` and install missing packages. |
| LLM API key missing | Set `OPENAI_API_KEY` environment variable before running. |

## Examples

**Example 1**: `/test-agent-developer ./my-agent all coverage=80`
**Example 2**: `/test-agent-developer ./support-bot golden`

## References

Constitution: `agent-developer-constitution.md`
