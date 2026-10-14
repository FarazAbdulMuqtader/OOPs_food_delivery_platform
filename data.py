from menu import FoodItem, DrinkItem

# Each restaurant has its own list of items.
# Food row:  ("food",  item_id, name, price)
# Drink row: ("drink", item_id, name, price, {size: price, ...})
MENUS = {
    "Coconut Groove": [
        ("food", 101, "Grilled Chicken", 950),
        ("food", 102, "Beef Steak", 1800),
        ("food", 103, "Fish and Chips", 1100),
        ("food", 104, "Caesar Salad", 600),
        ("food", 105, "Coconut Cake", 450),
        ("drink", 106, "Fresh Lime", 200, {"Small": 200, "Medium": 250, "Large": 300}),
        ("drink", 107, "Coconut Water", 300, {"Small": 300, "Medium": 380, "Large": 450}),
    ],
    "Ala Rahi": [
        ("food", 101, "Chicken Karahi", 1500),
        ("food", 102, "Mutton Biryani", 1100),
        ("food", 103, "Seekh Kebab", 700),
        ("food", 104, "Naan", 60),
        ("food", 105, "Kheer", 300),
        ("drink", 106, "Lassi", 200, {"Small": 200, "Medium": 260, "Large": 320}),
        ("drink", 107, "Doodh Patti Chai", 120, {"Small": 120, "Medium": 160, "Large": 200}),
    ],
    "Xanders": [
        ("food", 101, "Club Sandwich", 750),
        ("food", 102, "Chicken Wrap", 650),
        ("food", 103, "Loaded Fries", 450),
        ("food", 104, "Brownie", 350),
        ("drink", 105, "Cold Coffee", 400, {"Small": 400, "Medium": 480, "Large": 550}),
        ("drink", 106, "Iced Tea", 300, {"Small": 300, "Medium": 370, "Large": 430}),
    ],
    "Meat the Cheese": [
        ("food", 101, "Cheese Steak Sandwich", 1000),
        ("food", 102, "Cheesy Fries", 500),
        ("food", 103, "Mac and Cheese", 850),
        ("food", 104, "Chicken Quesadilla", 900),
        ("food", 105, "Cheesecake", 500),
        ("drink", 106, "Milkshake", 450, {"Small": 450, "Medium": 550, "Large": 650}),
    ],
    "The Burger Lab": [
        ("food", 101, "Classic Burger", 550),
        ("food", 102, "Cheese Burger", 650),
        ("food", 103, "Double Patty Burger", 900),
        ("food", 104, "Fries", 250),
        ("food", 105, "Chicken Nuggets", 400),
        ("food", 106, "Ice Cream", 300),
        ("drink", 107, "Soda", 120, {"Small": 120, "Medium": 150, "Large": 180}),
        ("drink", 108, "Mocktails", 350, {"Small": 350, "Medium": 430, "Large": 500}),
    ],
    "The Pizza Lab": [
        ("food", 101, "Margherita Pizza", 1100),
        ("food", 102, "Pepperoni Pizza", 1400),
        ("food", 103, "Fajita Pizza", 1500),
        ("food", 104, "Garlic Bread", 350),
        ("food", 105, "Pasta", 800),
        ("drink", 106, "Soda", 120, {"Small": 120, "Medium": 150, "Large": 180}),
        ("drink", 107, "Mint Margarita", 300, {"Small": 300, "Medium": 380, "Large": 450}),
    ],
    "Aristo": [
        ("food", 101, "Chicken Tikka", 800),
        ("food", 102, "Malai Boti", 850),
        ("food", 103, "Chicken Roll", 450),
        ("food", 104, "Fries", 250),
        ("food", 105, "Gulab Jamun", 250),
        ("drink", 106, "Soda", 120, {"Small": 120, "Medium": 150, "Large": 180}),
        ("drink", 107, "Rooh Afza", 150, {"Small": 150, "Medium": 200, "Large": 250}),
    ],
    "Perch": [
        ("food", 101, "Pancakes", 700),
        ("food", 102, "Eggs Benedict", 900),
        ("food", 103, "Avocado Toast", 800),
        ("food", 104, "Pasta Alfredo", 950),
        ("food", 105, "Tiramisu", 550),
        ("drink", 106, "Latte", 450, {"Small": 450, "Medium": 520, "Large": 590}),
        ("drink", 107, "Hot Chocolate", 400, {"Small": 400, "Medium": 470, "Large": 540}),
    ],
}


def build_menu(restaurant_name):
    """Turn the data rows for one restaurant into FoodItem / DrinkItem objects."""
    items = []
    for row in MENUS[restaurant_name]:
        if row[0] == "food":
            kind, item_id, name, cost = row
            items.append(FoodItem(item_id, name, cost))
        else:
            kind, item_id, name, cost, sizes = row
            items.append(DrinkItem(item_id, name, cost, sizes))
    return items