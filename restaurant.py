import random
from menu import Menu # from menu file import Menu class  

class Restaurant:
    def __init__(self, name, restaurant_id=None):
        self._restaurant_id = restaurant_id or random.randint(1000, 5000)  # protected
        self.name = name
        self.menu = Menu()                    # COMPOSITION: restaurant creates and owns its menu

    def add_item(self, *items):               # *args: Pack items in tuple form
        self.menu.add(*items)                 # Unpack items in tuple form and pass to Menu.add()       
        return f"Added {len(items)} item(s) to {self.name}'s menu"

    def get_item(self, item_id):
        return self.menu.get(item_id)

    def display_menu(self):
        print(f"--- {self.name} Menu ---")
        self.menu.show()
