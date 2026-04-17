"""
Example Model Configuration
Archetype: model-specialist
"""

from dataclasses import dataclass
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


@dataclass
class ModelConfig:
    """Model configuration."""
    provider: str
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 1000
    cost_per_1k_tokens: float = 0.0


# Model registry
MODEL_REGISTRY = {
    "gpt-4": ModelConfig("openai", "gpt-4", cost_per_1k_tokens=0.03),
    "gpt-3.5-turbo": ModelConfig("openai", "gpt-3.5-turbo", cost_per_1k_tokens=0.002),
    "claude-3-opus": ModelConfig("anthropic", "claude-3-opus-20240229", cost_per_1k_tokens=0.015),
    "claude-3-sonnet": ModelConfig("anthropic", "claude-3-sonnet-20240229", cost_per_1k_tokens=0.003),
}


class ModelRouter:
    """Route requests to appropriate model with fallback."""
    
    def __init__(self, primary: str, fallback: Optional[str] = None):
        self.primary_config = MODEL_REGISTRY[primary]
        self.fallback_config = MODEL_REGISTRY[fallback] if fallback else None
        self.total_cost = 0.0
    
    def get_model(self, use_fallback: bool = False):
        """Get model instance."""
        config = self.fallback_config if use_fallback and self.fallback_config else self.primary_config
        
        if config.provider == "openai":
            return ChatOpenAI(
                model=config.model_name,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
            )
        elif config.provider == "anthropic":
            return ChatAnthropic(
                model=config.model_name,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
            )
    
    def track_cost(self, tokens: int, use_fallback: bool = False):
        """Track token cost."""
        config = self.fallback_config if use_fallback and self.fallback_config else self.primary_config
        cost = (tokens / 1000) * config.cost_per_1k_tokens
        self.total_cost += cost
        return cost
