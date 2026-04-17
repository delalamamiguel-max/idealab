"""Schema generation helpers for MCP tools."""

from pydantic import BaseModel, Field
from typing import Any, Optional, get_type_hints
import inspect


def generate_input_schema(
    tool_name: str,
    parameters: dict[str, tuple[type, str]],
    defaults: Optional[dict[str, Any]] = None
) -> type[BaseModel]:
    """Generate Pydantic input schema from parameters.
    
    Args:
        tool_name: Name of the tool
        parameters: Dict of {param_name: (type, description)}
        defaults: Optional default values
        
    Returns:
        Generated Pydantic model class
    """
    defaults = defaults or {}
    
    fields = {}
    for param_name, (param_type, description) in parameters.items():
        default_value = defaults.get(param_name, ...)
        fields[param_name] = (
            param_type,
            Field(default=default_value, description=description)
        )
    
    schema_class = type(
        f"{tool_name.title().replace('_', '')}Input",
        (BaseModel,),
        {
            "__annotations__": {k: v[0] for k, v in fields.items()},
            **{k: v[1] for k, v in fields.items()}
        }
    )
    
    schema_class.__doc__ = f"Input schema for {tool_name} tool."
    
    return schema_class


def generate_output_schema(
    tool_name: str,
    fields: dict[str, tuple[type, str]]
) -> type[BaseModel]:
    """Generate Pydantic output schema.
    
    Args:
        tool_name: Name of the tool
        fields: Dict of {field_name: (type, description)}
        
    Returns:
        Generated Pydantic model class
    """
    schema_fields = {}
    for field_name, (field_type, description) in fields.items():
        schema_fields[field_name] = (
            field_type,
            Field(description=description)
        )
    
    schema_class = type(
        f"{tool_name.title().replace('_', '')}Output",
        (BaseModel,),
        {
            "__annotations__": {k: v[0] for k, v in schema_fields.items()},
            **{k: v[1] for k, v in schema_fields.items()}
        }
    )
    
    schema_class.__doc__ = f"Output schema for {tool_name} tool."
    
    return schema_class


def infer_schema_from_function(func) -> tuple[type[BaseModel], type[BaseModel]]:
    """Infer input and output schemas from function signature.
    
    Args:
        func: Function to analyze
        
    Returns:
        Tuple of (InputSchema, OutputSchema)
    """
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)
    
    # Generate input schema
    input_params = {}
    defaults = {}
    
    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue
        
        param_type = type_hints.get(param_name, Any)
        description = f"Parameter {param_name}"
        
        input_params[param_name] = (param_type, description)
        
        if param.default != inspect.Parameter.empty:
            defaults[param_name] = param.default
    
    input_schema = generate_input_schema(
        func.__name__,
        input_params,
        defaults
    )
    
    # Generate output schema
    return_type = type_hints.get("return", str)
    output_schema = generate_output_schema(
        func.__name__,
        {"result": (return_type, "Function result")}
    )
    
    return input_schema, output_schema


def generate_error_schema() -> type[BaseModel]:
    """Generate standard error schema.
    
    Returns:
        ToolError Pydantic model
    """
    class ToolError(BaseModel):
        """Structured error response for tools."""
        code: str = Field(description="Error code (VALIDATION_ERROR, TIMEOUT, etc.)")
        message: str = Field(description="Human-readable error message")
        retryable: bool = Field(default=False, description="Whether error is retryable")
        details: Optional[dict] = Field(default=None, description="Additional error details")
    
    return ToolError
