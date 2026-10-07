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
