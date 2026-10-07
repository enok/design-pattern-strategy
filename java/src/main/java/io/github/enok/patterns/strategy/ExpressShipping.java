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
