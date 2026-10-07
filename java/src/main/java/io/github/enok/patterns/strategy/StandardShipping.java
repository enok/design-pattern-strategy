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
