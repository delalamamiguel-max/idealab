---
description: Create output schemas with Pydantic models and structured output patterns (Output Spec Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Schema name**: Name for the output schema
- **Fields**: Field definitions with types
- **Purpose**: What data this captures
- **Integration**: How it integrates with LLM

### 2. Generate Pydantic Schema

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class {SchemaName}(BaseModel):
    """{purpose}"""
    
    {field1}: {type1} = Field(description="{desc}")
    {field2}: Optional[{type2}] = Field(default=None, description="{desc}")
    
    class Config:
        json_schema_extra = {
            "examples": [{example}]
        }
```

### 3. Generate LLM Integration

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4").with_structured_output({SchemaName})
result = model.invoke(prompt)
```

### 4. Generate Tests

### 5. Validate

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide output name, target format (JSON/Pydantic), and validation mode (strict/lenient). |
| `output-spec-specialist-constitution.md` not found | Stop. Ensure file is present at repo root. |
| `pydantic` not installed | Run `pip install pydantic>=2.0`. |
| Schema validation rejects valid output | Review field constraints — check `min_length`, `pattern`, and required fields against actual agent output format. |
| JSON parse fails on agent output | Agent is not returning valid JSON. Add output parser with retry logic using LangChain's `OutputFixingParser`. |
| Schema registry URL unreachable | Set `SCHEMA_REGISTRY_URL` env var or operate in local-only mode (remove registry push steps). |

## Examples
**Example**: `/scaffold-output-spec-specialist ExtractedEntity "name: str, type: str, confidence: float"`
