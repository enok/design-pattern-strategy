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
