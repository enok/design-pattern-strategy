import type { Order } from "./order.js";

/** Strategy role: one varying operation. Deliberately an open interface. */
export interface ShippingStrategy {
  readonly name: string;
  /** Shipping cost in integer cents. */
  cost(order: Order): number;
}

/** A strategy is just behavior: any function of this shape qualifies. */
export type ShippingCostFn = (order: Order) => number;

/** Wraps a plain function as a named strategy. */
export function strategyFrom(name: string, fn: ShippingCostFn): ShippingStrategy {
  return { name, cost: fn };
}
