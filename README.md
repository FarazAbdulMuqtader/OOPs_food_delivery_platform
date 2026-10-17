# OOPs Food Delivery Platform

A food ordering system in Python, built to apply core object-oriented programming principles over a real-world workflow: pick a restaurant, browse its menu, build a cart, check out, and keep a history of past orders. It runs as a console app (`main.py`) or as a themed Tkinter GUI (`gui.py`).

## Overview

The project simulates a full ordering session end to end: restaurant selection (8 restaurants, each with its own menu), menu display, item lookup by ID, drink size selection, cart management, 17% GST calculation, receipt generation, and order logging to `orders.csv`. Everything is built with a class-based structure instead of a flat script.

## Structure

| File            | Responsibility                                                                                  |
| --------------- | ----------------------------------------------------------------------------------------------- |
| `main.py`       | Console entry point: drives the ordering flow and user I/O                                      |
| `gui.py`        | Tkinter GUI (`FoodApp`, orange and black theme): menu, cart, checkout, receipt, order history   |
| `menu.py`       | `MenuItem` (abstract), `FoodItem`, `DrinkItem`, and `Menu`                                      |
| `restaurant.py` | `Restaurant` class: owns a `Menu` and delegates item lookup to it                               |
| `cart.py`       | `UserCart` class: selected items, GST total, deep-copied receipt                                |
| `orderlog.py`   | `OrderLog` class: saves and reads orders in `orders.csv`                                        |
| `data.py`       | Menu data for all restaurants and the `build_menu()` factory                                    |
| `orders.csv`    | Order history, one row per item                                                                 |

## UML Class Diagram

Each box lists attributes and methods. The red notes mark the OOP concept used in that class.

```mermaid
%%{init: {'theme':'base','themeVariables': {'noteBkgColor':'#FCEBEB','noteTextColor':'#A32D2D','noteBorderColor':'#E24B4A'}}}%%
classDiagram
direction TB

class MenuItem {
  <<abstract>>
  +item_id
  +name
  #_cost
  +cost : property
  +__init__(item_id, name, cost)
  +show_info()*
  +__eq__(other)
  +__lt__(other)
  +__radd__(other)
}
class FoodItem {
  +show_info()
}
class DrinkItem {
  +sizes : dict
  +chosen_size : str
  +with_size(size) DrinkItem
  +show_info()
}
class Menu {
  -__items : dict
  +add(*items)
  +get(item_id)
  +show()
}
class Restaurant {
  #_restaurant_id : int
  +name : str
  +menu : Menu
  +add_item(*items)
  +get_item(item_id)
  +display_menu()
}
class UserCart {
  +GST_RATE : int$
  +username : str
  -__selected_items : list
  +items : property
  +add_to_cart(item)
  +__iadd__(item)
  +__len__()
  +calc_total()
  +view_cart()
  +make_receipt()
  +clear()
}
class OrderLog {
  +FIELDS : list$
  +path : str
  +next_order_id()
  +save(restaurant_name, cart)
  +load_all()
  +orders_for(username)
}
class data["data.py"] {
  <<module>>
  +MENUS : dict
  +build_menu(restaurant_name)
}
class Tk["tk.Tk"]
class FoodApp {
  +restaurant : Restaurant
  +cart : UserCart
  +menu_items : list
  +cart_items : list
  +setup_theme()
  +open_restaurant()
  +ask_size(item)
  +add_to_cart()
  +refresh_cart()
  +checkout()
  +show_receipt(username, text)
  +show_history()
}
class main["main.py"] {
  <<script>>
  +RESTAURANTS : dict
  +ask_size(item)
}

MenuItem <|-- FoodItem : inheritance
MenuItem <|-- DrinkItem : inheritance
Menu o-- MenuItem : aggregation
UserCart o-- MenuItem : aggregation
Restaurant *-- Menu : composition
OrderLog ..> UserCart : uses
data ..> FoodItem : creates
data ..> DrinkItem : creates
Tk <|-- FoodApp : inheritance
FoodApp --> Restaurant : association
FoodApp --> UserCart : association
FoodApp ..> OrderLog : uses
FoodApp ..> data : uses
main --> Restaurant : association
main --> UserCart : association
main ..> OrderLog : uses
main ..> data : uses

note for MenuItem "ABSTRACTION: ABC + @abstractmethod\nENCAPSULATION: @property + setter\nOPERATOR OVERLOADING: dunder methods\n__slots__: fixed attributes"
note for FoodItem "INHERITANCE: single (MenuItem)\nPOLYMORPHISM: overrides show_info()"
note for DrinkItem "INHERITANCE: single (MenuItem)\nPOLYMORPHISM: overrides show_info()\nsuper().__init__(), with_size() returns a new object"
note for Menu "ENCAPSULATION: private __items (name mangling)\nAGGREGATION: holds MenuItem objects\n*args + lambda sort key"
note for Restaurant "COMPOSITION: creates and owns its Menu\nENCAPSULATION: protected _restaurant_id\n*args packing / unpacking, DELEGATION to Menu"
note for UserCart "AGGREGATION: items also live in Menu\nENCAPSULATION: private list + read-only property\nDEEP COPY: make_receipt() snapshot\nDUNDER: __iadd__, __len__, sum()\nCLASS ATTRIBUTE: GST_RATE"
note for OrderLog "DEPENDENCY: uses UserCart as a parameter\nCLASS ATTRIBUTE: FIELDS\nSINGLE RESPONSIBILITY: CSV storage"
note for data "FACTORY: tuple rows become objects\nDEPENDENCY: creates FoodItem / DrinkItem"
note for FoodApp "INHERITANCE: extends tk.Tk\nASSOCIATION: has Restaurant + UserCart\nPOLYMORPHISM: describe() calls show_info()\nisinstance() check for DrinkItem, lambda callbacks"
note for main "isinstance() check for DrinkItem\nuser_cart += item (__iadd__)\nmake_receipt() deep copy, then clear()"
```

