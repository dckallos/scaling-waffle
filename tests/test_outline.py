from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "docs"))

import outline  # noqa: E402


class OutlineTests(unittest.TestCase):
    def test_builds_json_ready_outline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            docs.mkdir()
            (docs / "README.md").write_text("# Docs\n", encoding="utf-8")
            area = docs / "airflow"
            area.mkdir()
            (area / "README.md").write_text("# Airflow Notes\n", encoding="utf-8")
            (area / "scheduling.md").write_text(
                "# Scheduling\n\n<!-- toc:start -->\n<!-- toc:end -->\n\n## DAGs\n\nSee [Airflow Notes](README.md).\n",
                encoding="utf-8",
            )

            result = outline.outline_to_dict(outline.build_outline(docs))
            self.assertEqual(result["document_count"], 3)
            self.assertIn({"name": "airflow", "readme": "airflow/README.md", "document_count": 2}, result["top_level_areas"])
            scheduling = next(document for document in result["documents"] if document["path"] == "airflow/scheduling.md")
            self.assertEqual(scheduling["title"], "Scheduling")
            self.assertEqual(scheduling["headings"][0]["title"], "DAGs")
            self.assertEqual(scheduling["links"][0]["kind"], "internal")

    def test_cli_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            docs.mkdir()
            (docs / "README.md").write_text("# Docs\n", encoding="utf-8")
            script = REPO_ROOT / "scripts" / "docs" / "outline.py"
            completed = subprocess.run(
                [sys.executable, str(script), "--docs-root", str(docs), "--json"],
                check=True,
                text=True,
                capture_output=True,
            )
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["document_count"], 1)
            self.assertEqual(payload["documents"][0]["path"], "README.md")


if __name__ == "__main__":
    unittest.main()
