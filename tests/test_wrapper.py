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

            request_json = self._request_json_path(workspace, completed.stdout)
            payload = json.loads(request_json.read_text(encoding="utf-8"))
            copied = workspace / payload["input_files"][0]["copied_path"]
            self.assertTrue(copied.exists())
            self.assertIn("no template", copied.read_text(encoding="utf-8"))
            self.assertEqual(payload["docs_root"], "docs")

    def test_dry_run_accepts_inline_topic_without_note_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()

            completed = subprocess.run(
                [
                    str(WRAPPER),
                    "--dry-run",
                    "--repo",
                    str(workspace),
                    "document",
                    "ways",
                    "for",
                    "me",
                    "to",
                    "run",
                    "Airbyte",
                    "from",
                    "my",
                    "Mac",
                ],
                check=True,
                input="",
                text=True,
                capture_output=True,
            )

            request_json = self._request_json_path(workspace, completed.stdout)
            payload = json.loads(request_json.read_text(encoding="utf-8"))
            intent = (workspace / payload["intent_file"]).read_text(encoding="utf-8")
            self.assertEqual(payload["input_mode"], "inline_topic")
            self.assertEqual(payload["input_files"], [])
            self.assertIn("document ways for me to run Airbyte from my Mac", intent)
            self.assertIn("Do not require a source document", completed.stdout)

    def test_dry_run_without_args_starts_codex_interview(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()

            completed = subprocess.run(
                [str(WRAPPER), "--dry-run", "--repo", str(workspace)],
                check=True,
                input="",
                text=True,
                capture_output=True,
            )

            request_json = self._request_json_path(workspace, completed.stdout)
            payload = json.loads(request_json.read_text(encoding="utf-8"))
            self.assertEqual(payload["input_mode"], "codex_interview")
            self.assertEqual(payload["input_files"], [])
            self.assertIn("What do you want to add documentation about?", completed.stdout)
            self.assertIn("Do not edit files until the user answers", completed.stdout)

    def test_dry_run_exec_without_args_records_unanswered_intake_when_no_tty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()

            completed = subprocess.run(
                [str(WRAPPER), "--dry-run", "--repo", str(workspace), "--exec"],
                check=True,
                input="",
                text=True,
                capture_output=True,
            )

            request_json = self._request_json_path(workspace, completed.stdout)
            payload = json.loads(request_json.read_text(encoding="utf-8"))
            self.assertEqual(payload["input_mode"], "shell_intake_unanswered")
            self.assertIsNotNone(payload["intake_file"])
            self.assertIn("would ask local shell intake questions", completed.stdout)

    @staticmethod
    def _request_json_path(workspace: Path, stdout: str) -> Path:
        request_json_line = next(line for line in stdout.splitlines() if line.startswith("request_json="))
        return workspace / request_json_line.split("=", 1)[1]


if __name__ == "__main__":
    unittest.main()
