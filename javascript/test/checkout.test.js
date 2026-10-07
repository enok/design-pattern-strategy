import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Checkout } from '../src/checkout.js';
import { Order } from '../src/order.js';
import { strategyFrom } from '../src/shipping-strategy.js';
import { ExpressShipping, StandardShipping, StorePickup } from '../src/strategies.js';
import { render } from '../src/demo.js';

const orders = { A: [4_990, 1_200], B: [10_000, 1_000], C: [9_999, 0], D: [25_000, 3_001] };
const makers = {
  Standard: () => new StandardShipping(),
  Express: () => new ExpressShipping(),
  Pickup: () => new StorePickup(),
  Flat300: () => strategyFrom('Flat rate (lambda)', () => 300),
};
const golden = {
  A: { Standard: 5_589, Express: 6_889, Pickup: 4_990, Flat300: 5_290 },
  B: { Standard: 10_000, Express: 11_699, Pickup: 10_000, Flat300: 10_300 },
  C: { Standard: 10_598, Express: 11_498, Pickup: 9_999, Flat300: 10_299 },
  D: { Standard: 25_000, Express: 27_299, Pickup: 25_000, Flat300: 25_300 },
};

for (const [label, args] of Object.entries(orders)) {
  for (const [name, make] of Object.entries(makers)) {
    test(`golden ${label}/${name}`, () => {
      assert.equal(new Checkout(make()).total(new Order(...args)), golden[label][name]);
    });
  }
}

test('runtime swap Standard -> Express on A', () => {
  const checkout = new Checkout(new StandardShipping());
  const order = new Order(4_990, 1_200);
  assert.equal(checkout.total(order), 5_589);
  checkout.setShippingStrategy(new ExpressShipping());
  assert.equal(checkout.total(order), 6_889);
});

test('null/undefined strategy rejected in constructor and setter', () => {
  for (const bad of [null, undefined]) {
    assert.throws(() => new Checkout(bad), TypeError);
    assert.throws(() => new Checkout(new StorePickup()).setShippingStrategy(bad), TypeError);
  }
});

test('Order rejects negative values', () => {
  assert.throws(() => new Order(-1, 0), RangeError);
  assert.throws(() => new Order(0, -1), RangeError);
  assert.throws(() => new Order(1.5, 0), TypeError);
});

test('demo text matches the spec exactly', () => {
  assert.equal(render(), [
    'Order: subtotal=49.90 weight=1200g',
    'Standard shipping -> shipping 5.99 | total 55.89',
    'Express shipping -> shipping 18.99 | total 68.89',
    'Store pickup -> shipping 0.00 | total 49.90',
    'Flat rate (lambda) -> shipping 3.00 | total 52.90',
    'Swapped at runtime: Standard shipping -> Express shipping | total 55.89 -> 68.89',
  ].join('\n'));
});

test('bare functions are accepted as strategies (constructor and setter)', () => {
  const order = new Order(4_990, 1_200);
  const checkout = new Checkout(() => 300);
  assert.equal(checkout.total(order), 5_290);
  assert.equal(checkout.shippingStrategyName, 'function');

  function halfPrice(o) { return Math.round(o.subtotalCents / 2); }
  checkout.setShippingStrategy(halfPrice);
  assert.equal(checkout.total(order), 4_990 + 2_495);
  assert.equal(checkout.shippingStrategyName, 'halfPrice');

  checkout.setShippingStrategy(() => 0);
  assert.equal(checkout.total(order), 4_990);
  assert.equal(checkout.shippingStrategyName, 'function');
  assert.equal(new Checkout(halfPrice).shippingStrategyName, 'halfPrice');
});
