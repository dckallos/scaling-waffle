from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "docs"))

import update_toc  # noqa: E402


class UpdateTocTests(unittest.TestCase):
    def test_updates_docs_index_and_page_toc(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            docs.mkdir()
            (docs / "README.md").write_text(
                "# Docs\n\n<!-- docs-index:start -->\nstale\n<!-- docs-index:end -->\n",
                encoding="utf-8",
            )
            (docs / "topic.md").write_text(
                "# Topic\n\n<!-- toc:start -->\nstale\n<!-- toc:end -->\n\n## Why it matters\n\n### Example\n",
                encoding="utf-8",
            )

            changes = update_toc.run(docs)
            self.assertEqual({change.reason for change in changes}, {"docs index", "page TOC"})
            readme = (docs / "README.md").read_text(encoding="utf-8")
            topic = (docs / "topic.md").read_text(encoding="utf-8")
            self.assertIn("[Topic](topic.md)", readme)
            self.assertIn("- [Why it matters](#why-it-matters)", topic)
            self.assertIn("  - [Example](#example)", topic)
            self.assertEqual(update_toc.run(docs, check=True), [])

    def test_check_reports_stale_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            docs.mkdir()
            page = docs / "topic.md"
            page.write_text(
                "# Topic\n\n<!-- toc:start -->\nstale\n<!-- toc:end -->\n\n## Fresh Heading\n",
                encoding="utf-8",
            )

            changes = update_toc.run(docs, check=True)
            self.assertEqual(len(changes), 1)
            self.assertEqual(changes[0].reason, "page TOC")
            self.assertIn("stale", page.read_text(encoding="utf-8"))

    def test_ignores_code_fence_headings(self) -> None:
        markdown = "# Topic\n\n```sql\n## not a heading\n```\n\n## Real Heading\n"
        headings = update_toc.headings_for_toc(markdown)
        self.assertEqual(headings, [(2, "Real Heading", "real-heading")])

    def test_skips_private_and_template_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            docs.mkdir()
            (docs / "visible.md").write_text("# Visible\n", encoding="utf-8")
            hidden_dir = docs / "_templates"
            hidden_dir.mkdir()
            (hidden_dir / "concept.md").write_text("# Template\n", encoding="utf-8")
            private_dir = docs / ".private"
            private_dir.mkdir()
            (private_dir / "draft.md").write_text("# Draft\n", encoding="utf-8")

            files = [path.relative_to(docs).as_posix() for path in update_toc.iter_markdown_files(docs)]
            self.assertEqual(files, ["visible.md"])


if __name__ == "__main__":
    unittest.main()
