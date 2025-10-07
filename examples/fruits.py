"""Example usage of task decorator."""

import os
from typing import List
from dataclasses import dataclass
from fungai import task

# Set up environment (you would set these as actual environment variables)
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"


@dataclass
class GroceryItem:
    name: str
    weight_kg: float
    price: float = None


@task
def filter_prefix(items: List[GroceryItem], prefix: str) -> List[GroceryItem]:
    """For every item, find items with name starting prefix matching prefix arg"""
    pass

@task
def categorise(items: List[GroceryItem], category: str) -> List[GroceryItem]:
    """For every item, find items that are in the same category as category arg"""
    pass

@task
def estimate_price(items: List[GroceryItem]) -> List[GroceryItem]:
    """For every item, estimate rough price in AUD based on weight_kg
    then populate price attribute"""
    pass


if __name__ == "__main__":
    # Example usage
    items = [
        GroceryItem("apple", 1),
        GroceryItem("milk", 2),
        GroceryItem("beef steak", 0.5),
        GroceryItem("banana", 1),
        GroceryItem("grape", 2)
    ]
    
    # NLP problem: Find fruits
    fruits = categorise(items, "fruits")
    print(f"Fruits: {fruits}")
    # > Fruits: [GroceryItem(name='apple', weight_kg=1, price=None), GroceryItem(name='banana', weight_kg=1, price=None), GroceryItem(name='grape', weight_kg=2, price=None)]

    # Probabilistic problem: Enrich with price info
    fruits = estimate_price(fruits)
    print(f"Fruits with price: {fruits}")
    # > Fruits with price: [GroceryItem(name='apple', weight_kg=1, price=3.5), GroceryItem(name='banana', weight_kg=1, price=2.0), GroceryItem(name='grape', weight_kg=2, price=6.0)]

    # Deterministic problem: Total price for Fruits
    total_price = sum(item.price for item in fruits if item.price is not None)
    print(f"Rough total price for fruits: {total_price}AUD")
    # > Rough total price for fruits: 11.5 AUD