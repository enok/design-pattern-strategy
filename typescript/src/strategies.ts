import type { Order } from "./order.js";
import type { ShippingStrategy } from "./shipping-strategy.js";

const RATES = {
  standardFlatCents: 599,
  freeShippingThresholdCents: 10_000,
  expressBaseCents: 1_499,
  expressPerKgCents: 200,
  gramsPerKg: 1_000,
} as const satisfies Record<string, number>;

abstract class NamedStrategy implements ShippingStrategy {
  readonly name: string;

  protected constructor(name: string) {
    this.name = name;
  }

  abstract cost(order: Order): number;
}

export class StandardShipping extends NamedStrategy {
  constructor() {
    super("Standard shipping");
  }

  override cost(order: Order): number {
    return order.subtotalCents >= RATES.freeShippingThresholdCents ? 0 : RATES.standardFlatCents;
  }
}

export class ExpressShipping extends NamedStrategy {
  constructor() {
    super("Express shipping");
  }

  override cost(order: Order): number {
    const kilos = Math.ceil(order.weightGrams / RATES.gramsPerKg);
    return RATES.expressBaseCents + RATES.expressPerKgCents * kilos;
  }
}

export class StorePickup extends NamedStrategy {
  constructor() {
    super("Store pickup");
  }

  override cost(_order: Order): number {
    return 0;
  }
}
