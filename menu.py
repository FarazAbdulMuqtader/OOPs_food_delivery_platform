import random
class MenuItem:
    def __init__(self, item_id, name, cost):
        self.item_id = item_id 
        self.name = name
        self.cost = cost

    def show_info(self):
        print(f"[{self.item_id}] {self.name} - Rs. {self.cost}")