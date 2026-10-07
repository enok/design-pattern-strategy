# Strategy pattern - Java 25

Checkout shipping-cost example. Model, rules and golden table are described in
[`../docs/03-application-example.md`](../docs/03-application-example.md).

## Roles (package `io.github.enok.patterns.strategy`)

| Class | Pattern role | What it does |
| --- | --- | --- |
| `ShippingStrategy` | Strategy | `@FunctionalInterface`, `long cost(Order)` + default `name()`; static `named(...)` labels a lambda. Not sealed, so it stays open for extension. |
| `StandardShipping` | ConcreteStrategy | 599 cents flat, free from 10,000 cents subtotal. |
| `ExpressShipping` | ConcreteStrategy | 1,499 + 200 per started kilogram. |
| `StorePickup` | ConcreteStrategy | Always 0. |
| `NamedShipping` | helper | Package-private wrapper that gives a lambda a display name. |
| `Checkout` | Context | Holds a strategy by composition, `total(order)`, runtime `setShippingStrategy`; rejects `null`. |
| `Order` | value object | Record `(subtotalCents, weightGrams)`; compact constructor rejects negatives. |
| `Demo` | client | Prints the spec's demo text; `render()` is package-visible so tests assert it. |

## Java 25 / modern features used

- Instance `void main()` and `IO.println` (JEP 512, final in Java 25) in `Demo`.
- Records for `Order` and the stateless concrete strategies, with compact-constructor validation.
- `Math.ceilDiv` for the per-kilogram rounding.
- Text block in the demo test; `var`; `String.formatted`; `List.getFirst()`.
- Lambdas as strategies via the functional interface.

## Run

Requires JDK 25 and Maven 3.9.x.

```text
mvn -q verify
java -cp target/classes io.github.enok.patterns.strategy.Demo
```
