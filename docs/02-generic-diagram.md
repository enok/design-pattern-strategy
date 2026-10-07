# Strategy pattern: generic diagrams

Back to the explanation: [01-pattern-explanation.md](01-pattern-explanation.md). A concrete application: [03-application-example.md](03-application-example.md).

## Class diagram

Source: [diagrams/strategy-generic-class.mmd](diagrams/strategy-generic-class.mmd)

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Arial, Helvetica, sans-serif", "fontSize": "20px", "background": "#FFFFFF", "primaryColor": "#FFFFFF", "primaryBorderColor": "#1B1F23", "primaryTextColor": "#1B1F23", "secondaryColor": "#FDDCB5", "tertiaryColor": "#F5F7FA", "lineColor": "#3D4650", "textColor": "#1B1F23", "mainBkg": "#FFFFFF", "nodeBorder": "#1B1F23", "clusterBkg": "#F5F7FA", "clusterBorder": "#9AA5B1", "edgeLabelBackground": "#FFFFFF", "noteBkgColor": "#FFF6D6", "noteBorderColor": "#B8860B", "noteTextColor": "#1B1F23", "actorBkg": "#B8E2B4", "actorBorder": "#2F6B35", "actorTextColor": "#1B1F23", "actorLineColor": "#7A8794", "signalColor": "#3D4650", "signalTextColor": "#1B1F23", "labelBoxBkgColor": "#F5F7FA", "labelBoxBorderColor": "#7A8794", "labelTextColor": "#1B1F23", "loopTextColor": "#1B1F23", "activationBkgColor": "#DDEFDB", "activationBorderColor": "#2F6B35", "sequenceNumberColor": "#FFFFFF", "classText": "#1B1F23"}, "flowchart": {"curve": "linear", "nodeSpacing": 50, "rankSpacing": 60, "padding": 16, "htmlLabels": false}, "sequence": {"actorMargin": 50, "messageMargin": 38, "boxMargin": 10, "noteMargin": 10, "mirrorActors": false, "useMaxWidth": false}, "class": {"padding": 12, "htmlLabels": false}, "fontFamily": "Arial, Helvetica, sans-serif"}}%%
classDiagram
    direction TB
    class Client {
        -context : Context
        +main() void
    }
    class Context {
        -strategy : Strategy
        +setStrategy(s) void
        +doWork(input) Result
    }
    class Strategy {
        <<interface>>
        +name : String
        +execute(input) Result
    }
    class ConcreteStrategyA {
        -settings : Settings
        +execute(input) Result
    }
    class ConcreteStrategyB {
        -settings : Settings
        +execute(input) Result
    }
    class ConcreteStrategyC {
        -settings : Settings
        +execute(input) Result
    }
    Client ..> Context : uses
    Client ..> ConcreteStrategyA : creates
    Context o-- Strategy : has-a
    Strategy <|.. ConcreteStrategyA : implements
    Strategy <|.. ConcreteStrategyB : implements
    Strategy <|.. ConcreteStrategyC : implements
    style Client fill:#FFFFFF,stroke:#1B1F23,stroke-width:2px
    style Context fill:#B8E2B4,stroke:#2F6B35,stroke-width:2.5px
    style Strategy fill:#FDDCB5,stroke:#B35C0F,stroke-width:2.5px
    style ConcreteStrategyA fill:#F7B267,stroke:#B35C0F,stroke-width:2.5px
    style ConcreteStrategyB fill:#F7B267,stroke:#B35C0F,stroke-width:2.5px
    style ConcreteStrategyC fill:#F7B267,stroke:#B35C0F,stroke-width:2.5px
```

Colour key: green = Context, light orange = Strategy interface, orange = concrete strategies, white = client.

The `Context` owns a field typed as the `Strategy` interface (the hollow diamond marks the has-a relationship), so it depends on the contract and never on a concrete class. Each `ConcreteStrategy` implements that contract with its own algorithm. The `Client` is the only place that names a concrete strategy: it creates one and gives it to the context, either at construction or through `setStrategy`.

## Sequence diagram

Source: [diagrams/strategy-generic-sequence.mmd](diagrams/strategy-generic-sequence.mmd)

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Arial, Helvetica, sans-serif", "fontSize": "20px", "background": "#FFFFFF", "primaryColor": "#FFFFFF", "primaryBorderColor": "#1B1F23", "primaryTextColor": "#1B1F23", "secondaryColor": "#FDDCB5", "tertiaryColor": "#F5F7FA", "lineColor": "#3D4650", "textColor": "#1B1F23", "mainBkg": "#FFFFFF", "nodeBorder": "#1B1F23", "clusterBkg": "#F5F7FA", "clusterBorder": "#9AA5B1", "edgeLabelBackground": "#FFFFFF", "noteBkgColor": "#FFF6D6", "noteBorderColor": "#B8860B", "noteTextColor": "#1B1F23", "actorBkg": "#B8E2B4", "actorBorder": "#2F6B35", "actorTextColor": "#1B1F23", "actorLineColor": "#7A8794", "signalColor": "#3D4650", "signalTextColor": "#1B1F23", "labelBoxBkgColor": "#F5F7FA", "labelBoxBorderColor": "#7A8794", "labelTextColor": "#1B1F23", "loopTextColor": "#1B1F23", "activationBkgColor": "#DDEFDB", "activationBorderColor": "#2F6B35", "sequenceNumberColor": "#FFFFFF", "classText": "#1B1F23"}, "flowchart": {"curve": "linear", "nodeSpacing": 50, "rankSpacing": 60, "padding": 16, "htmlLabels": false}, "sequence": {"actorMargin": 50, "messageMargin": 38, "boxMargin": 10, "noteMargin": 10, "mirrorActors": false, "useMaxWidth": false}, "class": {"padding": 12, "htmlLabels": false}, "fontFamily": "Arial, Helvetica, sans-serif"}}%%
sequenceDiagram
    autonumber
    actor Client
    participant Ctx as Context
    participant A as ConcreteStrategyA
    participant B as ConcreteStrategyB
    rect rgb(245,247,250)
        Note over Client,B: 1 · wire up and run with A
        Client->>A: create
        Client->>Ctx: create with strategy A
        Client->>+Ctx: doWork(input)
        Ctx->>A: execute(input)
        A-->>Ctx: result
        Ctx-->>-Client: result
    end
    rect rgb(245,247,250)
        Note over Client,B: 2 · swap at runtime
        Client->>B: create
        Client->>Ctx: setStrategy(B)
        Client->>+Ctx: doWork(input)
        Ctx->>B: execute(input)
        B-->>Ctx: result
        Ctx-->>-Client: result
    end
```

The client builds strategy A and injects it into the context. When the client asks the context to do its work, the context forwards the call to whatever strategy it currently holds. Later the client creates strategy B and swaps it in; the next call to the same context method now runs algorithm B, with no change to the context itself.

## Role table

| Role | Type | Responsibility | Knows about |
| --- | --- | --- | --- |
| Client | Calling code | Chooses a concrete strategy and injects or swaps it | Context, concrete strategies |
| Context | Class | Does its job by delegating the varying step | Only the `Strategy` interface |
| Strategy | Interface | Declares the operation all variants support | Nothing else |
| ConcreteStrategyA / B / C | Classes | Each implements one algorithm behind the interface | Their own inputs and logic |
