import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_docs  # noqa: E402

MMD = "flowchart LR\n  A --> B\n"


def make(root: Path, files: dict[str, str]):
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")


class CheckDocsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_valid_repo_passes(self):
        make(self.root, {
            "README.md": "[doc](docs/a.md) [web](https://x.io) [m](mailto:a@b.c) [h](#top)\n",
            "docs/a.md": "[back](../README.md#top)\n```mermaid\n" + MMD + "```\n",
            "docs/diagrams/a.mmd": MMD,
        })
        self.assertEqual(check_docs.run(self.root), 0)

    def test_broken_link_reported(self):
        make(self.root, {"README.md": "[x](docs/missing.md)\n"})
        problems = check_docs.check_links(self.root)
        self.assertEqual(len(problems), 1)
        self.assertIn("docs/missing.md", problems[0])
        self.assertEqual(check_docs.run(self.root), 1)

    def test_links_in_code_fences_ignored(self):
        make(self.root, {"README.md": "```\n[x](nope.md)\n```\n`[y](nope2.md)`\n"})
        self.assertEqual(check_docs.check_links(self.root), [])

    def test_diagram_drift_detected(self):
        make(self.root, {
            "docs/a.md": "```mermaid\nflowchart LR\n  A --> C\n```\n",
            "docs/diagrams/a.mmd": MMD,
        })
        self.assertEqual(len(check_docs.check_diagrams(self.root)), 1)

    def test_diagram_in_non_mermaid_fence_rejected(self):
        make(self.root, {
            "docs/a.md": "```text\n" + MMD + "```\n",
            "docs/diagrams/a.mmd": MMD,
        })
        self.assertEqual(len(check_docs.check_diagrams(self.root)), 1)

    def test_cli_self_test_flag_and_bad_root(self):
        self.assertEqual(check_docs.main(["--root", str(self.root / "nope")]), 2)


if __name__ == "__main__":
    unittest.main()
