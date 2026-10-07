import assert from "node:assert/strict";
import { test } from "node:test";
import {
  Checkout,
  ExpressShipping,
  Order,
  StandardShipping,
  StorePickup,
  strategyFrom,
  type ShippingStrategy,
} from "../src/index.js";
import { render } from "../src/demo.js";

const orders = {
  A: new Order(4_990, 1_200),
  B: new Order(10_000, 1_000),
  C: new Order(9_999, 0),
  D: new Order(25_000, 3_001),
} as const;

const strategies: Record<string, ShippingStrategy> = {
  standard: new StandardShipping(),
  express: new ExpressShipping(),
  pickup: new StorePickup(),
  flat: strategyFrom("Flat rate (lambda)", () => 300),
};

// order -> [standard, express, pickup, flat300] totals
const golden = {
  A: [5_589, 6_889, 4_990, 5_290],
  B: [10_000, 11_699, 10_000, 10_300],
  C: [10_598, 11_498, 9_999, 10_299],
  D: [25_000, 27_299, 25_000, 25_300],
} as const satisfies Record<keyof typeof orders, readonly number[]>;

const keys = ["standard", "express", "pickup", "flat"] as const;

for (const [label, expected] of Object.entries(golden)) {
  const order = orders[label as keyof typeof orders];
  keys.forEach((key, i) => {
    test(`golden ${label} / ${key}`, () => {
      const strategy = strategies[key];
      assert.ok(strategy);
      assert.equal(new Checkout(strategy).total(order), expected[i]);
    });
  });
}

test("shipping-only costs", () => {
  const standard = new StandardShipping();
  const express = new ExpressShipping();
  assert.deepEqual(
    Object.values(orders).map((o) => standard.cost(o)),
    [599, 0, 599, 0],
  );
  assert.deepEqual(
    Object.values(orders).map((o) => express.cost(o)),
    [1_899, 1_699, 1_499, 2_299],
  );
});

test("runtime swap changes the total", () => {
  const checkout = new Checkout(new StandardShipping());
  assert.equal(checkout.total(orders.A), 5_589);
  checkout.setShippingStrategy(new ExpressShipping());
  assert.equal(checkout.total(orders.A), 6_889);
});

test("null/undefined strategy rejected (constructor and setter)", () => {
  assert.throws(() => new Checkout(null as unknown as ShippingStrategy), TypeError);
  assert.throws(() => new Checkout(undefined as unknown as ShippingStrategy), TypeError);
  const checkout = new Checkout(new StorePickup());
  assert.throws(() => checkout.setShippingStrategy(null as unknown as ShippingStrategy), TypeError);
  assert.throws(
    () => checkout.setShippingStrategy(undefined as unknown as ShippingStrategy),
    TypeError,
  );
  assert.equal(checkout.shippingStrategy.name, "Store pickup");
});

test("negative subtotal rejected", () => {
  assert.throws(() => new Order(-1, 0), RangeError);
});

test("negative weight rejected", () => {
  assert.throws(() => new Order(0, -1), RangeError);
});

test("demo output matches the spec exactly", () => {
  const expected = [
    "Order: subtotal=49.90 weight=1200g",
    "Standard shipping -> shipping 5.99 | total 55.89",
    "Express shipping -> shipping 18.99 | total 68.89",
    "Store pickup -> shipping 0.00 | total 49.90",
    "Flat rate (lambda) -> shipping 3.00 | total 52.90",
    "Swapped at runtime: Standard shipping -> Express shipping | total 55.89 -> 68.89",
  ].join("\n");
  assert.equal(render(), expected);
});
