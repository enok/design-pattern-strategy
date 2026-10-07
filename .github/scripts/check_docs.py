#!/usr/bin/env python3
"""Docs guard (stdlib only).

1. Every relative Markdown link target in every *.md must exist.
2. Every docs/diagrams/*.mmd must appear verbatim inside a ```mermaid fenced
   block of some docs/*.md file (drift guard).

Usage: check_docs.py [--root DIR] [--self-test]
Exit codes: 0 ok, 1 problems found, 2 usage error.
"""
from __future__ import annotations

import argparse
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

SKIP_DIRS = {".git", "target", "__pycache__"}
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)"
                     r"|!\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")
EXTERNAL_RE = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//)")


def markdown_files(root: Path):
    for p in sorted(root.rglob("*.md")):
        if not any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            yield p


def iter_links(text: str):
    """Yield (line_no, target) for links outside fenced code blocks."""
    fence = None
    for no, line in enumerate(text.splitlines(), 1):
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(2)
            if fence is None:
                fence = marker[0] * len(marker)
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is not None:
            continue
        line = re.sub(r"`[^`]*`", "", line)  # drop inline code
        for lm in LINK_RE.finditer(line):
            yield no, lm.group(1) or lm.group(2)


def check_links(root: Path) -> list[str]:
    problems = []
    for md in markdown_files(root):
        rel = md.relative_to(root)
        for no, target in iter_links(md.read_text(encoding="utf-8")):
            if target.startswith("#") or EXTERNAL_RE.match(target):
                continue
            path_part = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not path_part:
                continue
            base = root if path_part.startswith("/") else md.parent
            dest = (base / path_part.lstrip("/")).resolve()
            if not dest.exists():
                problems.append(f"{rel}:{no}: broken link -> {target}")
    return problems


def mermaid_blocks(text: str) -> list[str]:
    blocks, cur, fence = [], None, None
    for line in text.splitlines():
        m = FENCE_RE.match(line)
        if cur is None:
            if m and line.strip()[len(m.group(2)):].strip().lower() == "mermaid":
                fence, cur = m.group(2), []
            continue
        if m and m.group(2)[0] == fence[0] and len(m.group(2)) >= len(fence) \
                and line.strip() == m.group(2):
            blocks.append("\n".join(cur))
            cur = None
        else:
            cur.append(line)
    return blocks


def _norm(s: str) -> str:
    return s.replace("\r\n", "\n").strip()


def check_diagrams(root: Path) -> list[str]:
    problems = []
    docs = root / "docs"
    diagrams = sorted((docs / "diagrams").glob("*.mmd")) if docs.is_dir() else []
    blocks = []
    if docs.is_dir():
        for md in sorted(docs.glob("*.md")):
            blocks += [_norm(b) for b in mermaid_blocks(md.read_text(encoding="utf-8"))]
    for mmd in diagrams:
        src = _norm(mmd.read_text(encoding="utf-8"))
        if not src:
            problems.append(f"{mmd.relative_to(root)}: diagram file is empty")
        elif not any(src in b for b in blocks):
            problems.append(f"{mmd.relative_to(root)}: content not found in any ```mermaid "
                            f"block of docs/*.md (drift)")
    return problems


SOURCE_RE = re.compile(r"^\s*<!--\s*source:\s*(\S+?)\s*-->\s*$")


def _lf(s: str) -> str:
    s = s.replace("\r\n", "\n")
    return s[:-1] if s.endswith("\n") else s


def check_sources(root: Path) -> list[str]:
    """Fenced blocks right after a `<!-- source: path -->` line must equal that file."""
    problems = []
    for md in markdown_files(root):
        rel = md.relative_to(root)
        lines = md.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
        i = 0
        while i < len(lines):
            m = SOURCE_RE.match(lines[i])
            i += 1
            if not m:
                continue
            path, marker_no = m.group(1), i
            fm = FENCE_RE.match(lines[i]) if i < len(lines) else None
            if not fm:
                problems.append(f"{rel}:{marker_no}: source marker not followed by a fenced block -> {path}")
                continue
            fence, body, j = fm.group(2), [], i + 1
            while j < len(lines):
                cm = FENCE_RE.match(lines[j])
                if cm and cm.group(2)[0] == fence[0] and len(cm.group(2)) >= len(fence) \
                        and lines[j].strip() == cm.group(2):
                    break
                body.append(lines[j])
                j += 1
            i = j + 1
            src = root / path
            if not src.is_file():
                problems.append(f"{rel}:{marker_no}: missing source -> {path}")
            elif _lf(src.read_text(encoding="utf-8")) != _lf("\n".join(body)):
                problems.append(f"{rel}:{marker_no}: code drift -> {path}")
    return problems


def run(root: Path) -> int:
    problems = check_links(root) + check_diagrams(root) + check_sources(root)
    if problems:
        print(f"docs check FAILED: {len(problems)} problem(s)")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("docs check OK")
    return 0


def self_test() -> int:
    here = Path(__file__).resolve().parent
    suite = unittest.defaultTestLoader.discover(str(here), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() and result.testsRun > 0 else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument("--self-test", action="store_true", help="run the unit tests and exit")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.root.is_dir():
        print(f"root not a directory: {args.root}", file=sys.stderr)
        return 2
    return run(args.root.resolve())


if __name__ == "__main__":
    sys.exit(main())
