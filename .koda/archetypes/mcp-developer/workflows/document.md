---
description: Generate documentation for MCP tools including schemas, examples, and integration guides (MCP Developer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Tool path**: Path to tool
- **Doc type**: full | api | integration

### 2. Generate Documentation

**API Reference:**
- Input schema
- Output schema
- Error codes

**Integration Guide:**
- How to use with agents
- Example invocations

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
**Example**: `/document-mcp-developer tools/search.py full`
