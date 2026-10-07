/** Immutable value object; money is integer cents, weight integer grams. */
export class Order {
  #subtotalCents;
  #weightGrams;

  /**
   * @param {number} subtotalCents integer >= 0
   * @param {number} weightGrams integer >= 0
   * @throws {TypeError} not an integer
   * @throws {RangeError} negative
   */
  constructor(subtotalCents, weightGrams) {
    this.#subtotalCents = Order.#check('subtotalCents', subtotalCents);
    this.#weightGrams = Order.#check('weightGrams', weightGrams);
    Object.freeze(this);
  }

  static #check(label, value) {
    if (!Number.isSafeInteger(value)) throw new TypeError(`${label} must be an integer`);
    if (value < 0) throw new RangeError(`${label} must be >= 0`);
    return value;
  }

  get subtotalCents() { return this.#subtotalCents; }
  get weightGrams() { return this.#weightGrams; }
}
