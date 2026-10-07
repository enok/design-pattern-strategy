package io.github.enok.patterns.strategy;

/** Decorates an ad-hoc strategy with a display name. Package-private helper. */
record NamedShipping(String name, ShippingStrategy delegate) implements ShippingStrategy {

    @Override
    public long cost(Order order) {
        return delegate.cost(order);
    }
}
