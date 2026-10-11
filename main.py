from menu import MenuItem
from restaurant import Restaurant
from cart import UserCart

RESTAURANTS = {
    1: "Coconut Groove",
    2: "Ala Rahi",
    3: "Xanders",
    4: "Meat the Cheese",
}

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

my_restaurant.add_item(MenuItem(101, "Burger", 550))
my_restaurant.add_item(MenuItem(102, "Pizza", 1200))
my_restaurant.add_item(MenuItem(103, "Fries", 250))
my_restaurant.add_item(MenuItem(104, "Drink", 125))

username = input("Enter your name: ")
user_cart = UserCart(username)

print()
my_restaurant.display_menu()
print("Enter any non-numeric key to stop ordering.")

while True:
    user_input = input("What to add in your cart using id: ")
    if not user_input.isdigit():
        print("Thank you for choosing it..")
        break
    selected_item = my_restaurant.get_item(int(user_input))
    if selected_item:
        user_cart.add_to_cart(selected_item)
    else:
        print("Invalid ID! Please try again.")

user_cart.view_cart()
print(f"\nTotal Amount to Pay: Rs. {user_cart.calc_total()}")
print("THANK YOU FOR CHOOSING US :)")