"""Promotions that can be added to products."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from products import Product


class Promotion(ABC):
    """Abstract base class for all promotions."""

    def __init__(self, name: str) -> None:
        """Create a promotion with a name."""
        self.name: str = name

    @abstractmethod
    def apply_promotion(self, product: Product, quantity: int) -> float:
        """Return the total price with the promotion applied."""


class PercentDiscount(Promotion):
    """A percent discount on the total price."""

    def __init__(self, name: str, percent: float) -> None:
        """Create a percent discount with a name and a percent value."""
        super().__init__(name)
        self.percent: float = percent

    def apply_promotion(self, product: Product, quantity: int) -> float:
        """Return the price minus the percent discount."""
        return product.price * quantity * (1 - self.percent / 100)


class SecondHalfPrice(Promotion):
    """Every second item costs half price."""

    def apply_promotion(self, product: Product, quantity: int) -> float:
        """Return the price where every second item is half price."""
        full_price_items = quantity // 2 + quantity % 2
        half_price_items = quantity // 2
        half_price = product.price * 0.5
        return full_price_items * product.price + half_price_items * half_price


class ThirdOneFree(Promotion):
    """Every third item is free."""

    def apply_promotion(self, product: Product, quantity: int) -> float:
        """Return the price where every third item is free."""
        paid_items = quantity - quantity // 3
        return paid_items * product.price
