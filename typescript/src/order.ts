/** Immutable value object; money is integer cents, weight is integer grams. */
export class Order {
  readonly subtotalCents: number;
  readonly weightGrams: number;

  constructor(subtotalCents: number, weightGrams: number) {
    this.subtotalCents = requireNonNegativeInt("subtotalCents", subtotalCents);
    this.weightGrams = requireNonNegativeInt("weightGrams", weightGrams);
    Object.freeze(this);
  }
}

function requireNonNegativeInt(field: string, value: number): number {
  if (!Number.isSafeInteger(value) || value < 0) {
    throw new RangeError(`${field} must be an integer >= 0, got ${String(value)}`);
  }
  return value;
}
