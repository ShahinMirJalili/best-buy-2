"""Store class that manages the products."""
from __future__ import annotations
from products import Product


class Store:
    """A store that holds products and handles orders."""

    def __init__(self, product_list: list[Product]) -> None:
        """Create the store with a list of products."""
        self.products: list[Product] = product_list

    def add_product(self, product: Product) -> None:
        """Add a product to the store."""
        self.products.append(product)

    def remove_product(self, product: Product) -> None:
        """Remove a product from the store."""
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        """Return the total quantity of all active products."""
        total = 0
        for product in self.products:
            if product.is_active():
                total += product.quantity
        return total

    def get_all_products(self) -> list[Product]:
        """Return a list of all active products."""
        active: list[Product] = []
        for product in self.products:
            if product.is_active():
                active.append(product)
        return active

    def order(self, shopping_list: list[tuple[Product, int]]) -> float:
        """Buy all products in the shopping list and return the price."""
        total = 0.0
        for product, quantity in shopping_list:
            total += product.buy(quantity)
        return total
