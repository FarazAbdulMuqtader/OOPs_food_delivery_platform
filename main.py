from menu import FoodItem, DrinkItem
from restaurant import Restaurant
from cart import UserCart
from data import build_menu
from orderlog import OrderLog

RESTAURANTS = {1: "Coconut Groove", 2: "Ala Rahi", 3: "Xanders", 4: "Meat the Cheese", 5: "The Burger Lab", 6: "The Pizza Lab", 7: "Aristo", 8: "Perch"}

print("Restaurants available:")
for number, name in RESTAURANTS.items():
    print(f"Option {number} is {name}")

while True:
    choice = input("Which restaurant would you like to pick? ")
    if choice.isdigit() and int(choice) in RESTAURANTS:
        restaurant_name = RESTAURANTS[int(choice)]
        break
    print("Not in the list, try again.")

my_restaurant = Restaurant(restaurant_name)
print("Welcome to", restaurant_name)
print("=============================")

my_restaurant.add_item(*build_menu(restaurant_name))   # each restaurant gets its own menu

username = input("Enter your name: ")
user_cart = UserCart(username)

print()
my_restaurant.display_menu()
print("Enter any non-numeric key to stop ordering.")

def ask_size(item):
    while True:
        choice = input(f"Choose size for {item.name} ({'/'.join(item.sizes)}): ").strip().title()
        if choice in item.sizes:
            return item.with_size(choice)
        print("Invalid size, try again.")

while True:
    user_input = input("What to add in your cart using id: ")
    if not user_input.isdigit():
        print("Thank you for choosing it..")
        break
    selected_item = my_restaurant.get_item(int(user_input))
    if selected_item:
        if isinstance(selected_item, DrinkItem):   # only drinks ask for a cup size
            selected_item = ask_size(selected_item)
        user_cart += selected_item
    else:
        print("Invalid ID! Please try again.")

print(f"\nItems in cart: {len(user_cart)}")
user_cart.view_cart()
print(f"\nTotal Amount to Pay: Rs. {user_cart.calc_total()}")

if len(user_cart) > 0:                        # record the order in orders.csv
    order_id = OrderLog().save(restaurant_name, user_cart)
    print(f"Order #{order_id} saved to orders.csv")

receipt = user_cart.make_receipt()            # copy first, then empty the cart
user_cart.clear()
print(f"\nCart after checkout: {len(user_cart)} | Receipt still has: {len(receipt)}")
print("THANK YOU FOR CHOOSING US :)")
