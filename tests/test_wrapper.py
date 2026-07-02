from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WRAPPER = REPO_ROOT / "bin" / "codex-add-notes"
DOCS_PREVIEW = REPO_ROOT / "bin" / "docs-preview"


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


class DocsPreviewWrapperTests(unittest.TestCase):
    def test_help_succeeds(self) -> None:
        completed = subprocess.run(
            [str(DOCS_PREVIEW), "--help"],
            check=True,
            text=True,
            capture_output=True,
        )
        self.assertIn("Usage:", completed.stdout)
        self.assertIn("--restart", completed.stdout)

    def test_dry_run_reports_bold_url_without_starting_server(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            self._write_minimal_preview_workspace(workspace)

            completed = subprocess.run(
                [str(DOCS_PREVIEW), "--dry-run", "--repo", str(workspace), "--port", "8123"],
                check=True,
                text=True,
                capture_output=True,
            )

            self.assertIn("dry_run=1", completed.stdout)
            self.assertIn("check_needed=yes", completed.stdout)
            self.assertIn("Available at: \x1b[1mhttp://127.0.0.1:8123/\x1b[0m", completed.stdout)
            self.assertFalse((workspace / ".mkdocs-preview").exists())

    def test_dry_run_fingerprint_changes_for_relevant_file_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            self._write_minimal_preview_workspace(workspace)

            before = subprocess.run(
                [str(DOCS_PREVIEW), "--dry-run", "--repo", str(workspace), "--port", "8124"],
                check=True,
                text=True,
                capture_output=True,
            )

            (workspace / "docs" / "README.md").write_text("# Docs\n\nChanged.\n", encoding="utf-8")

            after = subprocess.run(
                [str(DOCS_PREVIEW), "--dry-run", "--repo", str(workspace), "--port", "8124"],
                check=True,
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(
                self._stdout_value(before.stdout, "check_fingerprint"),
                self._stdout_value(after.stdout, "check_fingerprint"),
            )

    @staticmethod
    def _write_minimal_preview_workspace(workspace: Path) -> None:
        workspace.mkdir()
        (workspace / "docs").mkdir()
        (workspace / "scripts" / "docs").mkdir(parents=True)
        (workspace / "scripts" / "mkdocs").mkdir(parents=True)
        (workspace / "tests").mkdir()
        (workspace / "docs" / "README.md").write_text("# Docs\n", encoding="utf-8")
        (workspace / "mkdocs.yml").write_text("site_name: Test\n", encoding="utf-8")
        (workspace / "Makefile").write_text("check:\n\t@true\n", encoding="utf-8")
        (workspace / "pyproject.toml").write_text("[project]\nname = \"test\"\nversion = \"0.0.0\"\n", encoding="utf-8")
        (workspace / "uv.lock").write_text("", encoding="utf-8")

    @staticmethod
    def _stdout_value(stdout: str, key: str) -> str:
        prefix = f"{key}="
        return next(line for line in stdout.splitlines() if line.startswith(prefix)).split("=", 1)[1]


if __name__ == "__main__":
    unittest.main()
