# 03 - Application Example: Checkout Shipping Cost

This is a focused slice, not a full application. There is no cart, catalog, payment or
persistence here: only the one part of a checkout that varies, so the pattern stays easy
to see. Background on the pattern is in [01-pattern-explanation.md](01-pattern-explanation.md);
the diagrams for this example are in [04-example-diagram.md](04-example-diagram.md).

## The scenario

An online store must price shipping at checkout. Customers can choose:

- **Standard**: a flat fee, free for large orders.
- **Express**: a base fee plus a charge per started kilogram.
- **Store pickup**: always free.
- **Promotional flat rate**: a fixed amount the marketing team wants to try this week.

The checkout flow itself (take an order, add shipping, return a total) is identical for
all of them. Only the shipping-cost algorithm changes.

## Why the naive approaches break down

The first attempt is usually a conditional inside the checkout:

```text
function total(order, shippingType):
    if shippingType == "standard":
        shipping = (order.subtotal >= 10000) ? 0 : 599
    else if shippingType == "express":
        shipping = 1499 + 200 * ceil(order.weight / 1000)
    else if shippingType == "pickup":
        shipping = 0
    else:
        error("unknown shipping type")
    return order.subtotal + shipping
```

Every new option edits this function, so the checkout is never "finished". Each change
risks breaking the existing branches, tests must exercise the whole function, and the
branch list grows into a tangle once rules interact (free-shipping thresholds, regions,
holidays).

The other common attempt is a subclass per shipping type: `ExpressCheckout`,
`PickupCheckout`, and so on. That welds the shipping rule to the whole checkout flow. You
cannot change the rule for an existing checkout without creating a new object, and
combining it with a second varying concern (say, tax) multiplies the subclasses.

## How Strategy fixes it

Pull the varying algorithm behind a small interface and let the checkout hold one. The
checkout asks the strategy for the cost and does not know which rule answers.

| Pattern role | Name in this example | Responsibility |
| --- | --- | --- |
| Strategy | `ShippingStrategy` | One operation, `cost(order)`, returning integer cents, plus a human-readable `name` |
| ConcreteStrategy | `StandardShipping` | 599 cents; free when `subtotalCents >= 10_000` |
| ConcreteStrategy | `ExpressShipping` | `1_499 + 200 x ceil(weightGrams / 1_000)`; weight 0 gives 1_499 |
| ConcreteStrategy | `StorePickup` | Always 0 |
| Ad-hoc strategy | Flat-rate lambda | Always 300; shows that a strategy is just behavior |
| Context | `Checkout` | Holds a strategy by composition; `total(order)` = subtotal + strategy cost; `setShippingStrategy(s)` swaps it at runtime |
| Client | The demo | Chooses and swaps strategies |
| Data | `Order` | Immutable value object with `subtotalCents` and `weightGrams` |

## Rules the implementations follow

- **Integer cents everywhere.** No floating-point money. Only the demo formats cents as
  `units.cc` for display.
- **Validation.** `Order` rejects a negative `subtotalCents` or `weightGrams` with an
  `IllegalArgumentException`. `Checkout` rejects a `null` strategy with a
  `NullPointerException`, both at construction and on swap.
- **Open/closed.** `ShippingStrategy` is deliberately not sealed. A new rule is a new
  class (or lambda) passed in; `Checkout` is never edited.
- **Lambdas as strategies.** Because the contract is a single operation, a lambda can
  stand in for a class: `ShippingStrategy` is a `@FunctionalInterface`.

## Golden table

The JUnit tests assert all 16 totals (subtotal + shipping, in cents).

| Order | subtotalCents | weightGrams | Standard | Express | Pickup | Flat 300 |
| --- | --- | --- | --- | --- | --- | --- |
| A | 4_990 | 1_200 | 5_589 | 6_889 | 4_990 | 5_290 |
| B | 10_000 | 1_000 | 10_000 | 11_699 | 10_000 | 10_300 |
| C | 9_999 | 0 | 10_598 | 11_498 | 9_999 | 10_299 |
| D | 25_000 | 3_001 | 25_000 | 27_299 | 25_000 | 25_300 |

Order B sits exactly on the free-shipping threshold, and order C has zero weight, so the
boundary rules are covered. The tests also check the runtime swap (A: 5_589 to 6_889),
the null-strategy rejections, and both negative-value rejections.

## Expected demo output

The demo prices order A with all four strategies, then swaps at runtime.

```text
Order: subtotal=49.90 weight=1200g
Standard shipping -> shipping 5.99 | total 55.89
Express shipping -> shipping 18.99 | total 68.89
Store pickup -> shipping 0.00 | total 49.90
Flat rate (lambda) -> shipping 3.00 | total 52.90
Swapped at runtime: Standard shipping -> Express shipping | total 55.89 -> 68.89
```

## Where is the code?

The Java 25 implementation is in [`../java/`](../java/) and passes the golden table above. Component by component, the source is also on one page: [05-code-by-component.md](05-code-by-component.md).

From inside `java/` (needs JDK 25 and Maven 3.9.x):

```text
mvn -q verify
java -cp target/classes io.github.enok.patterns.strategy.Demo
```
