"""
Example MCP Tool Implementation
Archetype: mcp-developer
"""

import logging
from pydantic import BaseModel, Field
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


class SearchInput(BaseModel):
    """Input schema for search tool."""
    query: str = Field(description="Search query", min_length=1, max_length=500)
    max_results: int = Field(default=5, ge=1, le=50, description="Maximum results")


class SearchOutput(BaseModel):
    """Output schema for search tool."""
    results: list[str]
    count: int


@tool
async def search_tool(query: str, max_results: int = 5) -> dict:
    """
    Search for information.

    Args:
        query: Search query (1–500 chars)
        max_results: Maximum number of results (1–50)

    Returns:
        Validated SearchOutput dict
    """
    # Validate inputs via Pydantic before execution
    validated = SearchInput(query=query, max_results=max_results)

    try:
        # Replace with real search implementation
        results = [f"Result {i} for '{validated.query}'" for i in range(validated.max_results)]
        output = SearchOutput(results=results, count=len(results))
        return output.model_dump()
    except Exception as e:
        # NEVER expose raw exception — it may contain credentials or sensitive data
        logger.error("search_tool execution failed: %s", e)
        raise RuntimeError("Search execution failed. Check server logs for details.") from None


# Inline validation tests (no external dependency required)
def _run_tests() -> None:
    import asyncio

    async def _test():
        result = await search_tool.ainvoke({"query": "test", "max_results": 3})
        assert result["count"] == 3, f"Expected count=3, got {result['count']}"
        print("search_tool test PASSED")

    asyncio.run(_test())


if __name__ == "__main__":
    _run_tests()
