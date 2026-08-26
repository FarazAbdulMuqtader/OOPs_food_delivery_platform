import menu
import random

class Restaurant:
    def __init__(self,name,restaurant_id=None):
        self.restaurent_id = restaurant_id or random.randint(1000,2000) 
        self.name = name
        self.menu_items = {}

    def add_item(self, item):
        self.menu_items[item.item_id] = item
        return f"Added {item.name} to {self.name}'s menu"

    def get_item(self, item_id):
        if item_id in self.menu_items:
            return self.menu_items[item_id]
        else:
            return None

    def display_menu(self):
        print(f"--- {self.name} Menu ---")
        for item in self.menu_items.values():
            item.show_info()