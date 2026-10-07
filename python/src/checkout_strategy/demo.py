"""Demo client: prices order A with every strategy, then swaps at runtime."""

from __future__ import annotations

from .checkout import Checkout
from .order import Order
from .shipping_strategy import FunctionStrategy, ShippingStrategy
from .strategies import ExpressShipping, StandardShipping, StorePickup


def money(cents: int) -> str:
    """Format integer cents as ``units.cc``."""
    units, rest = divmod(cents, 100)
    return f"{units}.{rest:02d}"


def render() -> str:
    """Return the exact demo text (no trailing newline)."""
    order = Order(subtotal_cents=4_990, weight_grams=1_200)
    flat: ShippingStrategy = FunctionStrategy("Flat rate (function)", lambda _o: 300)
    strategies: list[ShippingStrategy] = [
        StandardShipping(),
        ExpressShipping(),
        StorePickup(),
        flat,
    ]
    lines = [f"Order: subtotal={money(order.subtotal_cents)} weight={order.weight_grams}g"]
    checkout = Checkout(strategies[0])
    for strategy in strategies:
        checkout.shipping_strategy = strategy
        lines.append(
            f"{strategy.name} -> shipping {money(strategy.cost(order))}"
            f" | total {money(checkout.total(order))}"
        )
    checkout.shipping_strategy = StandardShipping()
    before = checkout.total(order)
    first = checkout.shipping_strategy.name
    checkout.shipping_strategy = ExpressShipping()
    lines.append(
        f"Swapped at runtime: {first} -> {checkout.shipping_strategy.name}"
        f" | total {money(before)} -> {money(checkout.total(order))}"
    )
    return "\n".join(lines)
