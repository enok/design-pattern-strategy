import { pathToFileURL } from "node:url";
import { Checkout } from "./checkout.js";
import { Order } from "./order.js";
import { strategyFrom } from "./shipping-strategy.js";
import { ExpressShipping, StandardShipping, StorePickup } from "./strategies.js";

/** Formats integer cents as `units.cc` without floating point. */
function money(cents: number): string {
  return `${Math.floor(cents / 100)}.${String(cents % 100).padStart(2, "0")}`;
}

export function render(): string {
  const order = new Order(4_990, 1_200);
  const standard = new StandardShipping();
  const express = new ExpressShipping();
  const strategies = [
    standard,
    express,
    new StorePickup(),
    strategyFrom("Flat rate (lambda)", () => 300),
  ];

  const lines = [`Order: subtotal=${money(order.subtotalCents)} weight=${order.weightGrams}g`];
  for (const strategy of strategies) {
    const checkout = new Checkout(strategy);
    lines.push(
      `${strategy.name} -> shipping ${money(strategy.cost(order))} | total ${money(checkout.total(order))}`,
    );
  }

  const checkout = new Checkout(standard);
  const before = checkout.total(order);
  checkout.setShippingStrategy(express);
  const after = checkout.total(order);
  lines.push(
    `Swapped at runtime: ${standard.name} -> ${express.name} | total ${money(before)} -> ${money(after)}`,
  );
  return lines.join("\n");
}

const entry = process.argv[1];
if (entry !== undefined && import.meta.url === pathToFileURL(entry).href) {
  console.log(render());
}
