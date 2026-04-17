---
description: Scaffold language model evaluation pipeline with custom graders and async Evaluator (Eval Specialist)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Eval name**: Name for the evaluation pipeline
- **Metrics**: List of metrics to include
- **SOX scope**: Whether SOX compliance required
- **Judge model**: Model to use for LLM-as-judge

### 2. Generate Evaluation Pipeline

```python
"""Evaluation pipeline for {eval_name}."""

import asyncio
from dataclasses import dataclass
from typing import Optional
from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    HallucinationMetric,
)
from deepeval.test_case import LLMTestCase

@dataclass
class EvaluationInput:
    """Standard input schema for evaluation."""
    response: str
    prompt: Optional[str] = None
    context: Optional[list[str]] = None
    expected: Optional[str] = None

@dataclass
class GradeResult:
    """Standard result schema for graders."""
    grader_name: str
    score: float
    passed: bool
    reasoning: Optional[str] = None
    metadata: dict = None

class Evaluator:
    """Async evaluator with multiple graders."""
    
    def __init__(self, graders: list, thresholds: dict):
        self.graders = graders
        self.thresholds = thresholds
    
    async def evaluate(self, input: EvaluationInput) -> list[GradeResult]:
        """Run all graders on input."""
        tasks = [self._run_grader(g, input) for g in self.graders]
        return await asyncio.gather(*tasks)
    
    async def _run_grader(self, grader, input) -> GradeResult:
        try:
            test_case = LLMTestCase(
                input=input.prompt or "",
                actual_output=input.response,
                retrieval_context=input.context,
            )
            grader.measure(test_case)
            threshold = self.thresholds.get(grader.__class__.__name__, 0.8)
            return GradeResult(
                grader_name=grader.__class__.__name__,
                score=grader.score,
                passed=grader.score >= threshold,
                reasoning=grader.reason,
            )
        except Exception as e:
            return GradeResult(
                grader_name=grader.__class__.__name__,
                score=0.0,
                passed=False,
                reasoning=f"Error: {str(e)}",
            )
```

### 3. Add Phoenix Integration (if SOX)

```python
from agent_development.common import setup_phoenix_tracing, log_sox_event

tracer = setup_phoenix_tracing("{eval_name}", sox_scope=True)

def log_evaluation(results: list[GradeResult]):
    log_sox_event("evaluation", {
        "scores": {r.grader_name: r.score for r in results},
        "passed": all(r.passed for r in results),
    })
```

### 4. Generate Test Suite

```python
"""Test suite for {eval_name} evaluation pipeline."""

import pytest
import asyncio
from evaluation_pipeline import Evaluator, EvaluationInput

@pytest.fixture
def evaluator():
    from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
    return Evaluator(
        graders=[FaithfulnessMetric(threshold=0.8), AnswerRelevancyMetric(threshold=0.8)],
        thresholds={"FaithfulnessMetric": 0.8, "AnswerRelevancyMetric": 0.8},
    )

@pytest.mark.asyncio
@pytest.mark.parametrize("response,context,expected_pass", [
    ("Paris is the capital of France.", ["France's capital is Paris."], True),
    ("The sky is green.", ["The sky is blue."], False),
])
async def test_evaluator_grades_correctly(evaluator, response, context, expected_pass):
    result = await evaluator.evaluate(
        EvaluationInput(response=response, context=context)
    )
    assert any(r.passed == expected_pass for r in result)

async def test_evaluator_handles_empty_context(evaluator):
    result = await evaluator.evaluate(EvaluationInput(response="test", context=[]))
    assert len(result) > 0  # should not crash
```

### 5. Validate

Run validation checks before declaring the pipeline production-ready:

```bash
# Run the generated test suite
pytest tests/test_{eval_name}.py -v

# Confirm all graders return scores (not errors)
# Confirm pass/fail threshold logic is correct
# Confirm async execution completes without deadlocks
```

**Checklist:**
- [ ] All graders produce numeric scores (0.0–1.0)
- [ ] Test suite has ≥3 test cases including at least 1 expected-fail case
- [ ] `evaluate()` handles empty context without crashing
- [ ] SOX logging fires correctly if `sox_scope=True` (check Phoenix endpoint receives events)
- [ ] Pipeline runs end-to-end in under 30 seconds for a 10-item batch

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide eval name, metrics list, and SOX scope flag. |
| `eval-specialist-constitution.md` not found | Stop. Ensure file is present at repo root. |
| `deepeval` not installed | Run `pip install deepeval`. Check `available_libraries` in `templates/env-config.yaml`. |
| Grader returns error instead of score | Inspect grader logs. Verify test case has required fields (prompt, context, expected). |
| SOX Phoenix endpoint unreachable | Check `PHOENIX_ENDPOINT` env var is set. Verify network access. |
| All tests fail | Verify LLM API key is set and the judge model is accessible. |

## Examples
**Example**: `/scaffold-eval-specialist rag-eval "faithfulness,relevancy" SOX=yes`
