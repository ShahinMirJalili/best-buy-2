from __future__ import annotations
from products import Product


class Store:
    """Verwaltet eine Liste von Produkten und ermöglicht Bestellungen."""

    def __init__(self, product_list: list[Product]) -> None:
        """Legt den Store mit einer Startliste von Produkten an."""
        self.products: list[Product] = product_list

    def add_product(self, product: Product) -> None:
        """Fügt ein Produkt zum Store hinzu."""
        self.products.append(product)

    def remove_product(self, product: Product) -> None:
        """Entfernt ein Produkt aus dem Store."""
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        """Gibt die Gesamtmenge aller aktiven Produkte im Store zurück."""
        total = 0
        for product in self.products:
            if product.is_active():
                total += product.quantity
        return total

    def get_all_products(self) -> list[Product]:
        """Gibt eine Liste aller aktiven Produkte zurück."""
        active: list[Product] = []
        for product in self.products:
            if product.is_active():
                active.append(product)
        return active

    def order(self, shopping_list: list[tuple[Product, int]]) -> float:
        """Führt eine Bestellung aus und gibt den Gesamtpreis zurück."""
        total = 0.0
        for product, quantity in shopping_list:
            total += product.buy(quantity)
        return total
