"""
Example State Schema
Archetype: state-specialist
"""

from typing import TypedDict, Annotated
from operator import add


class ConversationState(TypedDict):
    """State schema for conversation agent."""
    
    # Message history (append-only)
    messages: Annotated[list[dict], add]
    
    # User context
    user_id: str
    session_id: str
    
    # Conversation metadata
    turn_count: int
    total_tokens: int
    
    # Agent state
    current_intent: str
    pending_actions: list[str]
    
    # Memory
    facts_extracted: Annotated[list[str], add]
    entities_mentioned: dict[str, list[str]]


def validate_state_bounds(state: ConversationState) -> bool:
    """Validate state is within bounds."""
    checks = [
        len(state["messages"]) <= 100,  # Max 100 messages
        state["total_tokens"] <= 100000,  # Max 100k tokens
        len(state["facts_extracted"]) <= 50,  # Max 50 facts
    ]
    return all(checks)
