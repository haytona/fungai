"""Type validation and conversion utilities."""

import json
from typing import Any, List, Dict, Union, get_origin, get_args

from pydantic import BaseModel, ValidationError, create_model


def validate_and_convert(value: Any, expected_type: type) -> Any:
    """Validate and convert value to expected type."""
    
    # Handle basic types
    if expected_type in (str, int, float, bool):
        return expected_type(value)
    
    # Handle Any type
    if expected_type is Any:
        return value
    
    # Handle generic types
    origin = get_origin(expected_type)
    args = get_args(expected_type)
    
    if origin is list or origin is List:
        if not isinstance(value, list):
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    raise ValueError(f"Cannot convert {value} to list")
            else:
                raise ValueError(f"Expected list, got {type(value)}")
        
        if args:
            return [validate_and_convert(item, args[0]) for item in value]
        return list(value)
    
    if origin is dict or origin is Dict:
        if not isinstance(value, dict):
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    raise ValueError(f"Cannot convert {value} to dict")
            else:
                raise ValueError(f"Expected dict, got {type(value)}")
        return value
    
    if origin is Union:
        # Try each type in the Union
        for arg_type in args:
            try:
                return validate_and_convert(value, arg_type)
            except (ValueError, TypeError):
                continue
        raise ValueError(f"Cannot convert {value} to any type in {expected_type}")
    
    # Handle custom classes/models (including dataclasses)
    if hasattr(expected_type, '__annotations__'):
        if isinstance(value, dict):
            try:
                return expected_type(**value)
            except (TypeError, ValueError):
                pass
    
    # If all else fails, try direct conversion
    try:
        return expected_type(value)
    except (ValueError, TypeError):
        return value