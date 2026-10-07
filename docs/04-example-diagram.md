# 04 - Example Diagrams

These diagrams show the checkout shipping slice described in
[03-application-example.md](03-application-example.md). For the generic version of the
pattern, see [02-generic-diagram.md](02-generic-diagram.md).

## Class diagram

```mermaid
classDiagram
    direction LR
    class Order {
        +int subtotalCents
        +int weightGrams
    }
    class Checkout {
        -ShippingStrategy strategy
        +total(order) int
        +setShippingStrategy(strategy) void
    }
    class ShippingStrategy {
        <<interface>>
        +name String
        +cost(order) int
    }
    class StandardShipping {
        +cost(order) int
    }
    class ExpressShipping {
        +cost(order) int
    }
    class StorePickup {
        +cost(order) int
    }
    class FlatRate {
        <<lambda>>
        +name String
        +cost(order) int
    }
    Checkout o-- ShippingStrategy : has-a
    ShippingStrategy <|.. StandardShipping
    ShippingStrategy <|.. ExpressShipping
    ShippingStrategy <|.. StorePickup
    ShippingStrategy <|.. FlatRate
    Checkout ..> Order : prices
    ShippingStrategy ..> Order : reads
```

Caption: `Checkout` owns one `ShippingStrategy` by composition and never mentions a concrete
class. The three named strategies and the `FlatRate` lambda all satisfy the same one-method
contract, so any of them can be plugged in. Source: [`diagrams/checkout-class.mmd`](diagrams/checkout-class.mmd).

## Sequence diagram

```mermaid
sequenceDiagram
    participant Demo as Client (Demo)
    participant C as Checkout
    participant S as StandardShipping
    participant E as ExpressShipping
    Note over Demo: Order A = subtotal 4990, weight 1200
    Demo->>C: new Checkout(StandardShipping)
    Demo->>C: total(orderA)
    C->>S: cost(orderA)
    S-->>C: 599
    C-->>Demo: 5589 (4990 + 599)
    Demo->>C: setShippingStrategy(ExpressShipping)
    Note over C,E: same Checkout object, new behavior
    Demo->>C: total(orderA)
    C->>E: cost(orderA)
    E-->>C: 1899 (1499 + 200 x 2)
    C-->>Demo: 6889 (4990 + 1899)
```

Caption: the demo prices order A with `StandardShipping` (599 cents, total 5,589), swaps the
strategy on the same `Checkout` object, and prices it again with `ExpressShipping`
(1,899 cents, total 6,889). Source: [`diagrams/checkout-sequence.mmd`](diagrams/checkout-sequence.mmd).

## Mapping back to the generic roles

| Generic role (see [02](02-generic-diagram.md)) | In this example |
| --- | --- |
| Strategy | `ShippingStrategy` (`cost(order)`, `name`) |
| ConcreteStrategy | `StandardShipping`, `ExpressShipping`, `StorePickup`, `FlatRate` lambda |
| Context | `Checkout` (`total(order)`, `setShippingStrategy`) |
| Client | The demo, which picks and swaps strategies |
| Data passed to the strategy | `Order` value object |

The theory behind each role is in [01-pattern-explanation.md](01-pattern-explanation.md).
