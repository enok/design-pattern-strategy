# Strategy pattern: explanation

> Behavioral pattern from the Gang of Four catalog. Study source: *Head First Design Patterns*, 2nd edition, chapter 1.

## In one minute

- **Intent:** define a family of interchangeable algorithms, put each behind a common interface, and let the code that needs one pick it, and even swap it, without changing that code.
- **Smell it cures:** a class that grows another `if`/`switch` branch every time a new variant appears, or a subclass tree that multiplies every time two behaviors combine.
- **Shape:** a `Context` holds a reference to a `Strategy` interface; several `ConcreteStrategy` classes implement it; the client decides which one the context receives.
- **Payoff:** new behavior is added by writing a new class, not by editing the working ones.
- **Price:** more types, and the client must understand the differences between strategies to choose well.

Diagrams: [02-generic-diagram.md](02-generic-diagram.md). A worked, runnable example: [03-application-example.md](03-application-example.md).

## Intent

Strategy lets an object delegate one varying piece of its job to a replaceable collaborator that follows a shared contract.

## The problem it solves

Imagine a class that does something in several ways: compressing files, ranking search results, pricing a delivery. The first draft is usually a method full of conditionals:

```text
if (kind == A) { ...algorithm A... }
else if (kind == B) { ...algorithm B... }
else if (kind == C) { ...algorithm C... }
```

Each new variant reopens a class that already works, risks breaking the other branches, and makes the method harder to test, because every test drags all the branches along.

The inheritance answer is no better. Suppose a base class defines behavior and subclasses override it. That works until variants cross: a subclass needs behavior from two different siblings, or two unrelated subclasses need the same code and you copy it, or a change to the base class silently alters every descendant. The number of subclasses grows with the number of combinations, not the number of ideas. Inheritance fixes the behavior at compile time, so an object also cannot change its mind while running.

Strategy removes both problems by moving each variant out of the class and into its own small object.

## Structure and roles

| Role | Responsibility |
| --- | --- |
| **Context** | The class that needs the algorithm. It keeps a reference typed as the strategy interface and delegates to it. It knows nothing about concrete variants. |
| **Strategy** | The contract: one operation (sometimes a few) that every variant supports. |
| **ConcreteStrategy** | One implementation of the contract, containing a single algorithm. |
| **Client** | The code that creates a concrete strategy and hands it to the context, at construction or later through a setter. The choice lives here, not in the context. |

At runtime the context calls the strategy; the strategy does the work and returns a result. Because the context only sees the interface, the client can replace one strategy with another between calls. See the class and sequence diagrams in [02-generic-diagram.md](02-generic-diagram.md).

## The three design principles from chapter 1

**Encapsulate what varies.** Find the part of the code that changes most often or differs between cases, and pull it out into its own unit, away from the part that stays stable. The stable code stops being touched when the variable part changes. In Strategy, the varying part is the algorithm.

**Program to an interface (a supertype), not to an implementation.** The context declares its collaborator by the abstract type, so it works with anything that honors the contract. Concrete classes can appear, disappear, or be written years later by someone else, and the context compiles untouched. "Interface" here means the contract in general: in Java, an `interface` (often a `@FunctionalInterface`) or an abstract type.

**Favor composition over inheritance.** Instead of getting behavior by being a subclass, an object gets it by holding another object (a has-a relationship). Composition is more flexible: you can assemble behavior from parts, reuse a part in unrelated classes, and exchange it while the program runs. Inheritance is still useful; it is just a heavier, less reversible commitment, so do not reach for it first.

## When to use it

- Several classes differ only in how they perform one task.
- You have a conditional that selects between algorithms and it keeps growing.
- Behavior must be chosen or changed at runtime (configuration, user choice, feature flag, A/B test).
- You want to test each algorithm in isolation, or hide algorithm-specific data from the rest of the code.

## When NOT to use it

- There are only two stable variants that will not grow; a plain `if` is clearer.
- The variants differ in data, not in behavior; a lookup table or a parameter suffices.
- The client cannot reasonably choose between strategies, for example because the differences are internal details you would be forcing it to learn.
- The algorithm is a single stateless operation: a lambda or method reference passed where a functional interface is expected is Strategy without the ceremony (see the comparison below).

## Consequences

**Benefits**
- Open for extension: adding a variant means adding a class, with no edits to the context.
- Conditionals disappear from the context, and each algorithm becomes small and focused.
- Each strategy is independently unit-testable and reusable by other contexts.
- Behavior can change at runtime.

**Costs**
- More classes and indirection for what might be a short `if`.
- The client needs to know the available strategies and how they differ.
- The interface must suit every variant. If one strategy needs inputs the others ignore, the contract gets awkward, or the context passes more data than most strategies use.
- Stateful strategies shared between contexts need care about thread safety.

## Strategy compared with its neighbors

| Pattern or tool | What varies | Who decides | How it differs |
| --- | --- | --- | --- |
| **Strategy** | An algorithm | The client, from outside | Strategies are independent and unaware of each other; the context is passive about the choice. |
| **State** | Behavior that depends on the object's current condition | The state objects themselves, by triggering transitions | Structure is similar, but states know about each other and move the context from one to the next. Strategy has no built-in transitions. |
| **Template Method** | Individual steps inside a fixed algorithm skeleton | Fixed at compile time by subclassing | Uses inheritance, so the variation cannot be swapped on a live object. Strategy replaces the whole algorithm through composition. |
| **Lambda or method reference** | A single operation | The caller | Same idea with less syntax. Prefer it when the strategy is one stateless operation; use classes when strategies carry configuration, several operations, or a name worth documenting. |

## Seen in real libraries

- **JDK:** `java.util.Comparator` passed to `List.sort` or `Collections.sort`. The sorting routine is the context and each comparator is a strategy.
- **Spring Framework:** `PasswordEncoder` implementations (bcrypt, Argon2, and others) are interchangeable hashing strategies.

## Related reading

- Next: [02-generic-diagram.md](02-generic-diagram.md) for the pictures, and [03-application-example.md](03-application-example.md) for a concrete use.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides. *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley, 1994. (Strategy, behavioral patterns chapter.)
2. Eric Freeman and Elisabeth Robson. *Head First Design Patterns*, 2nd edition. O'Reilly Media, 2020. Chapter 1.
3. Refactoring.Guru, "Strategy": <https://refactoring.guru/design-patterns/strategy>
