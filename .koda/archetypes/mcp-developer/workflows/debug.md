---
description: Debug MCP tool errors including validation failures, timeouts, and incorrect outputs (MCP Developer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Tool path**: Path to tool
- **Issue type**: validation | timeout | wrong_output | crash
- **Error message**: The error encountered

### 2. Diagnose
- Review error logs
- Check input validation
- Test with sample inputs
- Verify dependencies

### 3. Fix Issue
- Correct schema definitions
- Add missing error handling
- Fix timeout configuration
- Update validation logic

### 4. Add Regression Test

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
**Example**: `/debug-mcp-developer tools/search.py timeout "Tool takes >30s"`
