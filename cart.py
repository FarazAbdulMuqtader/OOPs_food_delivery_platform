import menu as m
import restaurant as rs
class UserCart:
    def __init__(self,username):
        self.username=username
        self.selected_items=[]

    def add_to_cart(self,selected_items):
        self.selected_items.append(selected_items)
        print("Added",selected_items.name,"to the cart")

    def calc_total(self):
        # loop selected items and return final cost
        total_cost=0
        total_cost_gst=0
        for items in self.selected_items:
           total_cost+=items.cost
           total_cost_gst=total_cost*117/100
        return total_cost_gst

    def view_cart(self):
        print(self.username," cart")

        if not self.selected_items:
            print("Cart is empty")
            return
        for items in self.selected_items:
            items.show_info()
