from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WRAPPER = REPO_ROOT / "bin" / "codex-add-notes"


class WrapperTests(unittest.TestCase):
    def test_dry_run_copies_external_note_without_requiring_note_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            external = Path(tmp) / "rough notes.txt"
            external.write_text("random bullets\n- no template\n- airflow scheduling\n", encoding="utf-8")

            completed = subprocess.run(
                [str(WRAPPER), "--dry-run", "--repo", str(workspace), "reference", str(external)],
                check=True,
                input="",
                text=True,
                capture_output=True,
            )

            request_json_line = next(line for line in completed.stdout.splitlines() if line.startswith("request_json="))
            request_json = workspace / request_json_line.split("=", 1)[1]
            payload = json.loads(request_json.read_text(encoding="utf-8"))
            copied = workspace / payload["input_files"][0]["copied_path"]
            self.assertTrue(copied.exists())
            self.assertIn("no template", copied.read_text(encoding="utf-8"))
            self.assertEqual(payload["docs_root"], "docs")


if __name__ == "__main__":
    unittest.main()
