from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from promotions import Promotion


class Product:
    """Repräsentiert ein Produkt mit Name, Preis, Menge, Aktiv-Status und optionaler Promotion."""

    def __init__(self, name: str, price: float, quantity: int) -> None:
        """Legt ein Produkt an und prüft Name, Preis und Menge auf gültige Werte."""
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
        """Gibt die aktuelle Lagermenge zurück."""
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        """Setzt die Menge und deaktiviert das Produkt, wenn sie 0 erreicht."""
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()
        else:
            self.activate()

    def is_active(self) -> bool:
        """Gibt zurück, ob das Produkt aktiv (verfügbar) ist."""
        return self.active

    def activate(self) -> None:
        """Setzt das Produkt auf aktiv."""
        self.active = True

    def deactivate(self) -> None:
        """Setzt das Produkt auf inaktiv."""
        self.active = False

    def get_promotion(self) -> Promotion | None:
        """Gibt die aktuelle Promotion des Produkts zurück (oder None)."""
        return self.promotion

    def set_promotion(self, promotion: Promotion) -> None:
        """Weist dem Produkt eine Promotion zu."""
        self.promotion = promotion

    def show(self) -> None:
        """Gibt Name, Preis, Menge und ggf. Promotion des Produkts aus."""
        info = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        if self.promotion:
            info += f", Promotion: {self.promotion.name}"
        print(info)

    def buy(self, quantity: int) -> float:
        """Kauft die Menge, prüft Aktiv-Status, Menge und Lager, wendet Promotion an und gibt den Preis zurück."""
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
    """Produkt ohne Lagerbestand (z. B. Software-Lizenz), immer verfügbar."""

    def __init__(self, name: str, price: float) -> None:
        """Legt ein nicht-lagerndes Produkt mit Menge 0 an."""
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity: int) -> None:
        """Ignoriert Mengenänderungen, da das Produkt keinen Bestand führt."""
        pass

    def buy(self, quantity: int) -> float:
        """Kauft die Menge ohne Lagerprüfung und gibt den Preis (ggf. mit Promotion) zurück."""
        if not self.active:
            raise ValueError("Produkt ist nicht aktiv")
        if quantity <= 0:
            raise ValueError("Menge muss größer als 0 sein")
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity

    def show(self) -> None:
        """Gibt das Produkt mit unbegrenzter Menge aus."""
        info = f"{self.name}, Price: {self.price}, Quantity: Unlimited"
        if self.promotion:
            info += f", Promotion: {self.promotion.name}"
        print(info)


class LimitedProduct(Product):
    """Produkt mit einer maximalen Kaufmenge pro Bestellung."""

    def __init__(self, name: str, price: float, quantity: int, maximum: int) -> None:
        """Legt ein Produkt mit Maximalmenge pro Bestellung an."""
        super().__init__(name, price, quantity)
        self.maximum: int = maximum

    def buy(self, quantity: int) -> float:
        """Kauft die Menge, sofern das Bestell-Maximum nicht überschritten wird."""
        if quantity > self.maximum:
            raise ValueError(f"Nur {self.maximum} mal pro Bestellung erlaubt")
        return super().buy(quantity)

    def show(self) -> None:
        """Gibt das Produkt mit Hinweis auf das Bestell-Limit aus."""
        info = f"{self.name}, Price: {self.price}, Limited to {self.maximum} per order!"
        if self.promotion:
            info += f", Promotion: {self.promotion.name}"
        print(info)
