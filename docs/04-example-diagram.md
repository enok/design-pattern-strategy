# 04 - Example Diagrams

These diagrams show the checkout shipping slice described in
[03-application-example.md](03-application-example.md). For the generic version of the
pattern, see [02-generic-diagram.md](02-generic-diagram.md).

## Class diagram

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Arial, Helvetica, sans-serif", "fontSize": "20px", "background": "#FFFFFF", "primaryColor": "#FFFFFF", "primaryBorderColor": "#1B1F23", "primaryTextColor": "#1B1F23", "secondaryColor": "#FDDCB5", "tertiaryColor": "#F5F7FA", "lineColor": "#3D4650", "textColor": "#1B1F23", "mainBkg": "#FFFFFF", "nodeBorder": "#1B1F23", "clusterBkg": "#F5F7FA", "clusterBorder": "#9AA5B1", "edgeLabelBackground": "#FFFFFF", "noteBkgColor": "#FFF6D6", "noteBorderColor": "#B8860B", "noteTextColor": "#1B1F23", "actorBkg": "#B8E2B4", "actorBorder": "#2F6B35", "actorTextColor": "#1B1F23", "actorLineColor": "#7A8794", "signalColor": "#3D4650", "signalTextColor": "#1B1F23", "labelBoxBkgColor": "#F5F7FA", "labelBoxBorderColor": "#7A8794", "labelTextColor": "#1B1F23", "loopTextColor": "#1B1F23", "activationBkgColor": "#DDEFDB", "activationBorderColor": "#2F6B35", "sequenceNumberColor": "#FFFFFF", "classText": "#1B1F23"}, "flowchart": {"curve": "linear", "nodeSpacing": 50, "rankSpacing": 60, "padding": 16, "htmlLabels": false}, "sequence": {"actorMargin": 50, "messageMargin": 38, "boxMargin": 10, "noteMargin": 10, "mirrorActors": false, "useMaxWidth": false}, "class": {"padding": 12, "htmlLabels": false}, "fontFamily": "Arial, Helvetica, sans-serif"}}%%
classDiagram
    direction TB
    class Client {
        -checkout : Checkout
        +main() void
    }
    class Checkout {
        -strategy : ShippingStrategy
        +total(order) int
        +setShippingStrategy(s)
    }
    class Order {
        <<value object>>
        +subtotalCents : int
        +weightGrams : int
        +Order(cents, grams)
    }
    class ShippingStrategy {
        <<interface>>
        +name : String
        +cost(order) int
    }
    class StandardShipping {
        +name : String
        +cost(order) int
    }
    class ExpressShipping {
        +name : String
        +cost(order) int
    }
    class StorePickup {
        +name : String
        +cost(order) int
    }
    class FlatRate {
        <<lambda>>
        +name : String
        +cost(order) int
    }
    Client ..> Checkout : uses
    Order <.. Checkout : prices
    Checkout o-- ShippingStrategy : has-a
    ShippingStrategy <|.. StandardShipping : implements
    ShippingStrategy <|.. ExpressShipping : implements
    ShippingStrategy <|.. StorePickup : implements
    ShippingStrategy <|.. FlatRate : implements
    style Client fill:#FFFFFF,stroke:#1B1F23,stroke-width:2.5px
    style Checkout fill:#B8E2B4,stroke:#2F6B35,stroke-width:2.5px
    style Order fill:#BBDDF7,stroke:#1F5FA8,stroke-width:2.5px
    style ShippingStrategy fill:#FDDCB5,stroke:#B35C0F,stroke-width:2.5px
    style StandardShipping fill:#F7B267,stroke:#B35C0F,stroke-width:2.5px
    style ExpressShipping fill:#F7B267,stroke:#B35C0F,stroke-width:2.5px
    style StorePickup fill:#F7B267,stroke:#B35C0F,stroke-width:2.5px
    style FlatRate fill:#FFF1D6,stroke:#B35C0F,stroke-width:2.5px,stroke-dasharray:6 4
```

Colour key: green = Context, light orange = Strategy interface, orange = concrete strategies, pale orange dashed = lambda strategy, blue = value object, white = client.

Caption: `Checkout` owns one `ShippingStrategy` by composition and never mentions a concrete
class. The three named strategies and the `FlatRate` lambda all satisfy the same one-method
contract, so any of them can be plugged in. Source: [`diagrams/checkout-class.mmd`](diagrams/checkout-class.mmd).

## Sequence diagram

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Arial, sans-serif", "fontSize": "20px", "background": "#FFFFFF", "primaryColor": "#FFFFFF", "primaryBorderColor": "#1B1F23", "primaryTextColor": "#1B1F23", "secondaryColor": "#FDDCB5", "tertiaryColor": "#F5F7FA", "lineColor": "#3D4650", "textColor": "#1B1F23", "mainBkg": "#FFFFFF", "nodeBorder": "#1B1F23", "clusterBkg": "#F5F7FA", "clusterBorder": "#9AA5B1", "edgeLabelBackground": "#FFFFFF", "noteBkgColor": "#FFF6D6", "noteBorderColor": "#B8860B", "noteTextColor": "#1B1F23", "actorBkg": "#B8E2B4", "actorBorder": "#2F6B35", "actorTextColor": "#1B1F23", "actorLineColor": "#7A8794", "signalColor": "#3D4650", "signalTextColor": "#1B1F23", "labelBoxBkgColor": "#F5F7FA", "labelBoxBorderColor": "#7A8794", "labelTextColor": "#1B1F23", "loopTextColor": "#1B1F23", "activationBkgColor": "#DDEFDB", "activationBorderColor": "#2F6B35", "sequenceNumberColor": "#FFFFFF", "classText": "#1B1F23"}, "flowchart": {"curve": "linear", "nodeSpacing": 50, "rankSpacing": 60, "padding": 16, "htmlLabels": false}, "sequence": {"actorMargin": 50, "messageMargin": 38, "boxMargin": 10, "noteMargin": 10, "mirrorActors": false, "useMaxWidth": false}, "class": {"padding": 12, "htmlLabels": false}, "fontFamily": "Inter, Arial, sans-serif"}}%%
sequenceDiagram
    autonumber
    participant Demo as Client (Demo)
    participant C as Checkout
    participant S as StandardShipping
    participant E as ExpressShipping
    rect rgb(245,247,250)
        Note over Demo,E: 1 · price with Standard
        Demo->>C: new Checkout(StandardShipping)
        Demo->>+C: total(orderA)
        C->>S: cost(orderA)
        S-->>C: 599
        C-->>-Demo: 5589
    end
    rect rgb(245,247,250)
        Note over Demo,E: 2 · swap at runtime
        Demo->>C: setShippingStrategy(ExpressShipping)
        Demo->>+C: total(orderA)
        C->>E: cost(orderA)
        E-->>C: 1899
        C-->>-Demo: 6889
    end
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
