import copy

class UserCart:
    GST_RATE = 17                             # class attribute
    def __init__(self, username):
        self.username = username
        self.__selected_items = []            # private; AGGREGATION:items exist in the menu too

    def add_to_cart(self, item):
        self.__selected_items.append(item)
        print("Added", item.name, "to the cart")

    def __iadd__(self, item):                 # Dunder method: cart += item
        self.add_to_cart(item)
        return self

    def __len__(self):                        # len(cart)
        return len(self.__selected_items)

    def calc_total(self):
        subtotal = sum(self.__selected_items)  # uses MenuItem.__radd__
        return subtotal * (100 + self.GST_RATE) / 100

    def view_cart(self):
        print(f"{self.username}'s cart")
        if not self.__selected_items:
            print("Cart is empty")
            return
        for item in self.__selected_items:
            item.show_info()                  # POLYMORPHISM: Food and Drink print differently

    def make_receipt(self):
        return copy.deepcopy(self)            # DEEP COPY: independent snapshot

    def clear(self):
        self.__selected_items.clear()