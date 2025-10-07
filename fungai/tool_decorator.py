"""Tool decorator implementation."""

import functools
from .registry import ToolRegistry


def tool(func):
    """Decorator to register a function as a tool."""
    registry = ToolRegistry()
    registry.register(func)
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    return wrapper