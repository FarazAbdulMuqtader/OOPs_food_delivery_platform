import menu as m
import restaurant as rs
import cart as c

print("Restaurants available:")
print("Option 1 is Coconut Groove")
print("Option 2 is Ala Rahi")
print("Option 3 is Xanders")
print("Option 5 is Meat the Cheese")
op=int(input("Which Restaurant would u like to pick"))

if op==1:
    restaurant_name="Coconut Groove"
elif op==2:
    restaurant_name="Ala Rahi"
elif op==3:
    restaurant_name="Xanders"
elif op==4:
    restaurant_name="Meat the Cheeese"
else:
    print("Not in the list")
   
my_restaurant = rs.Restaurant(restaurant_name)
print("Wellcome to ",restaurant_name)
print("=============================")
print()

item1 = m.MenuItem(101, "Burger", 550)
item2 = m.MenuItem(102, "Pizza", 1200)
item3 = m.MenuItem(103, "Fries", 250)
item4 = m.MenuItem(104,"Drink",125)

my_restaurant.add_item(item1)
my_restaurant.add_item(item2)
my_restaurant.add_item(item3)
my_restaurant.add_item(item4)

username = input("Enter your name: ")
user_cart = c.UserCart(username)

print("\n--- MENU ---")
print("Choose Burger-550 using id 101")
print("Choose Pizza-1200 using id 102")
print("Choose Fries-250 using id 103")
print("Choose Drink-125 using id 105")
print("Enter any other key to stop ordering.")

while True:
    user_input = input("What to add in your cart using id: ")

    if user_input.isdigit():
        ch = int(user_input)  # Convert str into int
    else:
        print("Thank you for choosing it..")
        break

    selected_item = my_restaurant.get_item(ch)

    if selected_item:
        user_cart.add_to_cart(selected_item)
    else:
        print("Invalid ID! Please try again.")

user_cart.view_cart()
total = user_cart.calc_total()
print(f"Total Amount to Pay after 17% Tax : Rs. {total}")
print("THANK YOU FOR CHOOSING US:)")my_restaurant.add_item(item4)

# 2. Setup User Cart
username = input("Enter your name: ")
user_cart = c.UserCart(username)

# 3. Display Menu to User
print("\n--- MENU ---")
print("Choose Burger-550 using id 101")
print("Choose Pizza-1200 using id 102")
print("Choose Fries-250 using id 103")
print("Choose Drink-125 using id 105")
print("Enter any other key to stop ordering.")

while True:
    user_input = input("What to add in your cart using id: ")

    if user_input.isdigit():
        ch = int(user_input)  # Convert str into int
    else:
        print("Thank you for choosing it..")
        break

    selected_item = my_restaurant.get_item(ch)

    if selected_item:
        user_cart.add_to_cart(selected_item)
    else:
        print("Invalid ID! Please try again.")

user_cart.view_cart()
total = user_cart.calc_total()
print(f"\nTotal Amount to Pay: Rs. {total}")
print("THANK YOU FOR CHOOSING US:) ")
