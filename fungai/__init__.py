"""FungAI - LLM-powered function decorator with type enforcement."""
from .tool_decorator import tool
from .task_decorator import task
from .registry import ToolRegistry

__version__ = "0.1.0"
__all__ = ["fungai", "tool", "task", "ToolRegistry"]