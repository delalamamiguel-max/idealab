"""
Language Model Evaluation Grader Library

This module provides example implementations of heuristic and LLM judge graders
following the BaseGrader abstraction pattern.

Last Updated: 2025-12-01
Constitution: .cdo-aifc/memory/archetypes/02-ml-operations-lifecycle/language-model-evaluation-constitution.md
"""

import asyncio
import pandas as pd
import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict, Callable, Union, Tuple


# ============================================================================
# Core Data Structures
# ============================================================================

@dataclass
class EvaluationInput:
    """
    Standardized input for all graders.
    """
    response: str
    prompt: Optional[str] = None
    system_prompt: Optional[str] = None
    context: Optional[Dict[str, Any]] = field(default_factory=dict)


@dataclass
class GradeResult:
    """
    Standardized output from all graders.
    """
    grader_name: str
    score: float
    reasoning: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


# ============================================================================
# Base Grader Classes
# ============================================================================

class BaseGrader(ABC):
    """
    Abstract base class for all graders.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def grade(self, input_data: EvaluationInput) -> GradeResult:
        """
        Async method to grade the input.
        """
        pass


class Heuristic(BaseGrader):
    """
    Base class for deterministic heuristics.
    Subclasses should implement the `compute_score` method.
    """
    async def grade(self, input_data: EvaluationInput) -> GradeResult:
        try:
            # Heuristics are usually CPU bound, but we make them async compatible
            # In a real app, you might want to run heavy CPU tasks in a thread pool
            score, reasoning, metadata = self.compute_score(input_data)
            return GradeResult(
                grader_name=self.name,
                score=score,
                reasoning=reasoning,
                metadata=metadata
            )
        except Exception as e:
            return GradeResult(
                grader_name=self.name,
                score=0.0,
                error=str(e)
            )

    @abstractmethod
    def compute_score(self, input_data: EvaluationInput) -> Tuple[float, Optional[str], Dict[str, Any]]:
        pass


class LLMJudge(BaseGrader):
    """
    Generic LLM Judge that uses composition for prompts.
    """
    def __init__(self, name: str, judge_prompt_template: str, llm_callable: Callable[[str], str], parser: Optional[Callable[[str], Tuple[float, str]]] = None):
        """
        Args:
            name: Name of the grader.
            judge_prompt_template: A string template for the judge's instructions. 
                                   Can use {response}, {prompt}, {system_prompt}.
            llm_callable: An async function that takes a prompt string and returns a string response.
            parser: Optional function to parse the LLM response into (score, reasoning).
        """
        super().__init__(name)
        self.judge_prompt_template = judge_prompt_template
        self.llm_callable = llm_callable
        self.parser = parser or self._default_parser

    async def grade(self, input_data: EvaluationInput) -> GradeResult:
        try:
            # Format the prompt for the judge
            formatted_prompt = self.judge_prompt_template.format(
                response=input_data.response,
                prompt=input_data.prompt or "",
                system_prompt=input_data.system_prompt or ""
            )
            
            # Call the LLM
            llm_response = await self.llm_callable(formatted_prompt)
            
            # Parse the response
            score, reasoning = self.parser(llm_response)
            
            return GradeResult(
                grader_name=self.name,
                score=score,
                reasoning=reasoning,
                metadata={"raw_llm_response": llm_response}
            )
        except Exception as e:
            return GradeResult(
                grader_name=self.name,
                score=0.0,
                error=str(e)
            )

    def _default_parser(self, response: str) -> Tuple[float, str]:
        """
        Simple default parser that extracts numeric score from response.
        """
        try:
            # Look for "Score: X" or "Score: X.XX" pattern
            match = re.search(r'Score:\s*(\d+(?:\.\d+)?)', response, re.IGNORECASE)
            if match:
                return float(match.group(1)), response
            
            # Fallback: find any number
            match = re.search(r'\b\d+(\.\d+)?\b', response)
            if match:
                return float(match.group(0)), response
            
            return 0.0, response
        except:
            return 0.0, response


# ============================================================================
# Example Heuristic Graders
# ============================================================================

class LengthCheckGrader(Heuristic):
    """
    Heuristic grader that checks response length.
    """
    def __init__(self, min_length: int = 50, max_length: int = 500):
        super().__init__(name="length_check")
        self.min_length = min_length
        self.max_length = max_length
    
    def compute_score(self, input_data: EvaluationInput) -> Tuple[float, Optional[str], Dict[str, Any]]:
        length = len(input_data.response)
        
        if self.min_length <= length <= self.max_length:
            score = 1.0
            reasoning = f"Response length {length} is within acceptable range [{self.min_length}, {self.max_length}]"
        elif length < self.min_length:
            shortfall = self.min_length - length
            if shortfall <= 20:
                score = 0.5
                reasoning = f"Response is slightly short ({length} chars, target {self.min_length}+)"
            else:
                score = 0.0
                reasoning = f"Response is too short ({length} chars, minimum {self.min_length})"
        else:  # length > self.max_length
            excess = length - self.max_length
            if excess <= 50:
                score = 0.5
                reasoning = f"Response is slightly long ({length} chars, target ≤{self.max_length})"
            else:
                score = 0.0
                reasoning = f"Response is too long ({length} chars, maximum {self.max_length})"
        
        metadata = {
            "response_length": length,
            "min_length": self.min_length,
            "max_length": self.max_length
        }
        
        return score, reasoning, metadata


class FormatValidatorGrader(Heuristic):
    """
    Heuristic grader that validates JSON format and required fields.
    """
    def __init__(self, required_fields: Optional[List[str]] = None):
        super().__init__(name="format_validator")
        self.required_fields = required_fields or ["answer", "confidence"]
    
    def compute_score(self, input_data: EvaluationInput) -> Tuple[float, Optional[str], Dict[str, Any]]:
        try:
            # Attempt to parse as JSON
            data = json.loads(input_data.response)
            
            # Check if all required fields are present
            missing_fields = [field for field in self.required_fields if field not in data]
            
            if not missing_fields:
                score = 1.0
                reasoning = f"Valid JSON with all required fields: {self.required_fields}"
            else:
                score = 0.0
                reasoning = f"Valid JSON but missing required fields: {missing_fields}"
            
            metadata = {
                "is_valid_json": True,
                "parsed_fields": list(data.keys()),
                "missing_fields": missing_fields
            }
            
        except json.JSONDecodeError as e:
            score = 0.0
            reasoning = f"Invalid JSON format: {str(e)}"
            metadata = {
                "is_valid_json": False,
                "parse_error": str(e)
            }
        
        return score, reasoning, metadata


class KeywordPresenceGrader(Heuristic):
    """
    Heuristic grader that checks for required or forbidden keywords.
    """
    def __init__(self, required_keywords: Optional[List[str]] = None, 
                 forbidden_keywords: Optional[List[str]] = None):
        super().__init__(name="keyword_presence")
        self.required_keywords = required_keywords or []
        self.forbidden_keywords = forbidden_keywords or []
    
    def compute_score(self, input_data: EvaluationInput) -> Tuple[float, Optional[str], Dict[str, Any]]:
        response_lower = input_data.response.lower()
        
        # Check required keywords
        missing_required = [kw for kw in self.required_keywords if kw.lower() not in response_lower]
        
        # Check forbidden keywords
        present_forbidden = [kw for kw in self.forbidden_keywords if kw.lower() in response_lower]
        
        # Calculate score
        if missing_required or present_forbidden:
            score = 0.0
            issues = []
            if missing_required:
                issues.append(f"missing required keywords: {missing_required}")
            if present_forbidden:
                issues.append(f"contains forbidden keywords: {present_forbidden}")
            reasoning = f"Keyword validation failed - {'; '.join(issues)}"
        else:
            score = 1.0
            reasoning = "All keyword checks passed"
        
        metadata = {
            "missing_required": missing_required,
            "present_forbidden": present_forbidden
        }
        
        return score, reasoning, metadata


# ============================================================================
# Evaluator Orchestration
# ============================================================================

class Evaluator:
    """
    Orchestrator class to run evaluations with concurrency control.
    """
    def __init__(self, graders: List[BaseGrader], max_concurrency: int = 5):
        self.graders = graders
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def evaluate_item(self, input_data: EvaluationInput) -> Dict[str, Any]:
        """
        Runs all graders for a single item.
        """
        tasks = []
        for grader in self.graders:
            tasks.append(self._run_grader_safe(grader, input_data))
        
        results = await asyncio.gather(*tasks)
        
        # Flatten results into a single dictionary row
        row = {
            "response": input_data.response,
            "prompt": input_data.prompt,
        }
        
        for res in results:
            row[f"{res.grader_name}_score"] = res.score
            row[f"{res.grader_name}_reasoning"] = res.reasoning
            if res.error:
                row[f"{res.grader_name}_error"] = res.error
                
        return row

    async def _run_grader_safe(self, grader: BaseGrader, input_data: EvaluationInput) -> GradeResult:
        """
        Runs a grader with semaphore protection.
        """
        async with self.semaphore:
            return await grader.grade(input_data)

    async def evaluate_batch(self, inputs: List[EvaluationInput]) -> pd.DataFrame:
        """
        Runs evaluation on a batch of inputs.
        """
        tasks = [self.evaluate_item(item) for item in inputs]
        results = await asyncio.gather(*tasks)
        return pd.DataFrame(results)


# ============================================================================
# Example Usage
# ============================================================================

async def example_usage():
    """
    Example of how to use the grader library.
    """
    # Create sample inputs
    inputs = [
        EvaluationInput(
            response='{"answer": "42", "confidence": 0.95}',
            prompt="What is the answer to life, the universe, and everything?",
            context={"ground_truth": "42"}
        ),
        EvaluationInput(
            response="The answer is clearly 42, as stated in the Hitchhiker's Guide to the Galaxy.",
            prompt="What is the answer to life, the universe, and everything?",
            context={"ground_truth": "42"}
        )
    ]
    
    # Create graders
    graders = [
        LengthCheckGrader(min_length=10, max_length=200),
        FormatValidatorGrader(required_fields=["answer", "confidence"]),
        KeywordPresenceGrader(required_keywords=["42"])
    ]
    
    # Create evaluator
    evaluator = Evaluator(graders=graders, max_concurrency=3)
    
    # Run evaluation
    results_df = await evaluator.evaluate_batch(inputs)
    
    print(results_df)
    return results_df


if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())
