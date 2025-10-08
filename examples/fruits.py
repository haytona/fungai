"""Example usage of task decorator."""

import os
from typing import List
from dataclasses import dataclass
from fungai import task

# Set up environment (you would set these as actual environment variables)
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"


@dataclass
class ShoppingItem:
    name: str
    price: float = None


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