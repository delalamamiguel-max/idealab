---
description: Refactor existing MCP tools for better validation, error handling, and performance (MCP Developer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Tool path**: Path to existing tool
- **Goal**: validation | error_handling | performance | security

### 2. Analyze Current Tool
- Check schema completeness
- Review error handling
- Assess security boundaries
- Measure performance

### 3. Apply Refactorings
- Add missing schema fields
- Improve error responses
- Add rate limiting
- Enhance logging

### 4. Validate
- Run existing tests
- Verify backward compatibility

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
**Example**: `/refactor-mcp-developer tools/search.py security`
