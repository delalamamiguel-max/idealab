---
description: Compare MCP tool implementations for performance, correctness, and maintainability (MCP Developer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Tools**: Tools to compare
- **Criteria**: performance | correctness | maintainability

### 2. Run Comparison

| Tool | Latency | Correctness | Error Rate |
|------|---------|-------------|------------|
| A | {ms} | {score} | {rate} |
| B | {ms} | {score} | {rate} |

### 3. Recommend

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
**Example**: `/compare-mcp-developer "search_v1 vs search_v2" performance`
