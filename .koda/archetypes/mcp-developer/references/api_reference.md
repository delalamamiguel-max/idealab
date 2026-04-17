# MCP Developer API Reference

## Core MCP Protocol Patterns

### Tool Registration
```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

@tool(args_schema=InputSchema)
async def my_tool(param: str) -> str:
    """Tool description for LLM."""
    pass
```

### Schema Definition Best Practices
```python
class ToolInput(BaseModel):
    """Always include class docstring."""
    param: str = Field(
        description="Clear description for LLM understanding",
        min_length=1,
        max_length=1000
    )
```

### Error Response Pattern
```python
class ToolError(BaseModel):
    code: str  # VALIDATION_ERROR, TIMEOUT, PERMISSION_DENIED, INTERNAL_ERROR
    message: str
    retryable: bool = False
    details: Optional[dict] = None
```

## Common Tool Patterns

### Read-Only Query Tool
```python
@tool(args_schema=QueryInput)
async def query_data(query: str, limit: int = 10) -> str:
    """Query data source. Read-only, idempotent."""
    try:
        results = await db.execute(query, limit=limit)
        return QueryOutput(results=results).model_dump_json()
    except Exception as e:
        return ToolError(code="QUERY_ERROR", message=str(e)).model_dump_json()
```

### Write Operation Tool
```python
@tool(args_schema=WriteInput)
async def write_data(data: dict) -> str:
    """Write data. Side effect: creates record. NOT idempotent."""
    try:
        record_id = await db.insert(data)
        return WriteOutput(id=record_id, status="created").model_dump_json()
    except Exception as e:
        return ToolError(code="WRITE_ERROR", message=str(e)).model_dump_json()
```

### External API Integration Tool
```python
@tool(args_schema=APIInput)
async def call_external_api(endpoint: str, params: dict) -> str:
    """Call external API with timeout and retry."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()
            return APIOutput(data=response.json()).model_dump_json()
    except httpx.TimeoutException:
        return ToolError(code="TIMEOUT", message="API timeout", retryable=True).model_dump_json()
    except httpx.HTTPStatusError as e:
        return ToolError(code="HTTP_ERROR", message=f"Status {e.response.status_code}").model_dump_json()
```

## Field Validation Patterns

### String Constraints
```python
name: str = Field(description="User name", min_length=1, max_length=100, pattern=r"^[a-zA-Z\s]+$")
```

### Numeric Constraints
```python
count: int = Field(description="Result count", ge=1, le=100, default=10)
price: float = Field(description="Price in USD", gt=0, le=1000000)
```

### Enum Constraints
```python
from enum import Enum

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    
status: Status = Field(description="Record status")
```

### List Constraints
```python
tags: list[str] = Field(description="Tags", min_items=1, max_items=10)
```

## Security Patterns

### Input Sanitization
```python
def sanitize_input(value: str) -> str:
    """Remove potentially dangerous characters."""
    # Remove SQL injection patterns
    value = value.replace("'", "").replace(";", "").replace("--", "")
    # Remove command injection patterns
    value = value.replace("|", "").replace("&", "").replace("`", "")
    return value
```

### Output Filtering
```python
def filter_sensitive_data(data: dict) -> dict:
    """Remove sensitive fields from response."""
    sensitive_keys = ["password", "api_key", "secret", "token", "ssn"]
    return {k: v for k, v in data.items() if k.lower() not in sensitive_keys}
```

### Rate Limiting
```python
from collections import defaultdict
from datetime import datetime, timedelta

rate_limits = defaultdict(list)

def check_rate_limit(user_id: str, max_calls: int = 100, window_minutes: int = 60) -> bool:
    """Check if user exceeded rate limit."""
    now = datetime.now()
    cutoff = now - timedelta(minutes=window_minutes)
    
    # Remove old timestamps
    rate_limits[user_id] = [ts for ts in rate_limits[user_id] if ts > cutoff]
    
    if len(rate_limits[user_id]) >= max_calls:
        return False
    
    rate_limits[user_id].append(now)
    return True
```

## Testing Patterns

### Schema Validation Test
```python
def test_input_schema_validation():
    """Test input schema catches invalid data."""
    with pytest.raises(ValidationError):
        ToolInput(param="")  # Should fail min_length
```

### Tool Correctness Test
```python
@pytest.mark.asyncio
async def test_tool_correct_output():
    """Test tool produces expected output."""
    result = await my_tool(param="test")
    output = json.loads(result)
    assert "results" in output
    assert len(output["results"]) > 0
```

### Error Handling Test
```python
@pytest.mark.asyncio
async def test_tool_handles_timeout():
    """Test tool returns ToolError on timeout."""
    with patch('httpx.AsyncClient.get', side_effect=asyncio.TimeoutError):
        result = await my_tool(param="test")
        error = json.loads(result)
        assert error["code"] == "TIMEOUT"
        assert error["retryable"] is True
```
