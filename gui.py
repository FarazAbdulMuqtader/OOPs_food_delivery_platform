"""
Food Delivery Platform - Tkinter GUI

This replaces the console-based main.py with a graphical interface.
menu.py, restaurant.py, and cart.py are untouched - all the original
OOP logic (MenuItem, Restaurant, UserCart) is reused as-is.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import menu as m
import restaurant as rs
import cart as c

RESTAURANT_NAMES = ["Coconut Groove", "Ala Rahi", "Xanders", "Meat the Cheese"]

# Same menu items every restaurant gets, matching the original main.py
DEFAULT_MENU = [
    (101, "Burger", 550),
    (102, "Pizza", 1200),
    (103, "Fries", 250),
    (104, "Drink", 125),
]


def build_restaurant(name: str) -> rs.Restaurant:
    restaurant = rs.Restaurant(name)
    for item_id, item_name, cost in DEFAULT_MENU:
        restaurant.add_item(m.MenuItem(item_id, item_name, cost))
    return restaurant


class FoodDeliveryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Food Delivery Platform")
        self.geometry("620x480")
        self.resizable(False, False)
        self.configure(bg="#E0E84A")

        self.restaurant = None
        self.user_cart = None

        self._build_setup_screen()

    # ---------- Screen 1: pick restaurant + name ----------
    def _build_setup_screen(self):
        self.setup_frame = tk.Frame(self, bg="#4B1B1B", padx=30, pady=30)
        self.setup_frame.pack(expand=True, fill="both")

        tk.Label(
            self.setup_frame, text="Welcome to the Food Delivery Platform",
            font=("Helvetica", 16, "bold"), bg="#121111"
        ).pack(pady=(0, 20))

        tk.Label(self.setup_frame, text="Enter your name:", bg="#0f0e0e",
                 font=("Helvetica", 11)).pack(anchor="w")
        self.name_entry = tk.Entry(self.setup_frame, font=("Helvetica", 11))
        self.name_entry.pack(fill="x", pady=(0, 15))

        tk.Label(self.setup_frame, text="Choose a restaurant:", bg="#290f0f",
                 font=("Helvetica", 11)).pack(anchor="w")
        self.restaurant_choice = ttk.Combobox(
            self.setup_frame, values=RESTAURANT_NAMES, state="readonly",
            font=("Helvetica", 11)
        )
        self.restaurant_choice.current(0)
        self.restaurant_choice.pack(fill="x", pady=(0, 25))

        tk.Button(
            self.setup_frame, text="Start Order", font=("Helvetica", 11, "bold"),
            bg="#2e8b57", fg="black", command=self._start_order
        ).pack(fill="x", ipady=6)

    def _start_order(self):
        username = self.name_entry.get().strip()
        if not username:
            messagebox.showwarning("Name required", "Please enter your name to continue.")
            return

        restaurant_name = self.restaurant_choice.get()
        self.restaurant = build_restaurant(restaurant_name)
        self.user_cart = c.UserCart(username)

        self.setup_frame.destroy()
        self._build_order_screen()

    # ---------- Screen 2: menu + cart ----------
    def _build_order_screen(self):
        header = tk.Frame(self, bg="#2e8b57", pady=12)
        header.pack(fill="x")
        tk.Label(
            header, text=f"{self.restaurant.name}  •  {self.user_cart.username}'s order",
            font=("Helvetica", 13, "bold"), bg="#2e8b57", fg="black"
        ).pack()

        body = tk.Frame(self, bg="#131111", padx=15, pady=15)
        body.pack(expand=True, fill="both")

        # Left: menu
        menu_frame = tk.LabelFrame(body, text="Menu", font=("Helvetica", 11, "bold"),
                                    bg="#070707", padx=10, pady=10)
        menu_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        for item in self.restaurant.menu_items.values():
            row = tk.Frame(menu_frame, bg="#151313")
            row.pack(fill="x", pady=4)
            tk.Label(row, text=f"{item.name} - Rs. {item.cost}",
                     font=("Helvetica", 10), bg="#343232", anchor="w").pack(side="left")
            tk.Button(
                row, text="Add to Cart", bg="#4a90d9", fg="black",
                command=lambda i=item: self._add_to_cart(i)
            ).pack(side="right")

        # Right: cart
        cart_frame = tk.LabelFrame(body, text="Your Cart", font=("Helvetica", 11, "bold"),
                                    bg="#0e0c0c", padx=10, pady=10)
        cart_frame.pack(side="right", fill="both", expand=True)

        self.cart_listbox = tk.Listbox(cart_frame, font=("Helvetica", 10), height=12)
        self.cart_listbox.pack(fill="both", expand=True)

        self.total_label = tk.Label(
            cart_frame, text="Total (incl. 17% GST): Rs. 0.00",
            font=("Helvetica", 11, "bold"), bg="#050505", anchor="w"
        )
        self.total_label.pack(fill="x", pady=(10, 10))

        tk.Button(
            cart_frame, text="Checkout", bg="#2e8b57", fg="black",
            font=("Helvetica", 10, "bold"), command=self._checkout
        ).pack(fill="x", ipady=5)

    def _add_to_cart(self, item):
        self.user_cart.add_to_cart(item)
        self._refresh_cart()

    def _refresh_cart(self):
        self.cart_listbox.delete(0, tk.END)
        for item in self.user_cart.selected_items:
            self.cart_listbox.insert(tk.END, f"{item.name} - Rs. {item.cost}")
        total = self.user_cart.calc_total()
        self.total_label.config(text=f"Total (incl. 17% GST): Rs. {total:.2f}")

    def _checkout(self):
        if not self.user_cart.selected_items:
            messagebox.showinfo("Cart is empty", "Add at least one item before checking out.")
            return
        total = self.user_cart.calc_total()
        messagebox.showinfo(
            "Order placed",
            f"Thank you, {self.user_cart.username}!\n\n"
            f"Total amount to pay: Rs. {total:.2f}\n\nTHANK YOU FOR CHOOSING US :)"
        )


if __name__ == "__main__":
    app = FoodDeliveryApp()
    app.mainloop()