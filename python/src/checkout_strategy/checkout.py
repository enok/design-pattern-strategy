"""Context role."""

from __future__ import annotations

from .order import Order
from .strategies import ShippingStrategy


class Checkout:
    """Context role: holds a strategy by composition and delegates to it.

    The checkout flow never changes when strategies are added (open/closed).

    Raises:
        TypeError: a ``None`` strategy is passed to the constructor or setter.
    """

    def __init__(self, strategy: ShippingStrategy) -> None:
        self._strategy = self._require(strategy)

    @staticmethod
    def _require(strategy: ShippingStrategy | None) -> ShippingStrategy:
        if strategy is None:
            raise TypeError("shipping strategy must not be None")
        return strategy

    @property
    def shipping_strategy(self) -> ShippingStrategy:
        return self._strategy

    @shipping_strategy.setter
    def shipping_strategy(self, strategy: ShippingStrategy) -> None:
        """Swap the algorithm at runtime."""
        self._strategy = self._require(strategy)

    def total(self, order: Order) -> int:
        """Subtotal plus the current strategy's shipping cost, in cents."""
        return order.subtotal_cents + self._strategy.cost(order)
