# Strategy Pattern — Head First Design Patterns, Chapter 1

[![CI](https://github.com/enok/design-pattern-strategy/actions/workflows/ci.yml/badge.svg)](https://github.com/enok/design-pattern-strategy/actions/workflows/ci.yml)
![Java 25](https://img.shields.io/badge/Java-25-orange)
![MIT](https://img.shields.io/badge/license-MIT-green)

Strategy is a behavioral design pattern: it puts a family of interchangeable algorithms behind one interface so the code that needs one can use, and even swap, it at runtime without being edited. This repo is one of a series, `enok/design-pattern-<pattern>`, with one repository per pattern. The study source is *Head First Design Patterns*, 2nd edition, by Eric Freeman and Elisabeth Robson (O'Reilly, 2020). All text and code here are original, and the example is written in Java 25.

> **Read the full write-up on Medium:** [What a Checkout’s Shipping Options Taught Me About the Strategy Pattern](https://medium.com/@enok.jesus/what-a-checkouts-shipping-options-taught-me-about-the-strategy-pattern-85e04c2691d5)
>
> **Discuss it on LinkedIn:** [the post sharing this study](https://www.linkedin.com/feed/update/urn:li:share:7513681151757299712/)

## What's inside

| Step | Content | Where |
| --- | --- | --- |
| 1 | Explanation of the pattern | [`docs/01-pattern-explanation.md`](docs/01-pattern-explanation.md) |
| 2 | Generic diagram | [`docs/02-generic-diagram.md`](docs/02-generic-diagram.md) |
| 3 | Application example | [`docs/03-application-example.md`](docs/03-application-example.md) |
| 4 | Diagram of the example | [`docs/04-example-diagram.md`](docs/04-example-diagram.md) |
| 5 | Java 25 code, as a project and component by component | [`java/`](java/) and [`docs/05-code-by-component.md`](docs/05-code-by-component.md) |
| 9 | Architecture perspective | [`docs/09-architecture-perspective.md`](docs/09-architecture-perspective.md) |
| 10 | Best YouTube video for the Java example | [`docs/10-videos.md`](docs/10-videos.md) |

## The pattern beyond the class diagram

Strategy is usually taught as a class diagram, but the same shape appears one level up: a stable core asks a question and one of several interchangeable answers is chosen elsewhere. The picture below shows those architecture-level applications; each one is worked through, with forces and trade-offs, in [`docs/09-architecture-perspective.md`](docs/09-architecture-perspective.md).

![Four architecture-level applications of Strategy: behind a port, runtime policy selection, across service boundaries, pluggable pipeline steps.](docs/diagrams/arch-applications.svg)

Also available as a [PNG](docs/diagrams/arch-applications.png).

## The pattern at a glance

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

- **Strategy (light orange):** the common interface for one varying algorithm.
- **ConcreteStrategy (orange):** one implementation of that algorithm; add a rule by adding a class.
- **Context (green):** holds a strategy by composition and delegates to it; the **client (white)** chooses which one it gets.

## The example in one minute

A checkout prices shipping. The flow (take an order, add shipping, return a total) never changes; only the shipping rule does: standard (599 cents, free from 10,000 cents subtotal), express (1,499 + 200 per started kilogram), store pickup (free), or a promotional flat rate of 300. `Checkout` holds a `ShippingStrategy` and can swap it at runtime. Money is integer cents. The tests assert 16 totals (subtotal + shipping, in cents):

| Order | subtotalCents | weightGrams | Standard | Express | Pickup | Flat 300 |
| --- | --- | --- | --- | --- | --- | --- |
| A | 4_990 | 1_200 | 5_589 | 6_889 | 4_990 | 5_290 |
| B | 10_000 | 1_000 | 10_000 | 11_699 | 10_000 | 10_300 |
| C | 9_999 | 0 | 10_598 | 11_498 | 9_999 | 10_299 |
| D | 25_000 | 3_001 | 25_000 | 27_299 | 25_000 | 25_300 |

Demo output:

```text
Order: subtotal=49.90 weight=1200g
Standard shipping -> shipping 5.99 | total 55.89
Express shipping -> shipping 18.99 | total 68.89
Store pickup -> shipping 0.00 | total 49.90
Flat rate (lambda) -> shipping 3.00 | total 52.90
Swapped at runtime: Standard shipping -> Express shipping | total 55.89 -> 68.89
```

Details: [`docs/03-application-example.md`](docs/03-application-example.md).

## Run it

Toolchain verified on 2026-10-06: JDK 25.0.4.1 (Temurin) with Maven 3.9.16. More detail is in [`java/README.md`](java/README.md).

**Java** (`java/`, needs JDK 25 and Maven 3.9.x)

```text
cd java
mvn -q verify
java -cp target/classes io.github.enok.patterns.strategy.Demo
```

## Video

One pick (English audio, results pulled 2026-10-06): [The Strategy Pattern Explained and Implemented in Java | Behavioral Design Patterns | Geekific](https://www.youtube.com/watch?v=Nrwj3gZiuJU), by Geekific. Backups are in [`docs/10-videos.md`](docs/10-videos.md).

## How this repo is maintained

- `main` is protected: no direct pushes.
- Every change lands through a pull request that must pass two CI checks: `java` (build, tests and demo) and `docs` (link, diagram-drift and code-drift guard).
- The repo is public and read-only for everyone except the owner.

## References

- Eric Freeman and Elisabeth Robson, *Head First Design Patterns*, 2nd edition, O'Reilly Media, 2020, chapter 1.
- Erich Gamma, Richard Helm, Ralph Johnson and John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1994 (the Strategy entry).

## License

[MIT](LICENSE).
