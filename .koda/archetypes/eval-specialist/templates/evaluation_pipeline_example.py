"""
Example Evaluation Pipeline
Archetype: eval-specialist
"""

import asyncio
from dataclasses import dataclass
from typing import Optional
from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    HallucinationMetric,
)
from deepeval.test_case import LLMTestCase
from agent_development.common import log_sox_event


@dataclass
class EvaluationInput:
    """Standard input schema."""
    response: str
    prompt: Optional[str] = None
    context: Optional[list[str]] = None
    expected: Optional[str] = None


@dataclass
class GradeResult:
    """Standard result schema."""
    grader_name: str
    score: float
    passed: bool
    reasoning: Optional[str] = None


class Evaluator:
    """Async evaluator with multiple graders."""
    
    def __init__(self, sox_scope: bool = False):
        self.sox_scope = sox_scope
        self.graders = [
            FaithfulnessMetric(threshold=0.9),
            AnswerRelevancyMetric(threshold=0.8),
            HallucinationMetric(threshold=0.95),
        ]
    
    async def evaluate(self, input: EvaluationInput) -> list[GradeResult]:
        """Run all graders."""
        tasks = [self._run_grader(g, input) for g in self.graders]
        results = await asyncio.gather(*tasks)
        
        if self.sox_scope:
            log_sox_event("evaluation", {
                "scores": {r.grader_name: r.score for r in results},
                "passed": all(r.passed for r in results),
            })
        
        return results
    
    async def _run_grader(self, grader, input: EvaluationInput) -> GradeResult:
        """Run single grader."""
        try:
            test_case = LLMTestCase(
                input=input.prompt or "",
                actual_output=input.response,
                retrieval_context=input.context,
            )
            grader.measure(test_case)
            return GradeResult(
                grader_name=grader.__class__.__name__,
                score=grader.score,
                passed=grader.score >= grader.threshold,
                reasoning=grader.reason,
            )
        except Exception as e:
            return GradeResult(
                grader_name=grader.__class__.__name__,
                score=0.0,
                passed=False,
                reasoning=f"Error: {str(e)}",
            )
