# FungAI

LLM-powered function decorator with type enforcement.

## Installation

```bash
pip install fungai
```

## Usage

```python
from typing import List
from fungai import fungai

@fungai
def my_logic(items: List[MyClass], needle: str) -> List[MyClass]:
    """For every item, find items that have object.name fuzzily matched to needle"""
    pass  # Implementation will be handled by LLM
```

## Configuration

Set environment variables:
- `OPENAI_API_KEY` for OpenAI
- `OLLAMA_BASE_URL` for Ollama (optional, defaults to http://localhost:11434)
- `LLM_PROVIDER` - either "openai" or "ollama" (defaults to "openai")

## License

MIT