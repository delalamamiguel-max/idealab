"""Example: External API integration tool with retry and rate limiting."""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from langchain_core.tools import tool
import httpx
import asyncio
import logging
from collections import defaultdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Rate limiting state
rate_limits = defaultdict(list)


class APIInput(BaseModel):
    """Input schema for external API call."""
    endpoint: HttpUrl = Field(
        description="Full URL of the API endpoint to call"
    )
    method: str = Field(
        default="GET",
        description="HTTP method (GET, POST, PUT, DELETE)",
        pattern="^(GET|POST|PUT|DELETE)$"
    )
    params: Optional[dict[str, str]] = Field(
        default=None,
        description="Query parameters as key-value pairs"
    )
    user_id: str = Field(
        description="User ID for rate limiting"
    )


class APIOutput(BaseModel):
    """Output schema for API response."""
    status_code: int
    data: dict
    response_time_ms: float


class ToolError(BaseModel):
    """Structured error response."""
    code: str
    message: str
    retryable: bool = False
    details: Optional[dict] = None


def check_rate_limit(user_id: str, max_calls: int = 100, window_minutes: int = 60) -> bool:
    """Check if user has exceeded rate limit."""
    now = datetime.now()
    cutoff = now - timedelta(minutes=window_minutes)
    
    # Remove old timestamps
    rate_limits[user_id] = [ts for ts in rate_limits[user_id] if ts > cutoff]
    
    if len(rate_limits[user_id]) >= max_calls:
        return False
    
    rate_limits[user_id].append(now)
    return True


@tool(args_schema=APIInput)
async def call_external_api(
    endpoint: str,
    method: str = "GET",
    params: Optional[dict] = None,
    user_id: str = "default"
) -> str:
    """Call external API with timeout, retry, and rate limiting.
    
    Implements exponential backoff for retries on transient failures.
    
    Side effects: May modify external system state (POST/PUT/DELETE)
    Idempotent: Only for GET requests
    Rate limit: 100 calls per hour per user
    """
    start_time = asyncio.get_event_loop().time()
    
    try:
        # Validate input
        validated = APIInput(
            endpoint=endpoint,
            method=method,
            params=params,
            user_id=user_id
        )
        
        # Check rate limit
        if not check_rate_limit(validated.user_id):
            return ToolError(
                code="RATE_LIMIT_EXCEEDED",
                message="Rate limit exceeded: 100 calls per hour",
                retryable=True,
                details={"retry_after_minutes": 60}
            ).model_dump_json()
        
        # Retry logic with exponential backoff
        max_retries = 3
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.request(
                        method=validated.method,
                        url=str(validated.endpoint),
                        params=validated.params or {}
                    )
                    response.raise_for_status()
                    
                    execution_time = (asyncio.get_event_loop().time() - start_time) * 1000
                    
                    output = APIOutput(
                        status_code=response.status_code,
                        data=response.json(),
                        response_time_ms=execution_time
                    )
                    
                    logger.info(f"API call successful: {validated.method} {validated.endpoint} ({execution_time:.2f}ms)")
                    return output.model_dump_json()
                    
            except httpx.TimeoutException:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"API timeout, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                else:
                    return ToolError(
                        code="TIMEOUT",
                        message=f"API call timed out after {max_retries} attempts",
                        retryable=True
                    ).model_dump_json()
                    
            except httpx.HTTPStatusError as e:
                # Don't retry on client errors (4xx)
                if 400 <= e.response.status_code < 500:
                    return ToolError(
                        code="CLIENT_ERROR",
                        message=f"Client error: {e.response.status_code}",
                        retryable=False,
                        details={"status_code": e.response.status_code}
                    ).model_dump_json()
                # Retry on server errors (5xx)
                elif attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Server error {e.response.status_code}, retrying in {wait_time}s")
                    await asyncio.sleep(wait_time)
                else:
                    return ToolError(
                        code="SERVER_ERROR",
                        message=f"Server error: {e.response.status_code}",
                        retryable=True
                    ).model_dump_json()
                    
            except httpx.NetworkError as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Network error, retrying in {wait_time}s")
                    await asyncio.sleep(wait_time)
                else:
                    return ToolError(
                        code="NETWORK_ERROR",
                        message="Network error after multiple retries",
                        retryable=True
                    ).model_dump_json()
        
    except Exception as e:
        logger.error(f"Unexpected error in API call: {e}")
        return ToolError(
            code="INTERNAL_ERROR",
            message="Unexpected error occurred"
        ).model_dump_json()
