"""Local MkDocs hooks for the Markdown learning site."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def is_visible_markdown(path: Path, docs_root: Path) -> bool:
    """Return True when a Markdown file should appear in MkDocs navigation."""
    rel_parts = path.relative_to(docs_root).parts
    if any(part.startswith(".") or part.startswith("_") for part in rel_parts):
        return False
    return path.suffix.lower() in {".md", ".markdown", ".mdown", ".mkdn", ".mkd"}


def nav_sort_key(path: Path) -> tuple[int, str]:
    if path.name in {"README.md", "index.md"}:
        return (0, path.name.lower())
    return (1, path.name.lower())


def build_file_name_nav(docs_root: Path, current_dir: Path | None = None) -> list[Any]:
    """Build MkDocs nav entries that mirror docs_root and show file names."""
    docs_root = docs_root.resolve()
    current_dir = docs_root if current_dir is None else current_dir

    entries: list[Any] = []
    children = sorted(current_dir.iterdir(), key=nav_sort_key)

    for child in children:
        if child.name.startswith(".") or child.name.startswith("_"):
            continue

        if child.is_dir():
            nested = build_file_name_nav(docs_root, child)
            if nested:
                entries.append({child.name: nested})
            continue

        if not child.is_file() or not is_visible_markdown(child, docs_root):
            continue

        rel_path = child.relative_to(docs_root).as_posix()
        entries.append({child.name: rel_path})

    return entries


def on_config(config, **kwargs):
    """Replace MkDocs title-based auto nav with source-folder navigation."""
    docs_root = Path(config["docs_dir"])
    config["nav"] = [{docs_root.name: build_file_name_nav(docs_root)}]
    return config
