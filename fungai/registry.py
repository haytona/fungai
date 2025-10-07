"""Tool registry for managing available tools."""

import inspect
from typing import Any, Dict, get_type_hints


class ToolRegistry:
    """Singleton registry for tools."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.tools = {}
        return cls._instance
    
    def register(self, func):
        """Register a tool function."""
        module = func.__module__
        name = func.__name__
        dotted_path = f"{module}.{name}"
        
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        
        self.tools[dotted_path] = {
            'function': func,
            'name': name,
            'dotted_path': dotted_path,
            'arguments': {
                param.name: {
                    'type': str(type_hints.get(param.name, 'Any')),
                    'required': param.default == param.empty
                }
                for param in sig.parameters.values()
            },
            'return_type': str(type_hints.get('return', 'Any')),
            'docstring': func.__doc__ or ""
        }
    
    def get_tools(self) -> Dict[str, Any]:
        """Get all registered tools."""
        return self.tools.copy()
    
    def get_tool(self, dotted_path: str) -> Dict[str, Any]:
        """Get a specific tool by dotted path."""
        return self.tools.get(dotted_path)