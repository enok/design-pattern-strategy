"""Strategy role, concrete strategies and the function adapter."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, override

from .order import Order

FREE_SHIPPING_THRESHOLD_CENTS = 10_000
STANDARD_FLAT_CENTS = 599
EXPRESS_BASE_CENTS = 1_499
EXPRESS_PER_KG_CENTS = 200
GRAMS_PER_KG = 1_000


class ShippingStrategy(Protocol):
    """Strategy role: the interchangeable algorithm interface.

    Structural typing keeps the abstraction open: any object with a ``name``
    and a ``cost(order) -> int`` (cents) is a strategy, no inheritance needed.
    """

    @property
    def name(self) -> str:
        """Human-readable label."""
        ...

    def cost(self, order: Order) -> int:
        """Return the shipping cost in integer cents."""
        ...


class StandardShipping(ShippingStrategy):
    """ConcreteStrategy: 599 cents flat, free from 10_000 cents subtotal."""

    name = "Standard shipping"

    @override
    def cost(self, order: Order) -> int:
        if order.subtotal_cents >= FREE_SHIPPING_THRESHOLD_CENTS:
            return 0
        return STANDARD_FLAT_CENTS


class ExpressShipping(ShippingStrategy):
    """ConcreteStrategy: 1_499 + 200 per started kilogram."""

    name = "Express shipping"

    @override
    def cost(self, order: Order) -> int:
        started_kg = -(-order.weight_grams // GRAMS_PER_KG)  # integer ceil division
        return EXPRESS_BASE_CENTS + EXPRESS_PER_KG_CENTS * started_kg


class StorePickup(ShippingStrategy):
    """ConcreteStrategy: customer collects the order, always free."""

    name = "Store pickup"

    @override
    def cost(self, order: Order) -> int:
        return 0


class FunctionStrategy:
    """Adapter: turns a plain ``Callable[[Order], int]`` into a strategy.

    Shows that a strategy is just behavior; no class hierarchy required.
    """

    def __init__(self, name: str, fn: Callable[[Order], int]) -> None:
        if not callable(fn):
            raise TypeError("fn must be callable")
        self._name = name
        self._fn = fn

    @property
    def name(self) -> str:
        return self._name

    def cost(self, order: Order) -> int:
        return self._fn(order)
