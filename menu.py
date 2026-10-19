from abc import ABC, abstractmethod

class MenuItem(ABC):                          # ABSTRACTION: can't be created directly
    __slots__ = ("item_id", "name", "_cost")  # __slots__: fixed attributes only

    def __init__(self, item_id, name, cost):
        self.item_id = item_id
        self.name = name
        self._cost = cost                    

    @property                                 # Encapsulation: getter
    def cost(self):
        return self._cost

    @cost.setter                              # Encapsulation: setter 
    def cost(self, value):
        if value < 0:
            print("Cost cannot be negative. Setting to 0")
            value = 0   
        self._cost = value

    @abstractmethod
    def show_info(self):
        pass            

    # DUNDER METHODS
    def __eq__(self, other):                   # lets == compare items by item_id
        return self.item_id == other.item_id

    def __lt__(self, other):                  # lets sorted() order items by price
        return self.cost < other.cost

    def __radd__(self, other):                # lets right side order sum(items) work
        return other + self.cost


class FoodItem(MenuItem):                       # Inheritance(single)
    __slots__ = ()                             

    def show_info(self):                        # Overriding
        print(f"[{self.item_id}] {self.name} - Rs. {self.cost}")


class DrinkItem(MenuItem):                      # Inheritance(Single)
    __slots__ = ("sizes", "chosen_size")

    def __init__(self, item_id, name, cost, sizes):
        super().__init__(item_id, name, cost) 
        self.sizes = sizes                      
        self.chosen_size = None

    def with_size(self, size):
        #Return new DrinkItem with chosen cup size and its price.
                                                # reflects the available sizes in a list
        chosen = DrinkItem(self.item_id, self.name, self.sizes[size], self.sizes)
        chosen.chosen_size = size
        return chosen

    def show_info(self):                        # Overriding
        if self.chosen_size:                    # in the cart
            print(f"[{self.item_id}] {self.name} ({self.chosen_size}) - Rs. {self.cost}")
        else:
            '''self.sizes: the dictionary, e.g. {"Small": 100, "Large": 200}.
            .items(): gives it as pairs: ("Small", 100), ("Large", 200).
            for s, p in ...: loop through the pairs. s is the size, p is the price.
            f"{s} Rs. {p}": build text for each pair: "Small Rs. 100", "Large Rs. 200".
            ", ".join(...): glue all the texts together with a comma and space between them: "Small Rs. 100, Large Rs. 200".
            options =: save that final text in a box called options.'''
            options = ", ".join(f"{s} Rs. {p}" for s, p in self.sizes.items())
            print(f"[{self.item_id}] {self.name} - {options}")

class Menu:
    def __init__(self):
        self.__items = {}                     # private (name mangling),dict

    def add(self, *items):                 
        for item in items:
            self.__items[item.item_id] = item

    def get(self, item_id):                   #get item by id
        return self.__items.get(item_id)

    def show(self):
        for item in sorted(self.__items.values(), key=lambda item: item.item_id):
            item.show_info()
    '''.values(): Grab only the items and ignore the ID labels'''
