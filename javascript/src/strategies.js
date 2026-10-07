/** @import { ShippingStrategy } from './shipping-strategy.js' */

/** 599 cents flat; free from 10_000 cents subtotal. @implements {ShippingStrategy} */
export class StandardShipping {
  static FLAT_CENTS = 599;
  static FREE_THRESHOLD_CENTS = 10_000;
  name = 'Standard shipping';
  cost(order) {
    return order.subtotalCents >= StandardShipping.FREE_THRESHOLD_CENTS ? 0 : StandardShipping.FLAT_CENTS;
  }
}

/** 1_499 + 200 per started kilogram. @implements {ShippingStrategy} */
export class ExpressShipping {
  static BASE_CENTS = 1_499;
  static PER_KG_CENTS = 200;
  name = 'Express shipping';
  cost(order) {
    return ExpressShipping.BASE_CENTS + ExpressShipping.PER_KG_CENTS * Math.ceil(order.weightGrams / 1_000);
  }
}

/** Always free. @implements {ShippingStrategy} */
export class StorePickup {
  name = 'Store pickup';
  cost() { return 0; }
}
