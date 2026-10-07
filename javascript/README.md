# Strategy pattern - JavaScript (ES2026 baseline, Node 24)

Checkout shipping-cost example. Full walkthrough: [../docs/03-application-example.md](../docs/03-application-example.md).

## Roles -> files

| Role | File |
| --- | --- |
| Strategy (duck-typed `@typedef`) + function adapter `strategyFrom` | `src/shipping-strategy.js` |
| ConcreteStrategies `StandardShipping`, `ExpressShipping`, `StorePickup` | `src/strategies.js` |
| Value object `Order` (private `#fields`, frozen) | `src/order.js` |
| Context `Checkout` (private `#strategy`, `setShippingStrategy`) | `src/checkout.js` |
| Demo (`render()`) | `src/demo.js` |
| Tests (16 golden totals, swap, validation, demo text) | `test/checkout.test.js` |

## Modern features used

| Feature | Edition | Node 24 | Source |
| --- | --- | --- | --- |
| Iterator helpers (`values().map(...)`) in `demo.js` | ES2025 | yes (V8 13.6) | [MDN: Iterator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Iterator), [TC39 finished proposals](https://github.com/tc39/proposals/blob/main/finished-proposals.md) |
| Private fields and methods (`#x`, `static #check`) | ES2022 | yes | [MDN: Private properties](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_properties), [TC39 finished proposals](https://github.com/tc39/proposals/blob/main/finished-proposals.md) |
| Static class fields | ES2022 | yes | [MDN: static](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/static) |

Edition reference: [ECMA-262, 16th edition (ES2025)](https://262.ecma-international.org/16.0/).
JSDoc `@import` is a TypeScript-tooling comment, not a runtime feature.

ES2026 additions such as `Error.isError` and `Math.sumPrecise` are deliberately NOT used, to stay within
what Node 24 (V8 13.6) is expected to ship; check the TC39 list above for their stage and your Node version.
Money stays integer cents, so no precise summation is needed.

## Run

```bash
cd javascript
npm test        # node --test
npm run demo    # node src/demo.js
```
