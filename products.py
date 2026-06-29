class Product:
    def __init__(self, name, price, quantity):
        if not name:
            raise ValueError("Name darf nicht leer sein")
        if price < 0:
            raise ValueError("Price darf nicht negativ sein")
        if quantity < 0:
            raise ValueError("Quantity darf nicht negativ sein")
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True
        self.promotion = None

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()
        else:
            self.activate()

    def is_active(self):
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def get_promotion(self):
        return self.promotion

    def set_promotion(self, promotion):
        self.promotion = promotion

    def show(self):
        info = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        if self.promotion:
            info += f", Promotion: {self.promotion.name}"
        print(info)

    def buy(self, quantity):
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
    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity):
        pass

    def buy(self, quantity):
        if not self.active:
            raise ValueError("Produkt ist nicht aktiv")
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity

    def show(self):
        info = f"{self.name}, Price: {self.price}, Quantity: Unlimited"
        if self.promotion:
            info += f", Promotion: {self.promotion.name}"
        print(info)


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity):
        if quantity > self.maximum:
            raise ValueError(f"Nur {self.maximum} mal pro Bestellung erlaubt")
        return super().buy(quantity)

    def show(self):
        info = f"{self.name}, Price: {self.price}, Limited to {self.maximum} per order!"
        if self.promotion:
            info += f", Promotion: {self.promotion.name}"
        print(info)
