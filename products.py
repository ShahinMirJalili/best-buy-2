from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from promotions import Promotion


class Product:
    def __init__(self, name: str, price: float, quantity: int) -> None:
        if not name:
            raise ValueError("Name darf nicht leer sein")
        if price < 0:
            raise ValueError("Price darf nicht negativ sein")
        if quantity < 0:
            raise ValueError("Quantity darf nicht negativ sein")
        self.name: str = name
        self.price: float = price
        self.quantity: int = quantity
        self.active: bool = True
        self.promotion: Promotion | None = None

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()
        else:
            self.activate()

    def is_active(self) -> bool:
        return self.active

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    def get_promotion(self) -> Promotion | None:
        return self.promotion

    def set_promotion(self, promotion: Promotion) -> None:
        self.promotion = promotion

    def show(self) -> None:
        info = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        if self.promotion:
            info += f", Promotion: {self.promotion.name}"
        print(info)

    def buy(self, quantity: int) -> float:
        if not self.active:
            raise ValueError("Produkt ist nicht aktiv")
        if quantity > self.quantity:
            raise ValueError("Nicht genug auf Lager")
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity
        self.set_quantity(self.quantity - quantity)
        return total_price


class NonStockedProduct(Product):
    def __init__(self, name: str, price: float) -> None:
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity: int) -> None:
        pass

    def buy(self, quantity: int) -> float:
        if not self.active:
            raise ValueError("Produkt ist nicht aktiv")
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity

    def show(self) -> None:
        info = f"{self.name}, Price: {self.price}, Quantity: Unlimited"
        if self.promotion:
            info += f", Promotion: {self.promotion.name}"
        print(info)


class LimitedProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, maximum: int) -> None:
        super().__init__(name, price, quantity)
        self.maximum: int = maximum

    def buy(self, quantity: int) -> float:
        if quantity > self.maximum:
            raise ValueError(f"Nur {self.maximum} mal pro Bestellung erlaubt")
        return super().buy(quantity)

    def show(self) -> None:
        info = f"{self.name}, Price: {self.price}, Limited to {self.maximum} per order!"
        if self.promotion:
            info += f", Promotion: {self.promotion.name}"
        print(info)
