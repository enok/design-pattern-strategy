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
