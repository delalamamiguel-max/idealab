"""
Example Input Guardrail Implementation
Archetype: guardrails-engineer
"""

from agent_development.common import BaseInputGuardrail, GuardrailResult, GuardrailAction


class PromptInjectionGuardrail(BaseInputGuardrail):
    """Detect and block prompt injection attempts."""
    
    def __init__(self, threshold: float = 0.8):
        super().__init__(
            name="prompt_injection",
            threshold=threshold,
            action=GuardrailAction.BLOCK,
        )
    
    async def evaluate(self, content: str, **kwargs) -> GuardrailResult:
        """Check for prompt injection patterns."""
        injection_patterns = [
            "ignore previous instructions",
            "disregard all",
            "forget everything",
            "system:",
            "assistant:",
            "new instructions:",
        ]
        
        content_lower = content.lower()
        matches = [p for p in injection_patterns if p in content_lower]
        
        if matches:
            confidence = min(1.0, len(matches) * 0.3)
            return self._create_result(
                passed=False,
                confidence=confidence,
                details=f"Detected injection patterns: {matches}",
            )
        
        return self._create_result(passed=True, confidence=1.0)
