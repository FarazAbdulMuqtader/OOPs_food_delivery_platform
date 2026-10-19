import io
import tkinter as tk
from contextlib import redirect_stdout
from tkinter import ttk, messagebox
from menu import FoodItem, DrinkItem
from restaurant import Restaurant
from cart import UserCart
from data import build_menu
from orderlog import OrderLog

RESTAURANTS = ["Coconut Groove", "Ala Rahi", "Xanders", "Meat the Cheese",
               "The Burger Lab", "The Pizza Lab", "Aristo", "Perch"]

# ---- theme: orange + black
BLACK = "#0D0D0D"
DARK = "#1C1C1C"
ORANGE = "#FF8C00"
ORANGE_HOVER = "#FFA733"
TEXT = "#F2F2F2"
FONT = ("Helvetica", 11)
FONT_BOLD = ("Helvetica", 11, "bold")


def describe(item):
    """show_info() prints to the console, so capture that text for the GUI."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        item.show_info()
    return buffer.getvalue().strip()


def make_button(parent, text, command):
    """A Label that acts as a button (real tk.Buttons ignore colors on macOS)."""
    btn = tk.Label(parent, text=text, bg=ORANGE, fg=BLACK, font=FONT_BOLD,
                   padx=14, pady=6, cursor="hand2")
    btn.bind("<Button-1>", lambda e: command())
    btn.bind("<Enter>", lambda e: btn.config(bg=ORANGE_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=ORANGE))
    return btn


def make_listbox(parent):
    return tk.Listbox(parent, bg=DARK, fg=TEXT, font=FONT, bd=0, highlightthickness=0,
                      selectbackground=ORANGE, selectforeground=BLACK,
                      activestyle="none", exportselection=False)


def make_panel(parent, title):
    return tk.LabelFrame(parent, text=f" {title} ", bg=BLACK, fg=ORANGE, font=FONT_BOLD,
                         bd=1, relief="solid", highlightbackground=ORANGE)


class FoodApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Food Delivery")
        self.geometry("980x520")
        self.configure(bg=BLACK)
        self.restaurant = None
        self.cart = None
        self.menu_items = []                  # items shown in the menu list
        self.cart_items = []                  # items shown in the cart list (mirrors the cart)
        self.setup_theme()

        tk.Label(self, text="FOOD DELIVERY", bg=BLACK, fg=ORANGE,
                 font=("Helvetica", 20, "bold")).pack(pady=(12, 0))

        # --- top bar: restaurant + name
        top = tk.Frame(self, bg=BLACK)
        top.pack(fill="x", padx=12, pady=10)
        tk.Label(top, text="Restaurant:", bg=BLACK, fg=TEXT, font=FONT).pack(side="left")
        self.combo = ttk.Combobox(top, values=RESTAURANTS, state="readonly", width=18)
        self.combo.current(0)
        self.combo.pack(side="left", padx=5)
        tk.Label(top, text="Your name:", bg=BLACK, fg=TEXT, font=FONT).pack(side="left", padx=(15, 0))
        self.name_var = tk.StringVar()
        tk.Entry(top, textvariable=self.name_var, width=16, bg=DARK, fg=TEXT, font=FONT,
                 insertbackground=ORANGE, bd=0, highlightthickness=1,
                 highlightbackground=ORANGE, highlightcolor=ORANGE_HOVER).pack(side="left", padx=5)
        make_button(top, "Open", self.open_restaurant).pack(side="left", padx=8)
        make_button(top, "History", self.show_history).pack(side="left", padx=(0, 8))

        # --- middle: menu (left) and cart (right)
        mid = tk.Frame(self, bg=BLACK)
        mid.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        left = make_panel(mid, "Menu")
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))
        self.menu_list = make_listbox(left)
        self.menu_list.pack(fill="both", expand=True, padx=8, pady=8)
        make_button(left, "Add to cart", self.add_to_cart).pack(pady=(0, 8))

        right = make_panel(mid, "Cart")
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))
        self.cart_list = make_listbox(right)
        self.cart_list.pack(fill="both", expand=True, padx=8, pady=8)
        self.total_label = tk.Label(right, text="Total: Rs. 0", bg=BLACK, fg=ORANGE, font=FONT_BOLD)
        self.total_label.pack()
        make_button(right, "Checkout", self.checkout).pack(pady=8)

    def setup_theme(self):
        style = ttk.Style(self)
        style.theme_use("clam")               # 'clam' accepts custom colors on every OS
        style.configure("TCombobox", fieldbackground=DARK, background=ORANGE, foreground=TEXT,
                        arrowcolor=BLACK, bordercolor=ORANGE, lightcolor=ORANGE, darkcolor=ORANGE)
        style.map("TCombobox", fieldbackground=[("readonly", DARK)],
                  foreground=[("readonly", TEXT)], selectbackground=[("readonly", DARK)],
                  selectforeground=[("readonly", ORANGE)])
        self.option_add("*TCombobox*Listbox.background", DARK)
        self.option_add("*TCombobox*Listbox.foreground", TEXT)
        self.option_add("*TCombobox*Listbox.selectBackground", ORANGE)
        self.option_add("*TCombobox*Listbox.selectForeground", BLACK)

    def open_restaurant(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing name", "Please enter your name first.")
            return
        restaurant_name = self.combo.get()
        self.menu_items = build_menu(restaurant_name)         # each restaurant has its own menu
        self.restaurant = Restaurant(restaurant_name)
        self.restaurant.add_item(*self.menu_items)
        self.cart = UserCart(name)
        self.cart_items = []
        self.menu_items.sort(key=lambda item: item.item_id)   # ID order, same as the console menu
        # For cheapest-first instead, use: self.menu_items.sort()   (uses MenuItem.__lt__)
        self.menu_list.delete(0, tk.END)
        for item in self.menu_items:
            self.menu_list.insert(tk.END, describe(item))
        self.refresh_cart()

    def ask_size(self, item):
        """Themed popup that lets the customer pick a cup size. Returns the sized
        DrinkItem, or None if the popup was cancelled."""
        result = {"item": None}
        win = tk.Toplevel(self)
        win.title("Choose size")
        win.configure(bg=BLACK, padx=24, pady=18)
        win.transient(self)

        tk.Label(win, text=f"Choose a cup size for {item.name}", bg=BLACK, fg=ORANGE,
                 font=("Helvetica", 13, "bold")).pack(pady=(0, 10))

        def pick(size):
            result["item"] = item.with_size(size)
            win.destroy()

        for size, price in item.sizes.items():
            make_button(win, f"{size}  -  Rs. {price}",
                        lambda s=size: pick(s)).pack(fill="x", pady=4)
        make_button(win, "Cancel", win.destroy).pack(fill="x", pady=(12, 0))

        win.wait_visibility()
        win.grab_set()                        # block the main window until a size is picked
        self.wait_window(win)
        return result["item"]

    def add_to_cart(self):
        if self.cart is None:
            messagebox.showwarning("No restaurant", "Click Open first.")
            return
        selected = self.menu_list.curselection()
        if not selected:
            messagebox.showinfo("Pick an item", "Select an item from the menu.")
            return
        item = self.restaurant.get_item(self.menu_items[selected[0]].item_id)
        if isinstance(item, DrinkItem):       # only drinks ask for a cup size
            item = self.ask_size(item)
            if item is None:                  # popup cancelled
                return
        self.cart += item                     # __iadd__ from UserCart
        self.cart_items.append(item)
        self.refresh_cart()

    def refresh_cart(self):
        self.cart_list.delete(0, tk.END)
        for item in self.cart_items:
            self.cart_list.insert(tk.END, describe(item))
        self.total_label.config(text=f"Total (incl. 17% GST): Rs. {self.cart.calc_total():.2f}")

    def checkout(self):
        if self.cart is None or len(self.cart) == 0:
            messagebox.showinfo("Empty cart", "Add something first.")
            return
        order_id = OrderLog().save(self.restaurant.name, self.cart)   # record in orders.csv
        receipt = self.cart.make_receipt()    # deep copy, then clear the cart
        lines = [describe(item) for item in self.cart_items]
        text = (f"Order #{order_id} - {self.restaurant.name}\n\n" + "\n".join(lines)
                + f"\n\nTotal: Rs. {receipt.calc_total():.2f}")
        self.cart.clear()
        self.cart_items = []
        self.refresh_cart()
        self.show_receipt(receipt.username, text)

    def show_receipt(self, username, text):
        win = tk.Toplevel(self)               # themed popup (native message boxes can't be colored)
        win.title("Receipt")
        win.configure(bg=BLACK, padx=24, pady=18)
        tk.Label(win, text=f"Receipt for {username}", bg=BLACK, fg=ORANGE,
                 font=("Helvetica", 14, "bold")).pack(pady=(0, 10))
        tk.Label(win, text=text, bg=BLACK, fg=TEXT, font=FONT, justify="left").pack()
        make_button(win, "Close", win.destroy).pack(pady=(14, 0))

    def show_history(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing name", "Enter your name to see your orders.")
            return
        orders = OrderLog().orders_for(name)
        if not orders:
            messagebox.showinfo("No orders", f"No orders found for {name}.")
            return

        win = tk.Toplevel(self)
        win.title("Order history")
        win.configure(bg=BLACK, padx=24, pady=18)
        tk.Label(win, text=f"Order history of {name}", bg=BLACK, fg=ORANGE,
                 font=("Helvetica", 14, "bold")).pack(pady=(0, 10))

        box = tk.Text(win, width=48, height=18, bg=DARK, fg=TEXT, font=FONT,
                      bd=0, highlightthickness=0, wrap="word")
        box.pack()
        for order in reversed(orders):        # newest first
            box.insert(tk.END, f"Order #{order['order_id']} - {order['restaurant']}\n")
            box.insert(tk.END, f"{order['timestamp']}\n")
            for item in order["items"]:
                size = f" ({item['size']})" if item["size"] else ""
                box.insert(tk.END, f"   {item['name']}{size} - Rs. {item['price']:.0f}\n")
            box.insert(tk.END, f"   Total: Rs. {order['total']:.2f}\n\n")
        box.config(state="disabled")          # read-only
        make_button(win, "Close", win.destroy).pack(pady=(14, 0))


if __name__ == "__main__":
    FoodApp().mainloop()
