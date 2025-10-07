"""LLM client implementations."""

import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict

import requests
import openai


class LLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def generate(self, context: Dict[str, Any]) -> Any:
        """Generate response based on context."""
        pass
    
    def _parse_response(self, result: str) -> Any:
        """Parse LLM response, handling markdown code blocks."""
        # Remove markdown code blocks
        if "```json" in result:
            start = result.find("```json") + 7
            end = result.find("```", start)
            result = result[start:end].strip()
        elif "```" in result:
            start = result.find("```") + 3
            end = result.find("```", start)
            result = result[start:end].strip()
        
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return result
    
    def _build_prompt(self, context: Dict[str, Any]) -> str:
        """Build prompt based on context."""
        return f"""
Function: {context['function_name']}
Task: {context['prompt']}
Arguments: {json.dumps(context['arguments'], indent=2)}
Return Type: {context['return_type']}

Return ONLY valid JSON that matches the return type exactly. No explanations, no markdown formatting.
"""


class OpenAIClient(LLMClient):
    """OpenAI client implementation."""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    def generate(self, context: Dict[str, Any]) -> Any:
        prompt = self._build_prompt(context)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        result = response.choices[0].message.content.strip()
        return self._parse_response(result)


class OllamaClient(LLMClient):
    """Ollama client implementation."""
    
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "gemma3:4b")
        try:
            self.seed = int(os.getenv("OLLAMA_SEED", "123"))
        except ValueError:
            self.seed = 123
        self.session = requests.Session()
    
    def generate(self, context: Dict[str, Any]) -> Any:
        prompt = self._build_prompt(context)
        
        response = self.session.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                # "format": "json",
                # Set seed for reproducibility
                "options": {
                    "seed": self.seed,
                },
                "stream": False
            }
        )
        resp = response.json()
        result = resp["response"].strip()
        return self._parse_response(result)


def get_llm_client() -> LLMClient:
    """Get LLM client based on environment configuration."""
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider == "openai":
        return OpenAIClient()
    elif provider == "ollama":
        return OllamaClient()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")