from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "mkdocs"))

import hooks  # noqa: E402


class MkDocsHooksTests(unittest.TestCase):
    def test_builds_file_name_nav_from_folder_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp) / "docs"
            docs.mkdir()
            (docs / "README.md").write_text("# Docs\n", encoding="utf-8")
            (docs / "glossary.md").write_text("# Glossary\n", encoding="utf-8")
            (docs / "_templates").mkdir()
            (docs / "_templates" / "concept.md").write_text("# Template\n", encoding="utf-8")

            airbyte = docs / "airbyte"
            airbyte.mkdir()
            (airbyte / "README.md").write_text("# Airbyte\n", encoding="utf-8")
            (airbyte / "running-on-mac.md").write_text("# Running\n", encoding="utf-8")

            dbt_models = docs / "dbt" / "models"
            dbt_models.mkdir(parents=True)
            (docs / "dbt" / "README.md").write_text("# dbt\n", encoding="utf-8")
            (dbt_models / "ref.md").write_text("# ref\n", encoding="utf-8")

            self.assertEqual(
                [{"docs": hooks.build_file_name_nav(docs)}],
                [
                    {
                        "docs": [
                            {"README.md": "README.md"},
                            {
                                "airbyte": [
                                    {"README.md": "airbyte/README.md"},
                                    {"running-on-mac.md": "airbyte/running-on-mac.md"},
                                ]
                            },
                            {
                                "dbt": [
                                    {"README.md": "dbt/README.md"},
                                    {"models": [{"ref.md": "dbt/models/ref.md"}]},
                                ]
                            },
                            {"glossary.md": "glossary.md"},
                        ]
                    }
                ],
            )


if __name__ == "__main__":
    unittest.main()
