"""Programmatic assertion helpers for agent validation."""

from typing import Any, Callable, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class AssertionError(Exception):
    """Custom assertion error with detailed context."""
    
    def __init__(self, message: str, expected: Any = None, actual: Any = None, context: dict = None):
        super().__init__(message)
        self.expected = expected
        self.actual = actual
        self.context = context or {}
        self.timestamp = datetime.now().isoformat()


def assert_equals(actual: Any, expected: Any, message: Optional[str] = None):
    """Assert two values are equal.
    
    Args:
        actual: Actual value
        expected: Expected value
        message: Optional custom message
        
    Raises:
        AssertionError: If values not equal
    """
    if actual != expected:
        msg = message or f"Expected {expected}, got {actual}"
        raise AssertionError(msg, expected=expected, actual=actual)
    
    logger.debug(f"Assertion passed: {actual} == {expected}")


def assert_contains(container: Any, item: Any, message: Optional[str] = None):
    """Assert container contains item.
    
    Args:
        container: Container to check
        item: Item to find
        message: Optional custom message
        
    Raises:
        AssertionError: If item not in container
    """
    if item not in container:
        msg = message or f"Expected {container} to contain {item}"
        raise AssertionError(msg, expected=f"contains {item}", actual=container)
    
    logger.debug(f"Assertion passed: {item} in container")


def assert_json_schema(data: dict, schema: dict, message: Optional[str] = None):
    """Assert data matches JSON schema.
    
    Args:
        data: Data to validate
        schema: JSON schema
        message: Optional custom message
        
    Raises:
        AssertionError: If data doesn't match schema
    """
    from jsonschema import validate, ValidationError
    
    try:
        validate(instance=data, schema=schema)
        logger.debug("JSON schema validation passed")
    except ValidationError as e:
        msg = message or f"JSON schema validation failed: {e.message}"
        raise AssertionError(msg, expected=schema, actual=data, context={"error": str(e)})


def assert_state_transition(
    previous_state: dict,
    current_state: dict,
    expected_changes: dict,
    message: Optional[str] = None
):
    """Assert state transitioned correctly.
    
    Args:
        previous_state: State before transition
        current_state: State after transition
        expected_changes: Expected field changes
        message: Optional custom message
        
    Raises:
        AssertionError: If state didn't transition as expected
    """
    for field, expected_value in expected_changes.items():
        if field not in current_state:
            msg = message or f"Field {field} missing from current state"
            raise AssertionError(msg, expected=expected_value, actual=None)
        
        if current_state[field] != expected_value:
            msg = message or f"Field {field} has wrong value"
            raise AssertionError(
                msg,
                expected=expected_value,
                actual=current_state[field],
                context={
                    "field": field,
                    "previous": previous_state.get(field),
                    "current": current_state[field]
                }
            )
    
    logger.debug(f"State transition validated: {len(expected_changes)} changes")


def assert_tool_call_correct(
    tool_call: dict,
    expected_tool: str,
    expected_args: Optional[dict] = None,
    message: Optional[str] = None
):
    """Assert tool call is correct.
    
    Args:
        tool_call: Tool call dict with name and arguments
        expected_tool: Expected tool name
        expected_args: Expected arguments (if any)
        message: Optional custom message
        
    Raises:
        AssertionError: If tool call incorrect
    """
    # Check tool name
    if tool_call.get("name") != expected_tool:
        msg = message or f"Wrong tool called"
        raise AssertionError(
            msg,
            expected=expected_tool,
            actual=tool_call.get("name")
        )
    
    # Check arguments if provided
    if expected_args:
        actual_args = tool_call.get("arguments", {})
        for arg_name, expected_value in expected_args.items():
            if arg_name not in actual_args:
                msg = message or f"Missing argument {arg_name}"
                raise AssertionError(msg, expected=expected_value, actual=None)
            
            if actual_args[arg_name] != expected_value:
                msg = message or f"Wrong value for argument {arg_name}"
                raise AssertionError(
                    msg,
                    expected=expected_value,
                    actual=actual_args[arg_name],
                    context={"argument": arg_name}
                )
    
    logger.debug(f"Tool call validated: {expected_tool}")


def assert_trajectory_follows_path(
    trajectory: list[dict],
    expected_path: list[str],
    message: Optional[str] = None
):
    """Assert agent trajectory follows expected path.
    
    Args:
        trajectory: List of trajectory steps
        expected_path: Expected sequence of node names
        message: Optional custom message
        
    Raises:
        AssertionError: If trajectory doesn't match path
    """
    actual_path = [step.get("node") for step in trajectory]
    
    if len(actual_path) != len(expected_path):
        msg = message or f"Trajectory length mismatch"
        raise AssertionError(
            msg,
            expected=expected_path,
            actual=actual_path,
            context={
                "expected_length": len(expected_path),
                "actual_length": len(actual_path)
            }
        )
    
    for i, (expected_node, actual_node) in enumerate(zip(expected_path, actual_path)):
        if expected_node != actual_node:
            msg = message or f"Trajectory diverged at step {i}"
            raise AssertionError(
                msg,
                expected=expected_node,
                actual=actual_node,
                context={
                    "step": i,
                    "expected_path": expected_path,
                    "actual_path": actual_path
                }
            )
    
    logger.debug(f"Trajectory validated: {len(expected_path)} steps")


