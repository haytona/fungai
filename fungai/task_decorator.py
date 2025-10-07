"""Task decorator that can use registered tools."""

import functools
import inspect
import json
from typing import Any, get_type_hints

from .llm_client import get_llm_client
from .type_validator import validate_and_convert
from .registry import ToolRegistry


def task(func):
    """Decorator that replaces function implementation with LLM-generated results using available tools."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get function signature and type hints
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        
        # Bind arguments to parameters
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        # Validate input types
        for param_name, value in bound_args.arguments.items():
            if param_name in type_hints:
                validate_and_convert(value, type_hints[param_name])
        
        # Get available tools
        registry = ToolRegistry()
        available_tools = registry.get_tools()
        
        # Get docstring as prompt
        prompt = func.__doc__ or "Process the given inputs"
        
        # Prepare context with available tools
        context = {
            "function_name": func.__name__,
            "arguments": {k: str(v) for k, v in bound_args.arguments.items()},
            "return_type": str(type_hints.get('return', 'Any')),
            "prompt": prompt,
            "available_tools": {
                path: {
                    "name": tool_info["name"],
                    "arguments": tool_info["arguments"],
                    "return_type": tool_info["return_type"],
                    "docstring": tool_info["docstring"]
                }
                for path, tool_info in available_tools.items()
            }
        }
        
        # Call LLM
        client = get_llm_client()
        result = client.generate(context)
        
        # Validate and convert return type
        return_type = type_hints.get('return', Any)
        return validate_and_convert(result, return_type)
    
    return wrapper