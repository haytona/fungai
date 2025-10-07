"""Example usage of tool decorator."""

import os
import requests
from typing import List
from dataclasses import dataclass

# Set up environment
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"

from fungai import tool, task, ToolRegistry


@dataclass
class Event:
    name: str
    date: str
    country: str


@tool
def public_holiday(country_code: str, year: int) -> List[Event]:
    """Tool used for retrieving public holiday
    - country_code: ISO 3166-1 alpha-2"""
    # Mock implementation - in real use this would call an API
    return [
        Event("New Year's Day", f"{year}-01-01", country_code),
        Event("Christmas Day", f"{year}-12-25", country_code)
    ]


@task
def get_holidays_for_country(country: str, year: int) -> List[Event]:
    """Get all public holidays for a given country and year"""
    pass


if __name__ == "__main__":
    # Check what tools are registered
    registry = ToolRegistry()
    tools = registry.get_tools()
    print("Registered tools:")
    for path, info in tools.items():
        print(f"  {path}: {info['docstring']}")
    
    # Use the task that can access registered tools
    holidays = get_holidays_for_country("AU", 2024)
    print(f"Holidays: {holidays}")