# FungAI

FungAI is an intelligent function decorator that uses Large Language Models (LLMs) to automatically implement function logic based on docstring descriptions. It analyzes whether tasks are deterministic (solvable with standard programming) or probabilistic (requiring AI inference) and handles each appropriately.

## Purpose

FungAI bridges the gap between natural language descriptions and code implementation by:

- **Automatic Implementation**: Write function signatures with docstrings, let AI implement the logic
- **Smart Analysis**: Distinguishes between deterministic tasks (calculations, sorting) and probabilistic tasks (NLP, classification)
- **Type Safety**: Enforces input/output types and validates results
- **Tool Integration**: Allows functions to call registered tools for complex workflows
- **Multi-LLM Support**: Works with OpenAI, Ollama, and other providers

## Quick Start

### Step 1: Install FungAI

```bash
pip install git+https://github.com/geeknam/fungai.git
```

### Step 2: Configure Environment

```bash
# For OpenAI (default)
export OPENAI_API_KEY="your-api-key"
export LLM_PROVIDER="openai"

# For Ollama
export LLM_PROVIDER="ollama"
export OLLAMA_BASE_URL="http://localhost:11434"
```

### Step 3: Define Your Data Models

```python
from dataclasses import dataclass
from typing import List

@dataclass
class ShoppingItem:
    name: str
    price: float = None
```

### Step 4: Use @task Decorator

## Usage Examples

```python
import os
from fungai import task

# Set up environment (you would set these as actual environment variables)
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"


@task
def categorise(items: List[ShoppingItem], category: str) -> List[ShoppingItem]:
    """For every item, find items that are in the same category as category arg"""
    pass

@task
def estimate_price(items: List[ShoppingItem]) -> List[ShoppingItem]:
    """For every item, estimate rough market price in AUD and
    then populate price attribute"""
    pass

@task
def find_most_expensive(items: List[ShoppingItem]) -> ShoppingItem:
    """Given all items, return only 1 item that is the most expensive"""
    pass


if __name__ == "__main__":
    # Example usage
    items = [
        ShoppingItem("apple"),
        ShoppingItem("apple iphone 17 pro"),
        ShoppingItem("milk"),
        ShoppingItem("beef steak"),
        ShoppingItem("banana"),
        ShoppingItem("grape")
    ]
    print(find_most_expensive(items))
    # ShoppingItem(name='apple iphone 17 pro', price=None)

    # NLP, categorisation problem: Find fruits
    fruits = categorise(items, "fruits")
    print(f"Fruits: {fruits}")
    # > Fruits: [ShoppingItem(name='apple', price=None), ShoppingItem(name='banana', price=None), ShoppingItem(name='grape', price=None)]

    # Probabilistic problem: Enrich items with estimated price
    fruits = estimate_price(fruits)
    print(f"Fruits with price: {fruits}")
    # > Fruits with price: [ShoppingItem(name='apple', price=3.5), ShoppingItem(name='banana', price=2.0), ShoppingItem(name='grape', price=6.0)]

    # Deterministic problem: Total price for Fruits
    total_price = sum(item.price for item in fruits if item.price is not None)
    print(f"Rough total price for fruits: {total_price}AUD")
    # > Rough total price for fruits: 11.5 AUD
```

## Key Features

- `@task` decorator for AI-powered function implementation
- `@tool` decorator for registering reusable functions
- Automatic deterministic vs probabilistic task detection
- Type validation and conversion
- Environment-based LLM provider configuration

## How It Works

1. **Task Analysis**: LLM analyzes the function docstring to determine if it's deterministic or probabilistic
2. **Deterministic Tasks**: Raises `DeterministicException` with suggested code implementation
3. **Probabilistic Tasks**: Uses LLM to process inputs and generate outputs matching the return type
4. **Tool Integration**: Automatically discovers and uses registered `@tool` functions when needed
5. **Type Validation**: Ensures inputs and outputs match the specified types

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider ("openai" or "ollama") | "openai" |
| `OPENAI_API_KEY` | OpenAI API key | Required for OpenAI |
| `OPENAI_MODEL` | OpenAI model name | "gpt-4o-mini" |
| `OLLAMA_BASE_URL` | Ollama server URL | "http://localhost:11434" |
| `OLLAMA_MODEL` | Ollama model name | "gemma3:4b" |
| `OLLAMA_SEED` | Seed for reproducible results | "123" |

### Exception Handling

```python
from fungai import task, DeterministicException

try:
    result = my_task(data)
except DeterministicException as e:
    print(f"Task should be implemented manually: {e}")
```

## Best Practices

- Write clear, specific docstrings describing the expected behavior
- Use proper type hints for inputs and outputs
- Handle `DeterministicException` for tasks that should be manually implemented
- Register frequently used functions as `@tool` for reuse across tasks
- Test with different LLM providers to find the best fit for your use case

## License

MIT