from dataclasses import dataclass

@dataclass
class CartItem:
    product_id:int
    quantity: int

    def increase_quantity(self, amount: int):
        self.quantity += amount

    def decrease_quantity(self, amount: int):
        self.quantity -= amount