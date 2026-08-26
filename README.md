# OOPs Food Delivery Platform

A console-based food ordering system in Python, built to apply core object-oriented programming principles over a simple, real-world workflow: pick a restaurant, browse a menu, build a cart, and check out.

## Overview

The project simulates a single-restaurant ordering session end to end — restaurant selection, menu display, item lookup by ID, cart management, and total calculation — using a clean class-based structure instead of a flat script.

## Structure

| File | Responsibility |
|---|---|
| `main.py` | Entry point — drives the ordering flow and user I/O |
| `restaurant.py` | `Restaurant` class — holds the menu and item lookup logic |
| `menu.py` | `MenuItem` class — represents a single menu item (id, name, price) |
| `cart.py` | `UserCart` class — manages added items and total calculation |

## Core Classes

- **`Restaurant`** — stores available menu items in a dictionary, exposes `add_item()` and `get_item(id)` for lookup.
- **`MenuItem`** — a simple data class for an item's id, name, and price.
- **`UserCart`** — tracks a user's selected items, with `add_to_cart()`, `view_cart()`, and `calc_total()`.

## How It Works

1. User picks a restaurant from a numbered list.
2. The app loads a fixed menu into that restaurant instance.
3. User enters a name to start a cart session.
4. User adds items by ID in a loop until they choose to stop.
5. The cart is displayed with a running total, then the final bill is printed.

## Concepts Practiced

- Encapsulation — each class owns its own data and behavior.
- Modular design — logic split across files instead of one script.
- Basic input validation and control flow (loops, conditionals).

## Run It

```bash
python main.py
```

## Notes

This is a learning-focused project — no persistence, no UI, no payment integration. The goal was structuring a real-world process cleanly with OOP before adding complexity.
