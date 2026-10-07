import os
import subprocess
import sys
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from checkout_strategy import (
    Checkout,
    ExpressShipping,
    FunctionStrategy,
    Order,
    StandardShipping,
    StorePickup,
)
from checkout_strategy.demo import render

EXPECTED = """Order: subtotal=49.90 weight=1200g
Standard shipping -> shipping 5.99 | total 55.89
Express shipping -> shipping 18.99 | total 68.89
Store pickup -> shipping 0.00 | total 49.90
Flat rate (function) -> shipping 3.00 | total 52.90
Swapped at runtime: Standard shipping -> Express shipping | total 55.89 -> 68.89"""

ORDERS = {
    "A": Order(4_990, 1_200),
    "B": Order(10_000, 1_000),
    "C": Order(9_999, 0),
    "D": Order(25_000, 3_001),
}
# order -> (standard, express, pickup, flat300) totals
GOLDEN = {
    "A": (5_589, 6_889, 4_990, 5_290),
    "B": (10_000, 11_699, 10_000, 10_300),
    "C": (10_598, 11_498, 9_999, 10_299),
    "D": (25_000, 27_299, 25_000, 25_300),
}


def strategies():
    return (
        StandardShipping(),
        ExpressShipping(),
        StorePickup(),
        FunctionStrategy("Flat 300", lambda _o: 300),
    )


class GoldenTable(unittest.TestCase):
    def test_all_16_totals(self):
        for key, order in ORDERS.items():
            for strategy, expected in zip(strategies(), GOLDEN[key], strict=True):
                with self.subTest(order=key, strategy=strategy.name):
                    self.assertEqual(Checkout(strategy).total(order), expected)

    def test_shipping_only_costs(self):
        self.assertEqual([StandardShipping().cost(ORDERS[k]) for k in "ABCD"], [599, 0, 599, 0])
        self.assertEqual(
            [ExpressShipping().cost(ORDERS[k]) for k in "ABCD"], [1_899, 1_699, 1_499, 2_299]
        )


class ContextBehaviour(unittest.TestCase):
    def test_runtime_swap(self):
        checkout = Checkout(StandardShipping())
        self.assertEqual(checkout.total(ORDERS["A"]), 5_589)
        checkout.shipping_strategy = ExpressShipping()
        self.assertEqual(checkout.total(ORDERS["A"]), 6_889)

    def test_none_rejected_in_constructor(self):
        with self.assertRaises(TypeError):
            Checkout(None)  # type: ignore[arg-type]

    def test_none_rejected_in_setter(self):
        checkout = Checkout(StorePickup())
        with self.assertRaises(TypeError):
            checkout.shipping_strategy = None  # type: ignore[assignment]
        self.assertIsInstance(checkout.shipping_strategy, StorePickup)

    def test_custom_strategy_needs_no_inheritance(self):
        class Drone:
            name = "Drone"

            def cost(self, order):
                return 42

        self.assertEqual(Checkout(Drone()).total(ORDERS["C"]), 10_041)


class OrderValidation(unittest.TestCase):
    def test_negative_subtotal_rejected(self):
        with self.assertRaises(ValueError):
            Order(-1, 0)

    def test_negative_weight_rejected(self):
        with self.assertRaises(ValueError):
            Order(0, -1)

    def test_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            ORDERS["A"].subtotal_cents = 1  # type: ignore[misc]


class Demo(unittest.TestCase):
    def test_render_exact(self):
        self.assertEqual(render(), EXPECTED)

    def test_module_entry_point(self):
        src = str(Path(__file__).resolve().parents[1] / "src")
        result = subprocess.run(
            [sys.executable, "-m", "checkout_strategy"],
            capture_output=True, text=True, check=True, env={**os.environ, "PYTHONPATH": src},
        )
        self.assertEqual(result.stdout, EXPECTED + "\n")


if __name__ == "__main__":
    unittest.main()
