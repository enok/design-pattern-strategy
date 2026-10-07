#!/usr/bin/env python3
"""Generate docs/05-code-by-component.md from the component file table (stdlib only).

Usage: gen_code_by_component.py [--root DIR] [--check]
Default writes the page; --check exits 1 if the file on disk differs from the
generated text (or is missing). Exit codes: 0 ok, 1 stale/missing/source error, 2 usage.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

OUTPUT = "docs/05-code-by-component.md"

LANGUAGE = "Java 25"
FENCE_LANG = "java"
SOURCE_DIR = "java/src/main/java/io/github/enok/patterns/strategy/"

# (title, pattern role sentence, [file names])
COMPONENTS = [
    ("Strategy interface",
     "The Strategy declares the single operation every interchangeable algorithm must offer.",
     ["ShippingStrategy.java", "NamedShipping.java"]),
    ("Concrete strategies",
     "Each ConcreteStrategy implements one shipping-cost algorithm behind the Strategy contract.",
     ["StandardShipping.java", "ExpressShipping.java", "StorePickup.java"]),
    ("Value object",
     "The immutable Order is the data every strategy prices; it validates its own invariants.",
     ["Order.java"]),
    ("Context",
     "The Checkout holds a Strategy by composition, delegates pricing to it and lets it be swapped at runtime.",
     ["Checkout.java"]),
    ("Client (demo)",
     "The client picks strategies, hands them to the context and shows the runtime swap.",
     ["Demo.java"]),
]


def anchor(text: str) -> str:
    return re.sub(r"[^a-z0-9 -]", "", text.lower()).replace(" ", "-")


def fence_for(code: str) -> str:
    longest = max((len(m) for m in re.findall(r"`+", code)), default=0)
    return "`" * max(3, longest + 1)


def generate(root: Path) -> str:
    out = [f"# Code by component — {LANGUAGE}", ""]
    out += [
        "This page reads the Strategy example component by component: for each role in the "
        "pattern you see the Java source, in a collapsible section. The files are shown whole "
        "and are generated from the source tree, so they cannot drift. Build and run commands "
        "are in [`java/`](../java/) ([README](../java/README.md)).",
        "",
        "## Components",
        "",
    ]
    for n, (title, _, _) in enumerate(COMPONENTS, 1):
        out.append(f"{n}. [{title}](#{anchor(f'{n}. {title}')})")
    out.append("")
    for n, (title, role, names) in enumerate(COMPONENTS, 1):
        code_names = ", ".join(f"<code>{x}</code>" for x in names)
        out += [f"## {n}. {title}", "", role, "",
                "<details open>",
                f"<summary><b>{LANGUAGE}</b> · {code_names}</summary>", ""]
        for name in names:
            rel = SOURCE_DIR + name
            path = root / rel
            if not path.is_file():
                raise FileNotFoundError(rel)
            code = path.read_text(encoding="utf-8").replace("\r\n", "\n")
            code = code[:-1] if code.endswith("\n") else code
            fence = fence_for(code)
            out += [f"<!-- source: {rel} -->", f"{fence}{FENCE_LANG}", code, fence, ""]
        out += ["</details>", ""]
    return "\n".join(out).rstrip("\n") + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument("--check", action="store_true", help="fail if the page on disk is stale")
    args = ap.parse_args(argv)
    if not args.root.is_dir():
        print(f"root not a directory: {args.root}", file=sys.stderr)
        return 2
    root = args.root.resolve()
    try:
        text = generate(root)
    except FileNotFoundError as e:
        print(f"missing source -> {e}", file=sys.stderr)
        return 1
    target = root / OUTPUT
    if args.check:
        current = target.read_bytes().decode("utf-8").replace("\r\n", "\n") if target.is_file() else None
        if current != text:
            print(f"{OUTPUT} is stale or missing; run: python .github/scripts/gen_code_by_component.py")
            return 1
        print(f"{OUTPUT} up to date")
        return 0
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
