# from Class.Need import Item


# class Stock(Item):
class Stock:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, name: str, quantity: int):
        if name in self.stocks:
            self.stocks[name]['quantity'] += quantity
        else:
            self.stocks[name] = {'quantity': quantity}

    def remove_stock(self, name: str):
        if name in self.stocks:
            del self.stocks[name]

    def __repr__(self):
        return "\n".join(
            [f"{name}:  Quantity={details['quantity']}" for name, details in self.stocks.items()]
        )


#     def __repr__(self):
#         return f"Stock(name='{self.name}', quantity={self.quantity})"

#     def add_stock(self, quantity):
#         self.quantity += quantity

#     def remove_stock(self, quantity):
#         if self.quantity < quantity:
#             raise Exception(f"Cannot remove {quantity} from '{self.name}' (left: {self.quantity})")
#         self.quantity -= quantity