def assert_performance_within_sla(
    duration_ms: float,
    sla_ms: float,
    message: Optional[str] = None
):
    """Assert operation completed within SLA.
    
    Args:
        duration_ms: Actual duration in milliseconds
        sla_ms: SLA threshold in milliseconds
        message: Optional custom message
        
    Raises:
        AssertionError: If duration exceeds SLA
    """
    if duration_ms > sla_ms:
        msg = message or f"Performance SLA violated"
        raise AssertionError(
            msg,
            expected=f"<= {sla_ms}ms",
            actual=f"{duration_ms}ms",
            context={
                "sla_ms": sla_ms,
                "duration_ms": duration_ms,
                "overage_ms": duration_ms - sla_ms,
                "overage_pct": ((duration_ms - sla_ms) / sla_ms * 100)
            }
        )
    
    logger.debug(f"Performance within SLA: {duration_ms}ms <= {sla_ms}ms")


def assert_no_errors_in_logs(logs: list[str], message: Optional[str] = None):
    """Assert no error-level logs present.
    
    Args:
        logs: List of log messages
        message: Optional custom message
        
    Raises:
        AssertionError: If error logs found
    """
    error_logs = [log for log in logs if "ERROR" in log or "CRITICAL" in log]
    
    if error_logs:
        msg = message or f"Found {len(error_logs)} error logs"
        raise AssertionError(
            msg,
            expected="no errors",
            actual=f"{len(error_logs)} errors",
            context={"error_logs": error_logs[:5]}  # First 5 errors
        )
    
    logger.debug(f"No errors in {len(logs)} log messages")


def assert_output_grounded_in_context(
    output: str,
    context: str,
    threshold: float = 0.9,
    message: Optional[str] = None
):
    """Assert output is grounded in provided context.
    
    Args:
        output: Agent output
        context: Provided context
        threshold: Grounding threshold (0-1)
        message: Optional custom message
        
    Raises:
        AssertionError: If output not grounded
    """
    # Simple heuristic: check if key phrases from output appear in context
    # In production, use proper faithfulness metric
    output_phrases = set(output.lower().split())
    context_phrases = set(context.lower().split())
    
    overlap = len(output_phrases & context_phrases)
    grounding_score = overlap / len(output_phrases) if output_phrases else 0
    
    if grounding_score < threshold:
        msg = message or f"Output not sufficiently grounded in context"
        raise AssertionError(
            msg,
            expected=f">= {threshold}",
            actual=grounding_score,
            context={
                "threshold": threshold,
                "grounding_score": grounding_score,
                "overlap_words": overlap,
                "total_words": len(output_phrases)
            }
        )
    
    logger.debug(f"Output grounding validated: {grounding_score:.2f}")


class AssertionCollector:
    """Collect multiple assertions and report all failures."""
    
    def __init__(self):
        """Initialize assertion collector."""
        self.assertions = []
        self.failures = []
    
    def add_assertion(self, assertion_func: Callable, *args, **kwargs):
        """Add assertion to collector.
        
        Args:
            assertion_func: Assertion function to call
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        try:
            assertion_func(*args, **kwargs)
            self.assertions.append({
                "function": assertion_func.__name__,
                "status": "passed",
                "args": args,
                "kwargs": kwargs
            })
        except AssertionError as e:
            self.failures.append({
                "function": assertion_func.__name__,
                "error": str(e),
                "expected": e.expected,
                "actual": e.actual,
                "context": e.context
            })
            self.assertions.append({
                "function": assertion_func.__name__,
                "status": "failed",
                "error": str(e)
            })
    
    def assert_all_passed(self):
        """Assert all collected assertions passed.
        
        Raises:
            AssertionError: If any assertions failed
        """
        if self.failures:
            msg = f"{len(self.failures)} of {len(self.assertions)} assertions failed"
            raise AssertionError(
                msg,
                expected="all passed",
                actual=f"{len(self.failures)} failed",
                context={"failures": self.failures}
            )
        
        logger.info(f"All {len(self.assertions)} assertions passed")
    
    def get_report(self) -> dict:
        """Get assertion report.
        
        Returns:
            Report dict with all assertions and failures
        """
        return {
            "total": len(self.assertions),
            "passed": len(self.assertions) - len(self.failures),
            "failed": len(self.failures),
            "assertions": self.assertions,
            "failures": self.failures
        }
