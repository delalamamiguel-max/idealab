"""
Example Output Guardrail Implementation
Archetype: guardrails-engineer
"""

from agent_development.common import BaseOutputGuardrail, GuardrailResult, GuardrailAction
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase


class HallucinationGuardrail(BaseOutputGuardrail):
    """Detect hallucinations in agent output."""
    
    def __init__(self, threshold: float = 0.95):
        super().__init__(
            name="hallucination",
            threshold=threshold,
            action=GuardrailAction.BLOCK,
        )
        self.metric = HallucinationMetric(threshold=threshold)
    
    async def evaluate(self, content: str, context: list[str] = None, **kwargs) -> GuardrailResult:
        """Check output against provided context."""
        if not context:
            return self._create_result(
                passed=True,
                confidence=0.5,
                details="No context provided, skipping hallucination check",
            )
        
        test_case = LLMTestCase(
            input="",
            actual_output=content,
            context=context,
        )
        
        self.metric.measure(test_case)
        
        return self._create_result(
            passed=self.metric.score >= self.threshold,
            confidence=self.metric.score,
            details=self.metric.reason,
        )
