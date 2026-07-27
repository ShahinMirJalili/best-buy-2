from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from products import Product


class Promotion(ABC):
    """Abstrakte Basisklasse für alle Promotions (Rabattaktionen)."""

    def __init__(self, name: str) -> None:
        """Legt eine Promotion mit einem Namen an."""
        self.name: str = name

    @abstractmethod
    def apply_promotion(self, product: Product, quantity: int) -> float:
        """Berechnet den Gesamtpreis für die Menge unter Anwendung der Promotion."""
        pass


class PercentDiscount(Promotion):
    """Promotion mit prozentualem Rabatt auf den Gesamtpreis."""

    def __init__(self, name: str, percent: float) -> None:
        """Legt einen Prozent-Rabatt mit Namen und Prozentsatz an."""
        super().__init__(name)
        self.percent: float = percent

    def apply_promotion(self, product: Product, quantity: int) -> float:
        """Gibt den Preis abzüglich des Prozent-Rabatts zurück."""
        return product.price * quantity * (1 - self.percent / 100)


class SecondHalfPrice(Promotion):
    """Promotion: jedes zweite Produkt zum halben Preis."""

    def apply_promotion(self, product: Product, quantity: int) -> float:
        """Berechnet den Preis, wobei jedes zweite Stück halb so viel kostet."""
        full_price_items = quantity // 2 + quantity % 2
        half_price_items = quantity // 2
        return full_price_items * product.price + half_price_items * product.price * 0.5


class ThirdOneFree(Promotion):
    """Promotion: jedes dritte Produkt ist gratis."""

    def apply_promotion(self, product: Product, quantity: int) -> float:
        """Berechnet den Preis, wobei jedes dritte Stück kostenlos ist."""
        paid_items = quantity - quantity // 3
        return paid_items * product.price
