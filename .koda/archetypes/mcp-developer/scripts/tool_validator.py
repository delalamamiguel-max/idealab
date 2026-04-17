"""Tool validation helpers for MCP development."""

from pydantic import BaseModel, ValidationError
from typing import Any, Optional
import json
import logging

logger = logging.getLogger(__name__)


class ToolValidationResult(BaseModel):
    """Result of tool validation."""
    is_valid: bool
    errors: list[str] = []
    warnings: list[str] = []
    validated_input: Optional[dict] = None


def validate_tool_input(input_data: dict, schema_class: type[BaseModel]) -> ToolValidationResult:
    """Validate tool input against Pydantic schema.
    
    Args:
        input_data: Input data to validate
        schema_class: Pydantic model class
        
    Returns:
        Validation result
    """
    result = ToolValidationResult(is_valid=True)
    
    try:
        validated = schema_class(**input_data)
        result.validated_input = validated.model_dump()
        logger.debug(f"Input validation passed for {schema_class.__name__}")
    except ValidationError as e:
        result.is_valid = False
        result.errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        logger.warning(f"Input validation failed: {result.errors}")
    
    return result


def validate_tool_output(output_data: Any, expected_type: type) -> ToolValidationResult:
    """Validate tool output type.
    
    Args:
        output_data: Output data to validate
        expected_type: Expected output type
        
    Returns:
        Validation result
    """
    result = ToolValidationResult(is_valid=True)
    
    if not isinstance(output_data, expected_type):
        result.is_valid = False
        result.errors.append(
            f"Expected type {expected_type.__name__}, got {type(output_data).__name__}"
        )
    
    # Check if output is JSON serializable
    try:
        json.dumps(output_data)
    except (TypeError, ValueError) as e:
        result.warnings.append(f"Output not JSON serializable: {e}")
    
    return result


def check_tool_description_quality(tool_func) -> ToolValidationResult:
    """Check quality of tool description and docstring.
    
    Args:
        tool_func: Tool function to check
        
    Returns:
        Validation result
    """
    result = ToolValidationResult(is_valid=True)
    
    # Check docstring exists
    if not tool_func.__doc__:
        result.errors.append("Tool missing docstring")
        result.is_valid = False
        return result
    
    docstring = tool_func.__doc__.strip()
    
    # Check docstring length
    if len(docstring) < 20:
        result.warnings.append("Docstring too short (< 20 chars)")
    
    # Check for common issues
    if "TODO" in docstring.upper():
        result.warnings.append("Docstring contains TODO")
    
    if not docstring[0].isupper():
        result.warnings.append("Docstring should start with capital letter")
    
    if not docstring.endswith("."):
        result.warnings.append("Docstring should end with period")
    
    # Check for side effects documentation
    if any(keyword in tool_func.__name__ for keyword in ["create", "update", "delete", "write"]):
        if "side effect" not in docstring.lower():
            result.warnings.append("Tool has side effects but docstring doesn't mention them")
    
    return result


def check_field_descriptions(schema_class: type[BaseModel]) -> ToolValidationResult:
    """Check that all fields have descriptions.
    
    Args:
        schema_class: Pydantic model class
        
    Returns:
        Validation result
    """
    result = ToolValidationResult(is_valid=True)
    
    for field_name, field_info in schema_class.model_fields.items():
        if not field_info.description:
            result.errors.append(f"Field '{field_name}' missing description")
            result.is_valid = False
    
    return result


def validate_tool_correctness(
    tool_func,
    test_cases: list[tuple[dict, Any]]
) -> ToolValidationResult:
    """Validate tool produces correct outputs.
    
    Args:
        tool_func: Tool function to test
        test_cases: List of (input, expected_output) tuples
        
    Returns:
        Validation result
    """
    result = ToolValidationResult(is_valid=True)
    
    for i, (input_data, expected_output) in enumerate(test_cases):
        try:
            actual_output = tool_func(**input_data)
            
            if actual_output != expected_output:
                result.errors.append(
                    f"Test case {i}: Expected {expected_output}, got {actual_output}"
                )
                result.is_valid = False
        except Exception as e:
            result.errors.append(f"Test case {i}: Exception {e}")
            result.is_valid = False
    
    return result
