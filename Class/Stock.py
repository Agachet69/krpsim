from Class.Need import Item


class Stock(Item):


    def __repr__(self):
        return f"Stock(name='{self.name}', quantity={self.quantity})"

    def add_stock(self, quantity):
        self.quantity += quantity

    def remove_stock(self, quantity):
        if self.quantity < quantity:
            raise Exception(f"Cannot remove {quantity} from '{self.name}' (left: {self.quantity})")
        self.quantity -= quantity