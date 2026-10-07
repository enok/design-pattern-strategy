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
