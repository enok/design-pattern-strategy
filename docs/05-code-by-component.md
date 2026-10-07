# Code by component — Java 25

This page reads the Strategy example component by component: for each role in the pattern you see the Java source, in a collapsible section. The files are shown whole and are generated from the source tree, so they cannot drift. Build and run commands are in [`java/`](../java/) ([README](../java/README.md)).

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
