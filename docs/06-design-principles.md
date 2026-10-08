# Design principles behind Strategy

Strategy is the shape that three object-oriented principles take when they meet one varying algorithm: encapsulate what varies, program to an interface, favor composition over inheritance (the three from chapter 1 of the study source, explained in [01-pattern-explanation.md](01-pattern-explanation.md)). From SOLID it serves the open/closed principle and dependency inversion most. This page checks each principle against this repo's own code and docs, names the participant that realises it, and says where it bends. The class names come from the checkout example ([03](03-application-example.md), [04](04-example-diagram.md)) and the Java 25 source in [`java/`](../java/src/main/java/io/github/enok/patterns/strategy/).

Definitions are the generic, well-known ones. Only the study source is cited (see Sources).

## Principles the pattern realises

Participants: the Context is `Checkout`, the Strategy is `ShippingStrategy`, the concrete strategies are `StandardShipping`, `ExpressShipping`, `StorePickup` (plus a flat-rate lambda), `Order` is the data they read, and the client is `Demo` (in a real application, the composition root plays this part).

| Principle | How (participant or seam) | Where it can be violated |
| --- | --- | --- |
| **SRP** (SOLID): one reason to change | `Checkout` changes only when the checkout flow changes (total = subtotal + shipping). Each concrete strategy owns one pricing rule, so a new express formula touches `ExpressShipping` alone. `Order` only carries and validates two numbers. | A strategy that also formats money for display, logs or adds tax; or `Checkout` starting to pick the strategy itself. |
| **OCP** (SOLID): extend without editing | `ShippingStrategy` is deliberately not sealed. A new rule is a new class, record or lambda passed to `Checkout`, which is never edited (the test `plainLambdaIsAccepted` passes `o -> 300`). | In the selector: the client's list of strategies, or a switch from a user's choice to a strategy, still grows with each option. Also when a new rule needs data `Order` does not carry, so `Order` and its callers change. |
| **LSP** (SOLID): any implementation can stand in | Every concrete strategy and the flat-rate lambda honour the contract that the Javadoc of `ShippingStrategy` states for `cost(Order)`: integer cents, never negative. The golden table runs all four through `Checkout`, weight 0 included (order C). | A strategy that returns a negative amount, throws for an input the others accept (an unsupported region, say), changes units, or needs a call before `cost`. |
| **ISP** (SOLID): depend only on what you use | `Checkout` needs one thing, and the contract has one abstract operation, `cost(Order)`. The default `name()` is for display; `Checkout` never calls it and implementers need not write it. | The interface growing operations only some strategies or contexts need (a delivery estimate, a carrier id), so every implementer supplies them or every context sees them. Already slightly: `name()` serves the demo, not `Checkout`; it is harmless only because it is a default. |
| **DIP** (SOLID): policy depends on abstractions | `Checkout`, the high-level flow, holds a `ShippingStrategy` and names no concrete strategy; the concrete strategies depend on the same interface. Only the client (and the tests) picks a concrete rule and injects it, through the constructor or `setShippingStrategy`. | `Checkout` doing `new StandardShipping()`, testing the strategy's concrete type, or importing a carrier type. |
| **Encapsulate what varies** (object-oriented) | The shipping rule is what changes (new options, a promotion this week, see 03). It sits behind `ShippingStrategy`; the checkout flow stays still. | Hiding something that does not vary, or letting the variation leak into the contract (carrier-specific parameters). |
| **Program to an interface** (object-oriented) | The field, the constructor and the setter of `Checkout` are typed `ShippingStrategy`, so it works with classes written later, a lambda included. | `instanceof` or casts on the strategy, or a variable typed as the concrete class to reach a method the contract lacks. |
| **Favor composition over inheritance** (object-oriented) | `Checkout` has a `ShippingStrategy`, so the rule changes on a live object (in the test `strategyCanBeSwappedAtRuntime` the total for order A goes from 5,589 to 6,889 cents) instead of `ExpressCheckout` and `PickupCheckout` subclasses. `NamedShipping` adds a display name by wrapping a strategy, not by extending one. | Strategies that extend a shared base class to inherit logic (a Template Method in disguise), or one subclass per pair when two concerns vary. |
| **Separation of concerns, cohesion** (general) | Four concerns, four places: the flow (`Checkout`), the rules (the strategies), the data (`Order`) and the choice (the client). Choosing which rule applies is kept apart from using it. | Selection logic creeping into `Checkout`, or a strategy accumulating unrelated rules. |
| **Low coupling, least knowledge** (general) | `Checkout` knows one method, `cost`, and calls methods only on its own field and its parameter. A strategy reads only the accessors of `Order`. No concrete strategy knows another; the one wrapper, `NamedShipping`, holds its delegate only as a `ShippingStrategy`. | Handing a strategy the `Checkout` itself, reaching through a strategy into its internals, or a strategy depending on another concrete strategy. |
| **DRY** (general) | The total is computed in one place, `Checkout.total`, and each pricing rule lives in exactly one class, so no part of the flow is repeated per shipping option. | Two strategies copying a rule they share (say, rounding weight up to started kilograms) instead of sharing it. |
| **Stable abstractions** (architecture) | `Checkout` and every strategy depend on `ShippingStrategy`, and it is the abstract, small type, kept to one abstract operation. The volatile concrete rules are depended on only by the client and the tests. Read here at type level; the original idea is about packages. | A contract that keeps changing (a new parameter for one variant), so every strategy and every context changes with it. |

