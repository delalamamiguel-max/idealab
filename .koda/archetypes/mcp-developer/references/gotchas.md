# MCP Developer Gotchas Reference

This file consolidates common failure patterns and solutions for MCP tool development.

## Tool Schema Issues

### Missing Field Descriptions
**Problem:** LLM passes incorrect arguments or misunderstands tool purpose  
**Detection:** Agent logs show wrong parameter values, unexpected tool behavior  
**Fix:** Add `description` to every Field. Include examples in docstrings.

```python
# ❌ Bad
class Input(BaseModel):
    query: str
    limit: int

# ✅ Good
class Input(BaseModel):
    query: str = Field(description="Search query string, e.g., 'python async patterns'")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum results to return")
```

### Ambiguous Type Annotations
**Problem:** Tool receives unexpected data types  
**Detection:** Runtime type errors, Pydantic validation failures  
**Fix:** Use specific types, not `Any`. Use Union for multiple valid types.

```python
# ❌ Bad
data: Any

# ✅ Good
data: dict[str, str | int]
```

## Error Handling Issues

### Unhandled Timeout Errors
**Problem:** Tool hangs indefinitely, agent becomes stuck  
**Detection:** Tool never returns, agent timeout  
**Fix:** Wrap all I/O with timeout, return ToolError with retryable=True

```python
# ❌ Bad
async def my_tool(url: str) -> str:
    response = await httpx.get(url)  # No timeout!
    return response.text

# ✅ Good
async def my_tool(url: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            return response.text
    except httpx.TimeoutException:
        return ToolError(code="TIMEOUT", message="Request timed out", retryable=True).model_dump_json()
```

### Credential Exposure in Error Messages
**Problem:** API keys or tokens appear in tool error responses  
**Detection:** Security scan flags exposed credentials in logs  
**Fix:** Sanitize all error messages, never include raw exception details

```python
# ❌ Bad
except Exception as e:
    return ToolError(code="ERROR", message=str(e)).model_dump_json()  # May contain credentials!

# ✅ Good
except Exception as e:
    safe_message = "External API call failed"
    logger.error(f"Tool error: {e}")  # Log full error securely
    return ToolError(code="API_ERROR", message=safe_message).model_dump_json()
```

## Side Effects and Idempotency

### Undocumented Side Effects
**Problem:** Agent repeatedly calls tool expecting different results  
**Detection:** Multiple identical tool calls, unexpected state changes  
**Fix:** Document all side effects in docstring, mark idempotent tools

```python
# ❌ Bad
@tool
async def process_data(data: str) -> str:
    """Process data."""  # Doesn't mention it writes to database!
    await db.insert(data)
    return "processed"

# ✅ Good
@tool
async def process_data(data: str) -> str:
    """Process data and store in database.
    
    Side effects:
    - Creates new record in database
    - NOT idempotent - multiple calls create multiple records
    - Requires write permissions
    """
    await db.insert(data)
    return "processed"
```

### Non-Idempotent Operations
**Problem:** Duplicate records, inconsistent state from retries  
**Detection:** Database contains duplicate entries  
**Fix:** Implement idempotency keys or check-before-write

```python
# ❌ Bad
async def create_user(email: str) -> str:
    user_id = await db.insert({"email": email})
    return user_id

# ✅ Good
async def create_user(email: str) -> str:
    existing = await db.find_one({"email": email})
    if existing:
        return existing["id"]  # Idempotent
    user_id = await db.insert({"email": email})
    return user_id
```

## Validation Issues

### Schema Validation Bypass
**Problem:** Tool receives invalid data, crashes with cryptic errors  
**Detection:** Runtime errors deep in tool logic  
**Fix:** Always instantiate input schema class, let Pydantic validate

```python
# ❌ Bad
@tool
async def my_tool(param: str, count: int) -> str:
    # Directly uses params without validation
    results = await fetch_data(param, count)
    return results

# ✅ Good
@tool(args_schema=MyToolInput)
async def my_tool(param: str, count: int) -> str:
    # Pydantic validates before function runs
    validated = MyToolInput(param=param, count=count)
    results = await fetch_data(validated.param, validated.count)
    return results
```

### Missing Boundary Validation
**Problem:** Tool accepts extreme values causing performance issues  
**Detection:** Slow queries, memory errors, timeouts  
**Fix:** Add ge/le/gt/lt constraints to numeric fields

```python
# ❌ Bad
limit: int = Field(description="Result limit")

# ✅ Good
limit: int = Field(description="Result limit", ge=1, le=1000, default=10)
```

## Async/Await Issues

### Blocking I/O in Async Tools
**Problem:** Tool blocks event loop, poor concurrency  
**Detection:** Other async operations stall when tool runs  
**Fix:** Use async libraries or wrap sync calls with to_thread

```python
# ❌ Bad
@tool
async def read_file(path: str) -> str:
    with open(path) as f:  # Blocking I/O!
        return f.read()

# ✅ Good
@tool
async def read_file(path: str) -> str:
    async with aiofiles.open(path) as f:
        return await f.read()
```

### Missing Await
**Problem:** Tool returns coroutine object instead of result  
**Detection:** Result is `<coroutine object>` string  
**Fix:** Always await async calls

```python
# ❌ Bad
result = fetch_data()  # Missing await!

# ✅ Good
result = await fetch_data()
```

## Security Issues

### SQL Injection Vulnerability
**Problem:** User input directly interpolated into SQL  
**Detection:** Security scan, penetration testing  
**Fix:** Use parameterized queries

```python
# ❌ Bad
query = f"SELECT * FROM users WHERE email = '{email}'"
await db.execute(query)

# ✅ Good
query = "SELECT * FROM users WHERE email = ?"
await db.execute(query, (email,))
```

### Command Injection Vulnerability
**Problem:** User input passed to shell commands  
**Detection:** Security scan, code review  
**Fix:** Never use shell=True, validate and sanitize inputs

```python
# ❌ Bad
import subprocess
subprocess.run(f"ls {user_path}", shell=True)

# ✅ Good
import subprocess
subprocess.run(["ls", user_path], shell=False)
```

## Testing Gaps

### Missing Error Path Tests
**Problem:** Error handling code never tested, fails in production  
**Detection:** Production errors in error handling logic  
**Fix:** Test all error paths explicitly

```python
@pytest.mark.asyncio
async def test_tool_handles_network_error():
    """Test tool handles network failures gracefully."""
    with patch('httpx.AsyncClient.get', side_effect=httpx.NetworkError):
        result = await my_tool(url="http://example.com")
        error = json.loads(result)
        assert error["code"] == "NETWORK_ERROR"
        assert "retryable" in error
```

### Missing Integration Tests
**Problem:** Tool works in isolation but fails when called by agent  
**Detection:** Agent can't use tool, integration failures  
**Fix:** Test tool with actual LangChain agent invocation

```python
@pytest.mark.asyncio
async def test_tool_with_agent():
    """Test tool works when invoked by agent."""
    from langchain.agents import AgentExecutor
    
    agent = create_agent(tools=[my_tool])
    result = await agent.ainvoke({"input": "use my_tool to fetch data"})
    assert "error" not in result["output"].lower()
```
