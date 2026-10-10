"""Product classes for the Best Buy store."""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from promotions import Promotion


class Product:
    """A store product with name, price, quantity and a promotion."""

    def __init__(self, name: str, price: float, quantity: int) -> None:
        """Create a product and validate name, price and quantity."""
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
        """Return the current quantity."""
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        """Set the quantity and deactivate the product when it reaches 0."""
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()
        else:
            self.activate()

    def is_active(self) -> bool:
        """Return True if the product is active."""
        return self.active

    def activate(self) -> None:
        """Activate the product."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the product."""
        self.active = False

    def get_promotion(self) -> Promotion | None:
        """Return the current promotion or None."""
        return self.promotion

    def set_promotion(self, promotion: Promotion) -> None:
        """Set a promotion for the product."""
        self.promotion = promotion

    def show(self) -> None:
        """Print the product details and its promotion."""
        info = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        if self.promotion:
            info += f", Promotion: {self.promotion.name}"
        print(info)

    def buy(self, quantity: int) -> float:
        """Buy the given quantity and return the total price."""
        if not self.active:
            raise ValueError("Produkt ist nicht aktiv")
        if quantity <= 0:
            raise ValueError("Menge muss größer als 0 sein")
        if quantity > self.quantity:
            raise ValueError("Nicht genug auf Lager")
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity
        self.set_quantity(self.quantity - quantity)
        return total_price


class NonStockedProduct(Product):
    """A product without stock, for example a software license."""

    def __init__(self, name: str, price: float) -> None:
        """Create a non stocked product with quantity 0."""
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity: int) -> None:
        """Ignore quantity changes because there is no stock."""

    def buy(self, quantity: int) -> float:
        """Buy the quantity without changing stock and return the price."""
        if not self.active:
            raise ValueError("Produkt ist nicht aktiv")
        if quantity <= 0:
            raise ValueError("Menge muss größer als 0 sein")
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity

    def show(self) -> None:
        """Print the product with unlimited quantity."""
        info = f"{self.name}, Price: {self.price}, Quantity: Unlimited"
        if self.promotion:
            info += f", Promotion: {self.promotion.name}"
        print(info)


class LimitedProduct(Product):
    """A product that can only be bought up to a maximum per order."""

    def __init__(self, name: str, price: float, quantity: int,
                 maximum: int) -> None:
        """Create a limited product with a maximum per order."""
        super().__init__(name, price, quantity)
        self.maximum: int = maximum

    def buy(self, quantity: int) -> float:
        """Buy the given quantity if it is not above the maximum."""
        if quantity > self.maximum:
            raise ValueError(f"Nur {self.maximum} mal pro Bestellung erlaubt")
        return super().buy(quantity)

    def show(self) -> None:
        """Print the product with its order limit."""
        info = (f"{self.name}, Price: {self.price}, "
                f"Limited to {self.maximum} per order!")
        if self.promotion:
            info += f", Promotion: {self.promotion.name}"
        print(info)
