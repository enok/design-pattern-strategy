package io.github.enok.patterns.strategy;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertSame;

import java.util.stream.Stream;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

class CheckoutTest {

    private static final ShippingStrategy FLAT_300 = ShippingStrategy.named("Flat 300", o -> 300);

    private static final Order A = new Order(4_990, 1_200);
    private static final Order B = new Order(10_000, 1_000);
    private static final Order C = new Order(9_999, 0);
    private static final Order D = new Order(25_000, 3_001);

    static Stream<Arguments> goldenTable() {
        return Stream.of(
                Arguments.of("A standard", A, new StandardShipping(), 5_589L),
                Arguments.of("A express", A, new ExpressShipping(), 6_889L),
                Arguments.of("A pickup", A, new StorePickup(), 4_990L),
                Arguments.of("A flat", A, FLAT_300, 5_290L),
                Arguments.of("B standard", B, new StandardShipping(), 10_000L),
                Arguments.of("B express", B, new ExpressShipping(), 11_699L),
                Arguments.of("B pickup", B, new StorePickup(), 10_000L),
                Arguments.of("B flat", B, FLAT_300, 10_300L),
                Arguments.of("C standard", C, new StandardShipping(), 10_598L),
                Arguments.of("C express", C, new ExpressShipping(), 11_498L),
                Arguments.of("C pickup", C, new StorePickup(), 9_999L),
                Arguments.of("C flat", C, FLAT_300, 10_299L),
                Arguments.of("D standard", D, new StandardShipping(), 25_000L),
                Arguments.of("D express", D, new ExpressShipping(), 27_299L),
                Arguments.of("D pickup", D, new StorePickup(), 25_000L),
                Arguments.of("D flat", D, FLAT_300, 25_300L));
    }

    @ParameterizedTest(name = "{0} -> {3}")
    @MethodSource("goldenTable")
    void totalMatchesGoldenTable(String label, Order order, ShippingStrategy strategy, long expected) {
        assertEquals(expected, new Checkout(strategy).total(order));
    }

    @Test
    void strategyCanBeSwappedAtRuntime() {
        var checkout = new Checkout(new StandardShipping());
        assertEquals(5_589L, checkout.total(A));

        var express = new ExpressShipping();
        checkout.setShippingStrategy(express);

        assertSame(express, checkout.shippingStrategy());
        assertEquals(6_889L, checkout.total(A));
    }

    @Test
    void plainLambdaIsAccepted() {
        assertEquals(5_290L, new Checkout(o -> 300).total(A));
    }

    @Test
    void nullStrategyRejectedInConstructor() {
        var ex = assertThrows(NullPointerException.class, () -> new Checkout(null));
        assertEquals("shippingStrategy must not be null", ex.getMessage());
    }

    @Test
    void nullStrategyRejectedInSetter() {
        var checkout = new Checkout(new StorePickup());
        var ex = assertThrows(NullPointerException.class, () -> checkout.setShippingStrategy(null));
        assertEquals("shippingStrategy must not be null", ex.getMessage());
        assertEquals(new StorePickup(), checkout.shippingStrategy());
    }

    @Test
    void negativeSubtotalRejected() {
        assertThrows(IllegalArgumentException.class, () -> new Order(-1, 0));
    }

    @Test
    void negativeWeightRejected() {
        assertThrows(IllegalArgumentException.class, () -> new Order(0, -1));
    }

    @Test
    void namedStrategyReportsNameAndDelegates() {
        var named = ShippingStrategy.named("Flat rate (lambda)", o -> 300);
        assertEquals("Flat rate (lambda)", named.name());
        assertEquals(300L, named.cost(A));
    }

    @Test
    void demoOutputMatchesSpecExactly() {
        var expected = """
                Order: subtotal=49.90 weight=1200g
                Standard shipping -> shipping 5.99 | total 55.89
                Express shipping -> shipping 18.99 | total 68.89
                Store pickup -> shipping 0.00 | total 49.90
                Flat rate (lambda) -> shipping 3.00 | total 52.90
                Swapped at runtime: Standard shipping -> Express shipping | total 55.89 -> 68.89""";
        assertEquals(expected, Demo.render());
    }
}
