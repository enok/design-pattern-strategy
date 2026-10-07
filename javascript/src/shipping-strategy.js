/**
 * Strategy contract (duck-typed; JavaScript has no interfaces).
 *
 * @typedef {object} ShippingStrategy
 * @property {string} name Human-readable label.
 * @property {(order: import('./order.js').Order) => number} cost
 *   Shipping price in integer cents for the given order.
 *
 * Any object with this shape is a valid strategy, so the contract stays open:
 * new strategies are added without touching `Checkout`.
 */

/**
 * Build a strategy from a plain function (strategy = behavior).
 * @param {string} name
 * @param {(order: import('./order.js').Order) => number} fn
 * @returns {ShippingStrategy}
 */
export function strategyFrom(name, fn) {
  if (typeof fn !== 'function') throw new TypeError('fn must be a function');
  return Object.freeze({ name: String(name), cost: (order) => fn(order) });
}

/** Type guard for the duck-typed contract. */
export function isShippingStrategy(value) {
  return value != null && typeof value.cost === 'function';
}
