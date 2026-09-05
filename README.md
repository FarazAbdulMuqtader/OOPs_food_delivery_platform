# OOPs Food Delivery Platform

A GUI-based food ordering system in Python, built to apply core object-oriented programming principles over a simple, real-world workflow: pick a restaurant, browse a menu, build a cart, and check out. Originally a CLI application, now converted to a desktop GUI using Tkinter.

## Overview

The project simulates a single-restaurant ordering session end to end — restaurant selection, menu display, item lookup, cart management, and total calculation — through an interactive Tkinter window, backed by a clean class-based structure instead of a flat script.

## Tech Stack

- **Language:** Python 3
- **GUI:** Tkinter (standard library)
- **Paradigm:** Object-Oriented Programming

## Structure

| File            | Responsibility                                                     |
| --------------- | -------------------------------------------------------------------|
| `gui.py`        | Entry point — builds the Tkinter window and drives the UI flow     |
| `restaurant.py` | `Restaurant` class — holds the menu and item lookup logic          |
| `menu.py`       | `MenuItem` class — represents a single menu item (id, name, price) |
| `cart.py`       | `UserCart` class — manages added items and total calculation       |

## Core Classes

- **`Restaurant`** — stores available menu items in a dictionary, exposes `add_item()` and `get_item(id)` for lookup.
- **`MenuItem`** — a simple data class for an item's id, name, and price.
- **`UserCart`** — tracks a user's selected items, with `add_to_cart()`, `view_cart()`, and `calc_total()` (total includes 17% GST).

## How It Works

1. User selects a restaurant and enters a name from the GUI.
2. The window opens to an order screen headed with the restaurant and customer name (e.g. "Coconut Groove • faraz's order").
3. User browses menu items and adds them to the cart via the interface.
4. The cart updates live, with the running total calculated including 17% GST.
5. User checks out and the final bill is displayed in the window.

## Run It

```bash
python gui.py
```

> Requires Tkinter, which ships with standard Python installations on most platforms. On some Linux distros you may need to install it separately (e.g. `sudo apt install python3-tk`).

## Concepts Practiced

- **Encapsulation** — each class owns its own data and behavior.
- **Modular design** — logic split across files instead of one script.
- **Separation of concerns** — GUI/event handling kept distinct from the underlying business logic (`Restaurant`, `MenuItem`, `UserCart`).
- Event-driven programming with Tkinter widgets and callbacks.

## Notes

This is a learning-focused project — no persistence, no backend, no payment integration. The goal was structuring a real-world process cleanly with OOP, then layering a GUI on top of that structure.

## Possible Next Steps

- Add multiple restaurants with switchable menus in the GUI
- Persist orders to a file or lightweight database
- Add unit tests for cart and menu logic
- Polish UI styling (themes, icons, item images)

## License

This project is open source and available for learning purposes.
