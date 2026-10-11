import random
from menu import Menu


class Restaurant:
    def __init__(self, name, restaurant_id=None):
        self._restaurant_id = restaurant_id or random.randint(1000, 2000)  # protected
        self.name = name
        self.menu = Menu()                    # COMPOSITION: restaurant creates and owns its menu

    def add_item(self, *items):
        self.menu.add(*items)
        return f"Added {len(items)} item(s) to {self.name}'s menu"

    def get_item(self, item_id):
        return self.menu.get(item_id)

    def display_menu(self):
        print(f"--- {self.name} Menu ---")
        self.menu.show()