## Principles that do not apply

- **Dependency rule** (architecture): the example is one package with no inner and outer ring, so the arrows toward `ShippingStrategy` are the DIP row above, not a separate fact. It applies behind a port, where the checkout core owns the contract and carrier adapters point inward (application 1 below).
- **Policy vs detail** (architecture): the participants are all policy (the checkout flow and the pricing rules); the only detail in the example, the demo's console formatting, sits in the client and owes nothing to the pattern. It starts to apply behind a port, where a carrier's wire format is the detail (see below).

Every other principle in the generic checklist is in the table above, or in the next section when the pattern is what puts it at risk (KISS, YAGNI).

## Tension and when not to use it

KISS and YAGNI are the principles Strategy bends when it arrives too early. With two fixed variants that will not grow, such as a flat 599 cents and store pickup forever, `pickup ? 0 : 599` is simpler than an interface, two classes and a selector, and the extra types buy flexibility nobody needs. The conditional does not disappear either: the decision moves out of `Checkout` into the client, so the pattern relocates a branch, it does not remove it. Variation that is only data (a rate table, a threshold) wants a parameter, not a class per row, and a single stateless operation is a lambda, as the flat-rate strategy in the demo is.

The checkout example earns the pattern because it has four rules, one of them a promotion the marketing team wants to try this week (03), each worth testing alone. Rule of thumb, from the [checklist in 09](09-architecture-perspective.md#checklist-is-architectural-strategy-worth-it): use Strategy when at least two real variants exist today (or one is contractually planned), when they change for different reasons or at a different speed than the caller, and when a plain conditional or a configuration value would not do the job just as well. If most of those stay unchecked, keep the simple code and revisit when the variation shows up.

## Architecture-level correlation

[09-architecture-perspective.md](09-architecture-perspective.md) takes the same example through four settings. Each realises a principle at a seam:

| Architecture application | Principle realised | Seam |
| --- | --- | --- |
| 1. Strategy behind a port (hexagonal / clean) | Dependency rule and policy vs detail (DIP at module scale) | The port (`ShippingRatePort`, in domain language) owned by the checkout core; carrier adapters implement it, and the composition root injects one |
| 2. Runtime selection by policy (registry, flag, region) | OCP, and separation of concerns (selecting is not executing) | The strategy registry and the selection policy in front of the Context; a candidate strategy is registered and switched on while the caller stays unedited |
| 3. Strategy across service boundaries | Encapsulate what varies, and low coupling, at service scale; the cost side is KISS and YAGNI | The rate-quote service contract (`quote(order)`) that hides the carriers behind one call, while its answer still reports which strategies ran; 09 keeps strategies in-process unless teams, scaling or data force the hop |
| 4. Pluggable algorithms in data and ML pipelines | LSP: models are interchangeable only if the contract pins down inputs, units and latency | The `predict(features)` contract of the pipeline stage; experiment assignment picks the model and the model id is logged |

Across all four, the contract is the stable abstraction: 09 says to treat the port as a public API, version it, and run one contract-test suite that every strategy, fakes and the fallback included, must pass. The golden table of the example is a small instance of that suite.

## Sources

- Eric Freeman and Elisabeth Robson, *Head First Design Patterns*, 2nd edition, O'Reilly Media, 2020, chapter 1: the three object-oriented principles named above, explained in 01 in original wording.
- No other principle on this page is attributed to a person or quoted.
