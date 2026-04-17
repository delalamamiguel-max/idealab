---
description: Refactor existing agents to apply security, performance, and architectural best practices (Agent Developer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Environment Setup

// turbo
Verify LangGraph environment available.
Run the cross-platform environment validation utility for `agent-developer` in JSON mode and halt if `ENV_VALID` is false.

### 2. Load Configuration

- Read `agent-developer-constitution.md` for patterns
- Load existing agent code

### 3. Parse Input

Extract from $ARGUMENTS:
- **Agent path**: Path to existing agent code
- **Refactoring goal**: security | performance | architecture | observability | all
- **Target level**: Optional new maturity level

### 4. Analyze Current Implementation

- Check state schema typing
- Verify error handling in nodes
- Check iteration limits
- Assess tool validation
- Review checkpointing
- Check guardrails integration

### 5. Generate Refactoring Plan

Identify issues and prioritize fixes based on constitution rules.

### 6. Implement Refactorings

Apply changes with detailed changelog.

### 7. Validate and Report

// turbo
Run tests and validate against constitution.
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

**Example 1**: `/refactor-agent-developer ./my-agent security`
**Example 2**: `/refactor-agent-developer ./legacy-bot architecture L3`

## References

Constitution: `agent-developer-constitution.md`
