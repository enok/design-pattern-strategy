"""The ``Order`` value object consumed by every shipping strategy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Order:
    """Immutable value object (not a pattern role): what a strategy prices.

    Money is integer cents; weight is integer grams.

    Raises:
        TypeError: a field is not an ``int`` (``bool`` is rejected too).
        ValueError: a field is negative.
    """

    subtotal_cents: int
    weight_grams: int

    def __post_init__(self) -> None:
        for field_name in ("subtotal_cents", "weight_grams"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{field_name} must be an int, got {type(value).__name__}")
            if value < 0:
                raise ValueError(f"{field_name} must be >= 0, got {value}")
