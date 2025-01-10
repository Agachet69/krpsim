from Class.Item import Item


class Stock(Item):
    def __repr__(self):
        return f"Stock(name='{self.name}', quantity={self.quantity})"

    def add(self, quantity):
        self.quantity += quantity

    def remove(self, quantity: int):
        if self.quantity < quantity:
            raise Exception(f"Cannot remove {quantity} from '{self.name}' (left: {self.quantity})")
        self.quantity -= quantity