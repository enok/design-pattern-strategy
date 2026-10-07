"""ConcreteStrategy role: the interchangeable shipping algorithms."""

from __future__ import annotations

from typing import override

from .order import Order
from .shipping_strategy import ShippingStrategy

FREE_SHIPPING_THRESHOLD_CENTS = 10_000
STANDARD_FLAT_CENTS = 599
EXPRESS_BASE_CENTS = 1_499
EXPRESS_PER_KG_CENTS = 200
GRAMS_PER_KG = 1_000


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
