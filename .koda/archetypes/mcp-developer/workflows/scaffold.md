---
description: Build MCP tool servers with schema validation, error handling, and security boundaries (MCP Developer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Environment Setup

// turbo
Verify MCP development environment:
- Python 3.10+
- pydantic, fastapi

### 2. Load Configuration

- Read `mcp-developer-constitution.md` for hard-stop rules

### 3. Parse Input

Extract from $ARGUMENTS:
- **Tool name**: Name for the tool
- **Purpose**: What the tool does
- **Input params**: Input parameters with types
- **Output type**: Return type
- **Side effects**: Any side effects (read-only, write, external-api)

If incomplete, request:
```
Please provide:
1. Tool Name: (e.g., "search_documents")
2. Purpose: (what does this tool do?)
3. Input Parameters: (e.g., "query: str, limit: int = 10")
4. Output Type: (e.g., "list[Document]")
5. Side Effects: read-only | write | external-api
```

### 4. Generate Tool Schema

```python
"""Tool: {tool_name}"""

from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.tools import tool
import logging

logger = logging.getLogger(__name__)

class {ToolName}Input(BaseModel):
    """{tool_name} input schema."""
    {param1}: {type1} = Field(description="{description}")
    {param2}: {type2} = Field(default={default}, description="{description}")

class {ToolName}Output(BaseModel):
    """{tool_name} output schema."""
    result: {output_type}
    metadata: Optional[dict] = None

class ToolError(BaseModel):
    """Structured error response."""
    code: str
    message: str
    retryable: bool = False

@tool(args_schema={ToolName}Input)
async def {tool_name}({params}) -> str:
    """{purpose}"""
    try:
        logger.info(f"Executing {tool_name} with {params}")
        
        # Validate inputs
        validated = {ToolName}Input({params})
        
        # Execute tool logic
        result = await _execute_{tool_name}(validated)
        
        # Return structured output
        return {ToolName}Output(result=result).model_dump_json()
        
    except ValidationError as e:
        return ToolError(code="VALIDATION_ERROR", message=str(e)).model_dump_json()
    except TimeoutError:
        return ToolError(code="TIMEOUT", message="Operation timed out", retryable=True).model_dump_json()
    except Exception as e:
        logger.error(f"Tool error: {e}")
        return ToolError(code="INTERNAL_ERROR", message=str(e)).model_dump_json()

async def _execute_{tool_name}(input: {ToolName}Input) -> {output_type}:
    """Internal implementation."""
    # TODO: Implement tool logic
    pass
```

### 5. Generate Tests

```python
"""Tests for {tool_name}."""

import pytest
from tools.{tool_name} import {tool_name}, {ToolName}Input

@pytest.mark.asyncio
async def test_{tool_name}_valid_input():
    """Test tool with valid input."""
    result = await {tool_name}({valid_params})
    assert "error" not in result.lower()

@pytest.mark.asyncio
async def test_{tool_name}_invalid_input():
    """Test tool handles invalid input."""
    result = await {tool_name}({invalid_params})
    assert "VALIDATION_ERROR" in result

@pytest.mark.asyncio
async def test_{tool_name}_timeout():
    """Test tool handles timeout."""
    # Mock timeout scenario
    pass
```

### 6. Validate and Report

// turbo
- [ ] Input schema defined with Pydantic
- [ ] Output schema defined
- [ ] Error handling implemented
- [ ] Logging added
- [ ] Tests created

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

**Example 1**: `/scaffold-mcp-developer search_docs "Search documents" "query: str, limit: int" "list[str]" read-only`

**Example 2**: `/scaffold-mcp-developer send_email "Send email notification" "to: str, subject: str, body: str" "bool" external-api`
