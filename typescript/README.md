# Strategy pattern: checkout shipping in TypeScript 7

Shipping cost varies (standard, express, pickup, ad-hoc function); the checkout flow does
not. See the full walkthrough in [`../docs/03-application-example.md`](../docs/03-application-example.md).

## Roles to files

| Role | Name | File |
| --- | --- | --- |
| Strategy | `ShippingStrategy` (+ `ShippingCostFn`, `strategyFrom`) | `src/shipping-strategy.ts` |
| ConcreteStrategy | `StandardShipping`, `ExpressShipping`, `StorePickup` | `src/strategies.ts` |
| Ad-hoc strategy | `strategyFrom("Flat rate (lambda)", () => 300)` | `src/demo.ts`, `test/` |
| Context | `Checkout` | `src/checkout.ts` |
| Value object | `Order` | `src/order.ts` |
| Demo | `render()` and main entry | `src/demo.ts` |

`Checkout` takes a `ShippingStrategy`, so a bare function is adapted with
`strategyFrom(name, fn)` (the counterpart of Python's `FunctionStrategy`).

## TypeScript features used

`readonly` fields and properties, `override` (with `noImplicitOverride`), `as const`,
`satisfies` (golden table and rates checked against their shapes), `import type` /
`export type` (`verbatimModuleSyntax`), a function type (`ShippingCostFn`), and an ECMAScript
private field (`#strategy`) in `Checkout`. Types do not guard JavaScript callers, so
`Checkout` also rejects `null`/`undefined` at runtime.

## TypeScript 7 notes

TypeScript 7 is the native (Go) compiler, installed from npm as `typescript@7.0.2`; the
command is still `tsc`. `tsconfig.json` uses only options that survive the 6.0 deprecations:
`target` ES2024, `module`/`moduleResolution` `nodenext`, `strict`, `verbatimModuleSyntax`,
`noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, explicit
`rootDir` and `outDir`, and `types: ["node"]` (type packages are no longer auto-included, so
`@types/node` 24.x is a devDependency for `node:test`). No `es5`, `node10`, `baseUrl` or
`outFile`.

## Run

Requires Node.js 24+.

```text
npm ci
npm test        # build + node --test over dist/test
npm run demo    # build + print the demo output
npm run typecheck
```
