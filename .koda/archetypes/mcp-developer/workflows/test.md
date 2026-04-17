---
description: Test MCP tools for correctness, error handling, and performance (MCP Developer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Tool path**: Path to tool
- **Test scope**: unit | integration | correctness | all

### 2. Generate/Run Tests

**Unit Tests:**
- Schema validation
- Error handling paths
- Edge cases

**Integration Tests:**
- Tool with agent invocation
- End-to-end flow

**Correctness Tests (ToolCorrectnessMetric):**
- Correct outputs for known inputs
- Argument validation

### 3. Generate Report

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide tool name, input schema, and output schema. |
| `mcp-developer-constitution.md` not found | Stop. Ensure file is present at repo root. |
| `pydantic` not installed | Run `pip install pydantic>=2.0`. |
| Tool raises raw exception exposing credentials | NEVER propagate `str(e)` to users. Log internally and raise a sanitised `RuntimeError`. |
| Schema validation fails at runtime | Verify input matches Pydantic model. Return structured error with field name and constraint violated. |
| Async tool hangs | Verify `timeout_seconds` is set in tool config. Add `asyncio.wait_for()` wrapper. |

## Examples
**Example**: `/test-mcp-developer tools/search.py all`
