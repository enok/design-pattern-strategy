import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_docs  # noqa: E402
import gen_code_by_component as gen  # noqa: E402


def fixture(root: Path):
    for _, _, names in gen.COMPONENTS:
        for name in names:
            p = root / gen.SOURCE_DIR / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(f"// {name}\nline 2\n", encoding="utf-8")


class SourceDriftTest(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        (self.root / "a.txt").write_text("x = 1\r\ny = 2\r\n", encoding="utf-8", newline="")

    def page(self, body):
        (self.root / "p.md").write_text(f"<!-- source: a.txt -->\n```text\n{body}\n```\n", encoding="utf-8")

    def test_clean(self):
        self.page("x = 1\ny = 2")
        self.assertEqual(check_docs.check_sources(self.root), [])

    def test_drift(self):
        self.page("x = 1\ny = 3")
        self.assertEqual(check_docs.check_sources(self.root), ["p.md:1: code drift -> a.txt"])

    def test_missing_source(self):
        (self.root / "p.md").write_text("<!-- source: nope.txt -->\n```text\nz\n```\n", encoding="utf-8")
        self.assertEqual(check_docs.check_sources(self.root), ["p.md:1: missing source -> nope.txt"])


class GeneratorTest(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        fixture(self.root)

    def test_output_structure_and_clean_source_check(self):
        self.assertEqual(gen.main(["--root", str(self.root)]), 0)
        text = (self.root / gen.OUTPUT).read_text(encoding="utf-8")
        self.assertEqual(text.count("\n## ") - 1, 5)  # minus the "Components" TOC heading
        self.assertTrue(text.startswith("# Code by component — Java 25\n"))
        files = sum(len(names) for _, _, names in gen.COMPONENTS)
        self.assertEqual(text.count("<!-- source:"), files)
        self.assertEqual(text.count("```java\n"), files)
        self.assertEqual(text.count("<details open>"), 5)
        self.assertEqual(text.count("<details>"), 0)
        self.assertEqual(check_docs.check_sources(self.root), [])

    def test_check_detects_stale_page(self):
        self.assertEqual(gen.main(["--root", str(self.root), "--check"]), 1)  # missing
        gen.main(["--root", str(self.root)])
        self.assertEqual(gen.main(["--root", str(self.root), "--check"]), 0)
        (self.root / gen.SOURCE_DIR / "Order.java").write_text("changed\n", encoding="utf-8")
        self.assertEqual(gen.main(["--root", str(self.root), "--check"]), 1)
        self.assertEqual(len(check_docs.check_sources(self.root)), 1)


if __name__ == "__main__":
    unittest.main()
