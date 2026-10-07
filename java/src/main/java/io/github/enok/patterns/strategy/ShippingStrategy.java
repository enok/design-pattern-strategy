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
