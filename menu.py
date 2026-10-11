from abc import ABC, abstractmethod


class MenuItem(ABC):                          # ABSTRACTION: can't be created directly
    __slots__ = ("item_id", "name", "_cost")  # __slots__: fixed attributes only

    def __init__(self, item_id, name, cost):
        self.item_id = item_id
        self.name = name
        self.cost = cost                      # goes through the setter below

    @property                                 # ENCAPSULATION: getter
    def cost(self):
        return self._cost

    @cost.setter                              # setter with validation
    def cost(self, value):
        if value < 0:
            raise ValueError("Cost can't be negative")
        self._cost = value

    @abstractmethod
    def show_info(self):                      # every child MUST define this
        ...

    # DUNDER METHODS
    def __eq__(self, other):
        return self.item_id == other.item_id

    def __lt__(self, other):                  # lets sorted() order items by price
        return self.cost < other.cost

    def __radd__(self, other):                # lets sum(items) work
        return other + self.cost


class FoodItem(MenuItem):                     # INHERITANCE (single)
    __slots__ = ()

    def show_info(self):                      # OVERRIDING
        print(f"[{self.item_id}] {self.name} (Food) - Rs. {self.cost}")


class DrinkItem(MenuItem):
    __slots__ = ("size",)

    def __init__(self, item_id, name, cost, size="Regular"):
        super().__init__(item_id, name, cost)  # CONSTRUCTOR CHAINING
        self.size = size

    def show_info(self):
        print(f"[{self.item_id}] {self.name} ({self.size} Drink) - Rs. {self.cost}")


class Menu:
    def __init__(self):
        self.__items = {}                     # private (name mangling)

    def add(self, *items):                    # *args: any number of items
        for item in items:
            self.__items[item.item_id] = item

    def get(self, item_id):
        return self.__items.get(item_id)

    def show(self):
        for item in sorted(self.__items.values()):   # uses __lt__
            item.show_info()