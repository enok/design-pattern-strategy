"""Strategy pattern example: pluggable shipping costs in a checkout."""

from .checkout import Checkout
from .order import Order
from .strategies import (
    ExpressShipping,
    FunctionStrategy,
    ShippingStrategy,
    StandardShipping,
    StorePickup,
)

__all__ = [
    "Checkout",
    "ExpressShipping",
    "FunctionStrategy",
    "Order",
    "ShippingStrategy",
    "StandardShipping",
    "StorePickup",
]