## File Relationships

How the files link to each other, and which kind of relationship each link is.

```mermaid
flowchart TB
  main["main.py<br/>console app"]
  gui["gui.py<br/>FoodApp extends tk.Tk"]
  data["data.py"]
  restaurant["restaurant.py"]
  cart["cart.py"]
  orderlog["orderlog.py"]
  menu["menu.py<br/>MenuItem, FoodItem, DrinkItem, Menu"]

  main -->|imports all four| data & restaurant & cart & orderlog
  gui -->|imports all four| data & restaurant & cart & orderlog
  orderlog -. "uses (dependency)" .-> cart
  data -. "dependency: creates Food + Drink" .-> menu
  restaurant == "composition: owns Menu" ==> menu
  cart -- "aggregation: holds MenuItems" --> menu
```

| Link                         | Type        | Why                                                              |
| ---------------------------- | ----------- | ---------------------------------------------------------------- |
| `FoodItem`, `DrinkItem` to `MenuItem` | Inheritance | Both extend the abstract base class                      |
| `Restaurant` to `Menu`       | Composition | The restaurant creates its own menu, so the menu lives and dies with it |
| `Menu` to `MenuItem`         | Aggregation | The menu holds items that are created elsewhere                  |
| `UserCart` to `MenuItem`     | Aggregation | Cart items also exist in the menu                                |
| `OrderLog` to `UserCart`     | Dependency  | Receives the cart as a parameter, never stores it                |
| `data.py` to `FoodItem`, `DrinkItem` | Dependency | `build_menu()` creates the objects                       |
| `FoodApp` to `tk.Tk`         | Inheritance | The GUI window is a Tkinter window                               |

## OOP Concepts Practiced

- **Abstraction:** `MenuItem` is an abstract base class (`ABC`, `@abstractmethod`) and cannot be created directly.
- **Encapsulation:** `@property` with a validating setter for `cost`, a private `__items` dict in `Menu`, a private cart list exposed through a read-only property.
- **Inheritance:** single inheritance from `MenuItem` into `FoodItem` and `DrinkItem`, and `FoodApp` extending `tk.Tk`.
- **Polymorphism:** `show_info()` is overridden, so food and drinks print differently through the same call.
- **Composition and aggregation:** `Restaurant` owns its `Menu`; `Menu` and `UserCart` hold `MenuItem` objects they did not create.
- **Operator overloading:** `__eq__`, `__lt__`, `__radd__` (so `sum(items)` works), `__iadd__` (`cart += item`), `__len__`.
- **Deep copy:** `make_receipt()` returns an independent snapshot of the cart.
- **Class attributes and `__slots__`:** `GST_RATE`, `OrderLog.FIELDS`, and fixed attributes on menu items.
- **Variable arguments:** `*args` packing and unpacking in `add_item()` and `Menu.add()`.

## How It Works

1. User picks one of 8 restaurants.
2. `build_menu()` loads that restaurant's own menu into a `Restaurant` instance.
3. User enters a name to start a cart session.
4. User adds items by ID (or by selection in the GUI). Drinks ask for a cup size first.
5. The cart shows the total including 17% GST.
6. On checkout the order is saved to `orders.csv`, a receipt copy is made, and the cart is cleared.
7. In the GUI, the History button shows a customer's past orders, newest first.

## Run It

Console version:

```
python main.py
```

GUI version:

```
python gui.py
```

## Notes

This is a learning-focused project: no payment integration and no database. Orders persist in a plain CSV file. The goal was structuring a real-world process cleanly with OOP.
