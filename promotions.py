from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from products import Product


class Promotion(ABC):
    def __init__(self, name: str) -> None:
        self.name: str = name

    @abstractmethod
    def apply_promotion(self, product: Product, quantity: int) -> float:
        pass


class PercentDiscount(Promotion):
    def __init__(self, name: str, percent: float) -> None:
        super().__init__(name)
        self.percent: float = percent

    def apply_promotion(self, product: Product, quantity: int) -> float:
        return product.price * quantity * (1 - self.percent / 100)


class SecondHalfPrice(Promotion):
    def apply_promotion(self, product: Product, quantity: int) -> float:
        full_price_items = quantity // 2 + quantity % 2
        half_price_items = quantity // 2
        return full_price_items * product.price + half_price_items * product.price * 0.5


class ThirdOneFree(Promotion):
    def apply_promotion(self, product: Product, quantity: int) -> float:
        paid_items = quantity - quantity // 3
        return paid_items * product.price
