"""Example usage of task decorator."""

import os
from typing import List
from dataclasses import dataclass
import requests
from fungai import task, tool

# Set up environment (you would set these as actual environment variables)
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"



@tool
def public_holiday(country_code: str, year:int) -> List[Event]:
    """Tool used for retrieving public holiday
    - country_code: ISO 3166-1 alpha-2"""
    
    url = "https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}".format(
        year=year, country_code=country_code
    )

    resp = requests.get(url)