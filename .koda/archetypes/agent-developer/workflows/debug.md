---
description: Debug agent failures including loop issues, tool errors, state corruption, and performance problems (Agent Developer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Environment Setup

// turbo
Verify debugging tools and LangSmith access.
Run the cross-platform environment validation utility for `agent-developer` in JSON mode and halt if `ENV_VALID` is false.

### 2. Load Configuration

- Read `agent-developer-constitution.md` for expected patterns

### 3. Parse Input

Extract from $ARGUMENTS:
- **Issue type**: infinite_loop | tool_error | state_corruption | timeout | unexpected_output
- **Agent path**: Path to agent code
- **Error messages**: Relevant logs or stack traces
- **Reproduction steps**: How to reproduce the issue

### 4. Diagnose Issue

**Infinite Loop:**
- Check iteration limits in edges.py
- Verify should_continue logic
- Check for missing END conditions

**Tool Errors:**
- Validate tool input schemas
- Check error handling in tools
- Verify timeout configuration

**State Corruption:**
- Check state schema typing
- Verify add_messages annotation
- Check for race conditions in async code

**Timeout:**
- Check MAX_ITERATIONS setting
- Review tool timeout configurations
- Check for blocking I/O

### 5. Generate Fix

Provide targeted fix with explanation.

### 6. Add Regression Test

Create test case to prevent recurrence.

### 7. Validate Fix

// turbo
Run tests and verify issue is resolved.
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

**Example 1**: `/debug-agent-developer infinite_loop ./my-agent "Agent stuck after 10 iterations"`
**Example 2**: `/debug-agent-developer tool_error ./support-bot "Search tool timeout"`

## References

Constitution: `agent-developer-constitution.md`
