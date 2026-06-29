from __future__ import annotations
from products import Product


class Store:
    def __init__(self, product_list: list[Product]) -> None:
        self.products: list[Product] = product_list

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product: Product) -> None:
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        total = 0
        for product in self.products:
            total += product.quantity
        return total

    def get_all_products(self) -> list[Product]:
        active: list[Product] = []
        for product in self.products:
            if product.is_active():
                active.append(product)
        return active

    def order(self, shopping_list: list[tuple[Product, int]]) -> float:
        total = 0.0
        for product, quantity in shopping_list:
            total += product.buy(quantity)
        return total
