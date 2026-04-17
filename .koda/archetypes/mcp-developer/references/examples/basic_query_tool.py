"""Example: Basic read-only query tool with proper error handling."""

from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.tools import tool
import asyncio
import logging

logger = logging.getLogger(__name__)


class QueryInput(BaseModel):
    """Input schema for database query tool."""
    query: str = Field(
        description="SQL query to execute. Must be SELECT only (read-only).",
        min_length=1,
        max_length=5000
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=1000,
        description="Maximum number of results to return"
    )


class QueryOutput(BaseModel):
    """Output schema for query results."""
    results: list[dict]
    count: int
    execution_time_ms: float


class ToolError(BaseModel):
    """Structured error response."""
    code: str
    message: str
    retryable: bool = False
    details: Optional[dict] = None


@tool(args_schema=QueryInput)
async def query_database(query: str, limit: int = 10) -> str:
    """Execute read-only database query.
    
    Returns JSON with results array and metadata.
    
    Side effects: None (read-only)
    Idempotent: Yes
    """
    start_time = asyncio.get_event_loop().time()
    
    try:
        # Validate input
        validated = QueryInput(query=query, limit=limit)
        
        # Security check: ensure read-only
        if not validated.query.strip().upper().startswith("SELECT"):
            return ToolError(
                code="VALIDATION_ERROR",
                message="Only SELECT queries allowed (read-only tool)"
            ).model_dump_json()
        
        # Execute query with timeout
        async with asyncio.timeout(30.0):
            # Simulated database call
            results = await _execute_query(validated.query, validated.limit)
        
        execution_time = (asyncio.get_event_loop().time() - start_time) * 1000
        
        output = QueryOutput(
            results=results,
            count=len(results),
            execution_time_ms=execution_time
        )
        
        logger.info(f"Query executed successfully: {len(results)} results in {execution_time:.2f}ms")
        return output.model_dump_json()
        
    except asyncio.TimeoutError:
        return ToolError(
            code="TIMEOUT",
            message="Query execution timed out after 30 seconds",
            retryable=True
        ).model_dump_json()
        
    except ValueError as e:
        return ToolError(
            code="VALIDATION_ERROR",
            message=f"Invalid query: {str(e)}"
        ).model_dump_json()
        
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        return ToolError(
            code="INTERNAL_ERROR",
            message="Database query failed"
        ).model_dump_json()


async def _execute_query(query: str, limit: int) -> list[dict]:
    """Internal query execution (simulated)."""
    # In real implementation, this would call actual database
    await asyncio.sleep(0.1)  # Simulate I/O
    return [
        {"id": 1, "name": "Example 1"},
        {"id": 2, "name": "Example 2"}
    ][:limit]
