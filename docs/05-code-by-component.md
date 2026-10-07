# Code by component — Java 25 · Python 3 · JavaScript (ES2026) · TypeScript 7

This page reads the Strategy example component by component: for each role in the pattern you see the same component in every language, with one collapsible section per language. The files are shown whole and are generated from the source tree, so they cannot drift. Run commands are in each language folder: [`java/`](../java/) ([README](../java/README.md)), [`python/`](../python/) ([README](../python/README.md)), [`javascript/`](../javascript/) ([README](../javascript/README.md)), [`typescript/`](../typescript/) ([README](../typescript/README.md)).

## Components

1. [Strategy interface](#1-strategy-interface)
2. [Concrete strategies](#2-concrete-strategies)
3. [Value object](#3-value-object)
4. [Context](#4-context)
5. [Client (demo)](#5-client-demo)

## 1. Strategy interface

The Strategy declares the single operation every interchangeable algorithm must offer.

<details open>
<summary><b>Java 25</b> · <code>ShippingStrategy.java</code>, <code>NamedShipping.java</code></summary>

<!-- source: java/src/main/java/io/github/enok/patterns/strategy/ShippingStrategy.java -->
```java
package io.github.enok.patterns.strategy;

import java.util.Objects;

/**
 * <b>Strategy</b> role of the Strategy pattern: one family of interchangeable
 * shipping-price algorithms behind a single operation.
 *
 * <p>The interface is deliberately <em>not</em> sealed: anyone can add a new strategy
 * (a class, a record, or just a lambda) without touching {@link Checkout}. That is the
 * open/closed principle at work. Because it has exactly one abstract method it is also a
 * {@link FunctionalInterface}, so a lambda is a perfectly valid strategy.
 */
@FunctionalInterface
public interface ShippingStrategy {

    /**
     * Prices shipping for an order.
     *
     * @param order the order being shipped, never {@code null}
     * @return shipping cost in integer cents, never negative
     */
    long cost(Order order);

    /**
     * Human-readable label used in the demo output. Lambdas get the default; wrap them
     * with {@link #named(String, ShippingStrategy)} to give them a label.
     *
     * @return the strategy name
     */
    default String name() {
        return getClass().getSimpleName();
    }

    /**
     * Gives an ad-hoc strategy (typically a lambda) a display name.
     *
     * @param name     label to report from {@link #name()}
     * @param strategy the behavior to delegate to
     * @return a strategy that delegates {@code cost} and reports {@code name}
     * @throws NullPointerException if either argument is {@code null}
     */
    static ShippingStrategy named(String name, ShippingStrategy strategy) {
        Objects.requireNonNull(name, "name must not be null");
        Objects.requireNonNull(strategy, "strategy must not be null");
        return new NamedShipping(name, strategy);
    }
}
```

<!-- source: java/src/main/java/io/github/enok/patterns/strategy/NamedShipping.java -->
```java
package io.github.enok.patterns.strategy;

/** Decorates an ad-hoc strategy with a display name. Package-private helper. */
record NamedShipping(String name, ShippingStrategy delegate) implements ShippingStrategy {

    @Override
    public long cost(Order order) {
        return delegate.cost(order);
    }
}
```

</details>

<details>
<summary><b>Python 3</b> · <code>shipping_strategy.py</code></summary>

<!-- source: python/src/checkout_strategy/shipping_strategy.py -->
```python
"""Strategy role: the ShippingStrategy Protocol and the function adapter."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from .order import Order


class ShippingStrategy(Protocol):
    """Strategy role: the interchangeable algorithm interface.

    Structural typing keeps the abstraction open: any object with a ``name``
    and a ``cost(order) -> int`` (cents) is a strategy, no inheritance needed.
    """

    @property
    def name(self) -> str:
        """Human-readable label."""
        ...

    def cost(self, order: Order) -> int:
        """Return the shipping cost in integer cents."""
        ...


class FunctionStrategy:
    """Adapter: turns a plain ``Callable[[Order], int]`` into a strategy.

    Shows that a strategy is just behavior; no class hierarchy required.
    """

    def __init__(self, name: str, fn: Callable[[Order], int]) -> None:
        if not callable(fn):
            raise TypeError("fn must be callable")
        self._name = name
        self._fn = fn

    @property
    def name(self) -> str:
        return self._name

    def cost(self, order: Order) -> int:
        return self._fn(order)
```

</details>

<details>
<summary><b>JavaScript (ES2026)</b> · <code>shipping-strategy.js</code></summary>

<!-- source: javascript/src/shipping-strategy.js -->
```javascript
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
```

</details>

<details>
<summary><b>TypeScript 7</b> · <code>shipping-strategy.ts</code></summary>

<!-- source: typescript/src/shipping-strategy.ts -->
```typescript
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
```

</details>

## 2. Concrete strategies

Each ConcreteStrategy implements one shipping-cost algorithm behind the Strategy contract.

<details open>
<summary><b>Java 25</b> · <code>StandardShipping.java</code>, <code>ExpressShipping.java</code>, <code>StorePickup.java</code></summary>

<!-- source: java/src/main/java/io/github/enok/patterns/strategy/StandardShipping.java -->
```java
package io.github.enok.patterns.strategy;

/**
 * <b>ConcreteStrategy</b>: 599 cents flat, free when the subtotal reaches 10,000 cents.
 */
public record StandardShipping() implements ShippingStrategy {

    private static final long FLAT_CENTS = 599;
    private static final int FREE_THRESHOLD_CENTS = 10_000;

    @Override
    public long cost(Order order) {
        return order.subtotalCents() >= FREE_THRESHOLD_CENTS ? 0 : FLAT_CENTS;
    }

    @Override
    public String name() {
        return "Standard shipping";
    }
}
```

<!-- source: java/src/main/java/io/github/enok/patterns/strategy/ExpressShipping.java -->
```java
package io.github.enok.patterns.strategy;

/**
 * <b>ConcreteStrategy</b>: 1,499 cents base plus 200 cents per started kilogram.
 */
public record ExpressShipping() implements ShippingStrategy {

    private static final long BASE_CENTS = 1_499;
    private static final long PER_KG_CENTS = 200;
    private static final int GRAMS_PER_KG = 1_000;

    @Override
    public long cost(Order order) {
        return BASE_CENTS + PER_KG_CENTS * Math.ceilDiv(order.weightGrams(), GRAMS_PER_KG);
    }

    @Override
    public String name() {
        return "Express shipping";
    }
}
```

<!-- source: java/src/main/java/io/github/enok/patterns/strategy/StorePickup.java -->
```java
package io.github.enok.patterns.strategy;

/**
 * <b>ConcreteStrategy</b>: the customer collects the order, so shipping is always free.
 */
public record StorePickup() implements ShippingStrategy {

    @Override
    public long cost(Order order) {
        return 0;
    }

    @Override
    public String name() {
        return "Store pickup";
    }
}
```

</details>

<details>
<summary><b>Python 3</b> · <code>strategies.py</code></summary>

<!-- source: python/src/checkout_strategy/strategies.py -->
```python
"""ConcreteStrategy role: the interchangeable shipping algorithms."""

from __future__ import annotations

from typing import override

from .order import Order
from .shipping_strategy import ShippingStrategy

FREE_SHIPPING_THRESHOLD_CENTS = 10_000
STANDARD_FLAT_CENTS = 599
EXPRESS_BASE_CENTS = 1_499
EXPRESS_PER_KG_CENTS = 200
GRAMS_PER_KG = 1_000


class StandardShipping(ShippingStrategy):
    """ConcreteStrategy: 599 cents flat, free from 10_000 cents subtotal."""

    name = "Standard shipping"

    @override
    def cost(self, order: Order) -> int:
        if order.subtotal_cents >= FREE_SHIPPING_THRESHOLD_CENTS:
            return 0
        return STANDARD_FLAT_CENTS


class ExpressShipping(ShippingStrategy):
    """ConcreteStrategy: 1_499 + 200 per started kilogram."""

    name = "Express shipping"

    @override
    def cost(self, order: Order) -> int:
        started_kg = -(-order.weight_grams // GRAMS_PER_KG)  # integer ceil division
        return EXPRESS_BASE_CENTS + EXPRESS_PER_KG_CENTS * started_kg


class StorePickup(ShippingStrategy):
    """ConcreteStrategy: customer collects the order, always free."""

    name = "Store pickup"

    @override
    def cost(self, order: Order) -> int:
        return 0
```

</details>

<details>
<summary><b>JavaScript (ES2026)</b> · <code>strategies.js</code></summary>

<!-- source: javascript/src/strategies.js -->
```javascript
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
```

</details>

<details>
<summary><b>TypeScript 7</b> · <code>strategies.ts</code></summary>

<!-- source: typescript/src/strategies.ts -->
```typescript
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
```

</details>

## 3. Value object

The immutable Order is the data every strategy prices; it validates its own invariants.

<details open>
<summary><b>Java 25</b> · <code>Order.java</code></summary>

<!-- source: java/src/main/java/io/github/enok/patterns/strategy/Order.java -->
```java
package io.github.enok.patterns.strategy;

/**
 * Immutable value object passed to every strategy. Money is integer cents; there is no
 * floating-point money anywhere in this example.
 *
 * @param subtotalCents merchandise total in cents, must be {@code >= 0}
 * @param weightGrams   parcel weight in grams, must be {@code >= 0}
 */
public record Order(int subtotalCents, int weightGrams) {

    /**
     * Validates the components.
     *
     * @throws IllegalArgumentException if either component is negative
     */
    public Order {
        if (subtotalCents < 0) {
            throw new IllegalArgumentException("subtotalCents must be >= 0 but was " + subtotalCents);
        }
        if (weightGrams < 0) {
            throw new IllegalArgumentException("weightGrams must be >= 0 but was " + weightGrams);
        }
    }
}
```

</details>

<details>
<summary><b>Python 3</b> · <code>order.py</code></summary>

<!-- source: python/src/checkout_strategy/order.py -->
```python
"""The ``Order`` value object consumed by every shipping strategy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Order:
    """Immutable value object (not a pattern role): what a strategy prices.

    Money is integer cents; weight is integer grams.

    Raises:
        TypeError: a field is not an ``int`` (``bool`` is rejected too).
        ValueError: a field is negative.
    """

    subtotal_cents: int
    weight_grams: int

    def __post_init__(self) -> None:
        for field_name in ("subtotal_cents", "weight_grams"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{field_name} must be an int, got {type(value).__name__}")
            if value < 0:
                raise ValueError(f"{field_name} must be >= 0, got {value}")
```

</details>

<details>
<summary><b>JavaScript (ES2026)</b> · <code>order.js</code></summary>

<!-- source: javascript/src/order.js -->
```javascript
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
```

</details>

<details>
<summary><b>TypeScript 7</b> · <code>order.ts</code></summary>

<!-- source: typescript/src/order.ts -->
```typescript
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
```

</details>

## 4. Context

The Checkout holds a Strategy by composition, delegates pricing to it and lets it be swapped at runtime.

<details open>
<summary><b>Java 25</b> · <code>Checkout.java</code></summary>

<!-- source: java/src/main/java/io/github/enok/patterns/strategy/Checkout.java -->
```java
package io.github.enok.patterns.strategy;

import java.util.Objects;

/**
 * <b>Context</b> role: runs the fixed checkout flow and delegates the part that varies
 * (shipping price) to whichever {@link ShippingStrategy} it currently holds.
 *
 * <p>The strategy is held by composition and can be swapped at runtime. {@code Checkout}
 * never inspects the concrete type, so new strategies need no change here.
 */
public final class Checkout {

    private ShippingStrategy shippingStrategy;

    /**
     * @param shippingStrategy initial strategy
     * @throws NullPointerException if {@code shippingStrategy} is {@code null}
     */
    public Checkout(ShippingStrategy shippingStrategy) {
        this.shippingStrategy = Objects.requireNonNull(shippingStrategy, "shippingStrategy must not be null");
    }

    /**
     * Computes subtotal plus shipping.
     *
     * @param order the order to price
     * @return total in cents
     * @throws NullPointerException if {@code order} is {@code null}
     */
    public long total(Order order) {
        Objects.requireNonNull(order, "order must not be null");
        return order.subtotalCents() + shippingStrategy.cost(order);
    }

    /**
     * Swaps the strategy at runtime.
     *
     * @param shippingStrategy the new strategy
     * @throws NullPointerException if {@code shippingStrategy} is {@code null}
     */
    public void setShippingStrategy(ShippingStrategy shippingStrategy) {
        this.shippingStrategy = Objects.requireNonNull(shippingStrategy, "shippingStrategy must not be null");
    }

    /** @return the strategy currently in use */
    public ShippingStrategy shippingStrategy() {
        return shippingStrategy;
    }
}
```

</details>

<details>
<summary><b>Python 3</b> · <code>checkout.py</code></summary>

<!-- source: python/src/checkout_strategy/checkout.py -->
```python
"""Context role."""

from __future__ import annotations

from .order import Order
from .shipping_strategy import ShippingStrategy


class Checkout:
    """Context role: holds a strategy by composition and delegates to it.

    The checkout flow never changes when strategies are added (open/closed).

    Raises:
        TypeError: a ``None`` strategy is passed to the constructor or setter.
    """

    def __init__(self, strategy: ShippingStrategy) -> None:
        self._strategy = self._require(strategy)

    @staticmethod
    def _require(strategy: ShippingStrategy | None) -> ShippingStrategy:
        if strategy is None:
            raise TypeError("shipping strategy must not be None")
        return strategy

    @property
    def shipping_strategy(self) -> ShippingStrategy:
        return self._strategy

    @shipping_strategy.setter
    def shipping_strategy(self, strategy: ShippingStrategy) -> None:
        """Swap the algorithm at runtime."""
        self._strategy = self._require(strategy)

    def total(self, order: Order) -> int:
        """Subtotal plus the current strategy's shipping cost, in cents."""
        return order.subtotal_cents + self._strategy.cost(order)
```

</details>

<details>
<summary><b>JavaScript (ES2026)</b> · <code>checkout.js</code></summary>

<!-- source: javascript/src/checkout.js -->
```javascript
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
```

</details>

<details>
<summary><b>TypeScript 7</b> · <code>checkout.ts</code></summary>

<!-- source: typescript/src/checkout.ts -->
```typescript
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
```

</details>

## 5. Client (demo)

The client picks strategies, hands them to the context and shows the runtime swap.

<details open>
<summary><b>Java 25</b> · <code>Demo.java</code></summary>

<!-- source: java/src/main/java/io/github/enok/patterns/strategy/Demo.java -->
```java
package io.github.enok.patterns.strategy;

import java.util.ArrayList;
import java.util.List;

/**
 * Tiny runnable demo: prices one order with four strategies, then swaps at runtime.
 * Uses the Java 25 compact launch protocol (instance {@code main}, JEP 512).
 */
public final class Demo {

    /** Builds the exact demo text (no trailing newline). Kept separate so tests can assert it. */
    static String render() {
        var order = new Order(4_990, 1_200);
        var flatRate = ShippingStrategy.named("Flat rate (lambda)", o -> 300);
        var strategies = List.of(new StandardShipping(), new ExpressShipping(), new StorePickup(), flatRate);

        var lines = new ArrayList<String>();
        lines.add("Order: subtotal=%s weight=%dg".formatted(money(order.subtotalCents()), order.weightGrams()));

        var checkout = new Checkout(strategies.getFirst());
        for (ShippingStrategy strategy : strategies) {
            checkout.setShippingStrategy(strategy);
            lines.add("%s -> shipping %s | total %s".formatted(
                    strategy.name(), money(strategy.cost(order)), money(checkout.total(order))));
        }

        var swapped = new Checkout(new StandardShipping());
        var before = swapped.shippingStrategy();
        long totalBefore = swapped.total(order);
        swapped.setShippingStrategy(new ExpressShipping());
        lines.add("Swapped at runtime: %s -> %s | total %s -> %s".formatted(
                before.name(), swapped.shippingStrategy().name(), money(totalBefore), money(swapped.total(order))));

        return String.join("\n", lines);
    }

    /** Formats non-negative cents as {@code units.cc}. */
    static String money(long cents) {
        return "%d.%02d".formatted(cents / 100, cents % 100);
    }

    void main() {
        IO.println(render());
    }
}
```

</details>

<details>
<summary><b>Python 3</b> · <code>demo.py</code>, <code>__main__.py</code>, <code>__init__.py</code></summary>

<!-- source: python/src/checkout_strategy/demo.py -->
```python
"""Demo client: prices order A with every strategy, then swaps at runtime."""

from __future__ import annotations

from .checkout import Checkout
from .order import Order
from .shipping_strategy import FunctionStrategy, ShippingStrategy
from .strategies import ExpressShipping, StandardShipping, StorePickup


def money(cents: int) -> str:
    """Format integer cents as ``units.cc``."""
    units, rest = divmod(cents, 100)
    return f"{units}.{rest:02d}"


def render() -> str:
    """Return the exact demo text (no trailing newline)."""
    order = Order(subtotal_cents=4_990, weight_grams=1_200)
    flat: ShippingStrategy = FunctionStrategy("Flat rate (function)", lambda _o: 300)
    strategies: list[ShippingStrategy] = [
        StandardShipping(),
        ExpressShipping(),
        StorePickup(),
        flat,
    ]
    lines = [f"Order: subtotal={money(order.subtotal_cents)} weight={order.weight_grams}g"]
    checkout = Checkout(strategies[0])
    for strategy in strategies:
        checkout.shipping_strategy = strategy
        lines.append(
            f"{strategy.name} -> shipping {money(strategy.cost(order))}"
            f" | total {money(checkout.total(order))}"
        )
    checkout.shipping_strategy = StandardShipping()
    before = checkout.total(order)
    first = checkout.shipping_strategy.name
    checkout.shipping_strategy = ExpressShipping()
    lines.append(
        f"Swapped at runtime: {first} -> {checkout.shipping_strategy.name}"
        f" | total {money(before)} -> {money(checkout.total(order))}"
    )
    return "\n".join(lines)
```

<!-- source: python/src/checkout_strategy/__main__.py -->
```python
"""``python -m checkout_strategy`` prints the demo."""

from .demo import render

if __name__ == "__main__":
    print(render())
```

<!-- source: python/src/checkout_strategy/__init__.py -->
```python
"""Strategy pattern example: pluggable shipping costs in a checkout."""

from .checkout import Checkout
from .order import Order
from .shipping_strategy import FunctionStrategy, ShippingStrategy
from .strategies import ExpressShipping, StandardShipping, StorePickup

__all__ = [
    "Checkout",
    "ExpressShipping",
    "FunctionStrategy",
    "Order",
    "ShippingStrategy",
    "StandardShipping",
    "StorePickup",
]
```

</details>

<details>
<summary><b>JavaScript (ES2026)</b> · <code>demo.js</code></summary>

<!-- source: javascript/src/demo.js -->
```javascript
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
```

</details>

<details>
<summary><b>TypeScript 7</b> · <code>demo.ts</code>, <code>index.ts</code></summary>

<!-- source: typescript/src/demo.ts -->
```typescript
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
```

<!-- source: typescript/src/index.ts -->
```typescript
export { Checkout } from "./checkout.js";
export { Order } from "./order.js";
export { strategyFrom } from "./shipping-strategy.js";
export type { ShippingCostFn, ShippingStrategy } from "./shipping-strategy.js";
export { ExpressShipping, StandardShipping, StorePickup } from "./strategies.js";
```

</details>
