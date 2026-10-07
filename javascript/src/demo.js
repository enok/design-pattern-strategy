import { Checkout } from './checkout.js';
import { Order } from './order.js';
import { strategyFrom } from './shipping-strategy.js';
import { ExpressShipping, StandardShipping, StorePickup } from './strategies.js';

const money = (cents) => `${Math.floor(cents / 100)}.${String(cents % 100).padStart(2, '0')}`;

/** @returns {string} the exact demo text (no trailing newline) */
export function render() {
  const order = new Order(4_990, 1_200);
  const standard = new StandardShipping();
  const express = new ExpressShipping();
  const strategies = [
    standard,
    express,
    new StorePickup(),
    strategyFrom('Flat rate (lambda)', () => 300),
  ];

  // ES2025 iterator helpers: lazy map over the strategies.
  const rows = strategies.values().map((s) => {
    const total = new Checkout(s).total(order);
    return `${s.name} -> shipping ${money(s.cost(order))} | total ${money(total)}`;
  });

  const checkout = new Checkout(standard);
  const before = checkout.total(order);
  checkout.setShippingStrategy(express);
  const after = checkout.total(order);

  return [
    `Order: subtotal=${money(order.subtotalCents)} weight=${order.weightGrams}g`,
    ...rows,
    `Swapped at runtime: ${standard.name} -> ${express.name} | total ${money(before)} -> ${money(after)}`,
  ].join('\n');
}

if (import.meta.filename === process.argv[1]) {
  console.log(render());
}
