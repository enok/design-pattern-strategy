import type { Order } from "./order.js";
import type { ShippingStrategy } from "./shipping-strategy.js";

/** Context role: holds a strategy by composition and delegates to it. */
export class Checkout {
  #strategy: ShippingStrategy;

  constructor(strategy: ShippingStrategy) {
    this.#strategy = requireStrategy(strategy);
  }

  get shippingStrategy(): ShippingStrategy {
    return this.#strategy;
  }

  setShippingStrategy(strategy: ShippingStrategy): void {
    this.#strategy = requireStrategy(strategy);
  }

  /** Total in cents: subtotal + shipping chosen by the current strategy. */
  total(order: Order): number {
    return order.subtotalCents + this.#strategy.cost(order);
  }
}

// Compile-time types do not protect JavaScript callers, so check at runtime too.
function requireStrategy(strategy: ShippingStrategy | null | undefined): ShippingStrategy {
  if (strategy === null || strategy === undefined) {
    throw new TypeError("shipping strategy must not be null or undefined");
  }
  return strategy;
}
