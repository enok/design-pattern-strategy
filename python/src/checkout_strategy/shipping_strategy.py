"""Strategy role: the ShippingStrategy Protocol and the function adapter."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from .order import Order


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
