import csv
import os
from datetime import datetime


class OrderLog:
    """Keeps a record of every order in a plain CSV file (one row per item)."""

    FIELDS = ["order_id", "timestamp", "customer", "restaurant",
              "item_id", "item_name", "size", "price", "order_total"]

    def __init__(self, path=None):
        # by default, orders.csv is created next to this script
        if path is None:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders.csv")
        self.path = path

    def next_order_id(self):
        """Read the last order id from the file and add 1 (starts at 1001)."""
        if not os.path.exists(self.path):
            return 1001
        with open(self.path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            return 1001
        return int(rows[-1]["order_id"]) + 1

    def save(self, restaurant_name, cart):
        """Append the cart as one order. Returns the new order id."""
        order_id = self.next_order_id()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = round(cart.calc_total(), 2)
        new_file = not os.path.exists(self.path)

        with open(self.path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDS)
            if new_file:
                writer.writeheader()          # header only once, when the file is created
            for item in cart.items:
                writer.writerow({
                    "order_id": order_id,
                    "timestamp": timestamp,
                    "customer": cart.username,
                    "restaurant": restaurant_name,
                    "item_id": item.item_id,
                    "item_name": item.name,
                    "size": getattr(item, "chosen_size", "") or "",   # FoodItem has no size
                    "price": item.cost,
                    "order_total": total,
                })
        return order_id

    def load_all(self):
        """Read the CSV back and group the rows into orders (oldest first)."""
        if not os.path.exists(self.path):
            return []
        orders = {}                           # order_id -> order dict
        with open(self.path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                order_id = int(row["order_id"])          # CSV gives strings, convert
                if order_id not in orders:               # first row of this order
                    orders[order_id] = {
                        "order_id": order_id,
                        "timestamp": row["timestamp"],
                        "customer": row["customer"],
                        "restaurant": row["restaurant"],
                        "total": float(row["order_total"]),
                        "items": [],
                    }
                orders[order_id]["items"].append({
                    "name": row["item_name"],
                    "size": row["size"],
                    "price": float(row["price"]),
                })
        return list(orders.values())

    def orders_for(self, username):
        """Only the orders placed by this customer (case-insensitive)."""
        return [o for o in self.load_all()
                if o["customer"].lower() == username.strip().lower()]
