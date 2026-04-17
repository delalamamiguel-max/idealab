"""
Example Output Schema
Archetype: output-spec-specialist
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class CustomerIntent(BaseModel):
    """Structured output for intent classification."""
    
    intent: Literal["question", "complaint", "request", "feedback"] = Field(
        description="Primary customer intent"
    )
    
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score"
    )
    
    entities: dict[str, str] = Field(
        default_factory=dict,
        description="Extracted entities"
    )
    
    requires_escalation: bool = Field(
        description="Whether to escalate to human"
    )
    
    reasoning: str = Field(
        description="Explanation of classification"
    )
    
    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Ensure confidence is in valid range."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confidence must be between 0 and 1")
        return v


# Example usage with retry
def parse_with_retry(llm_output: str, max_retries: int = 3) -> CustomerIntent:
    """Parse LLM output with retry logic."""
    for attempt in range(max_retries):
        try:
            return CustomerIntent.model_validate_json(llm_output)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            # Could add repair logic here
    raise ValueError("Failed to parse output")
