# Strategy pattern: checkout shipping (Python)

Python 3.13 implementation (runs on 3.12+, stdlib only) of the shared example in
[`../docs/03-application-example.md`](../docs/03-application-example.md).

## Roles to modules

| Role | Where |
| --- | --- |
| Strategy | `ShippingStrategy` (`typing.Protocol`) in `src/checkout_strategy/shipping_strategy.py` |
| ConcreteStrategy | `StandardShipping`, `ExpressShipping`, `StorePickup` in `strategies.py` |
| Ad-hoc strategy / adapter | `FunctionStrategy(name, fn)` in `shipping_strategy.py` |
| Context | `Checkout` in `checkout.py` |
| Value object | `Order` in `order.py` |
| Client | `demo.py` (`render()`) and `__main__.py` |

## Python features used

- `typing.Protocol`: open, structural Strategy (no inheritance needed).
- `typing.override` (3.12) on concrete `cost` methods.
- `@dataclass(frozen=True, slots=True)` with `__post_init__` validation.
- Integer ceiling division `-(-w // 1000)`: no floats for money or weights.
- `collections.abc.Callable`, `X | None` unions, named constants, full type hints.
- Property setter to swap the strategy at runtime.

Errors: `Order` raises `ValueError` for negatives (`TypeError` for non-ints);
`Checkout` raises `TypeError` for `None`.

## Run

```bash
cd python
PYTHONPATH=src python -m checkout_strategy
PYTHONPATH=src python -m unittest discover -s tests -t .
```
