import { isShippingStrategy, strategyFrom } from './shipping-strategy.js';

/** @import { ShippingStrategy } from './shipping-strategy.js' */

/** Context: the flow is fixed, only the shipping algorithm varies. */
export class Checkout {
  /** @type {ShippingStrategy} */
  #strategy;

  /** @param {ShippingStrategy | ((order: object) => number)} strategy */
  constructor(strategy) {
    this.#strategy = Checkout.#normalize(strategy);
  }

  static #normalize(strategy) {
    if (typeof strategy === 'function') return strategyFrom(strategy.name || 'function', strategy);
    if (!isShippingStrategy(strategy)) {
      throw new TypeError('shipping strategy must be an object with cost(order), or a function');
    }
    return strategy;
  }

  /** Swap the algorithm at runtime. @throws {TypeError} on null/undefined/invalid */
  setShippingStrategy(strategy) {
    this.#strategy = Checkout.#normalize(strategy);
  }

  get shippingStrategyName() { return this.#strategy.name; }

  /** @returns {number} subtotal + shipping, integer cents */
  total(order) {
    return order.subtotalCents + this.#strategy.cost(order);
  }
}
