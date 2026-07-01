#!/usr/bin/env python3
"""Update generated Markdown TOCs and the docs index.

The script is dependency-free and intentionally conservative:
- It only changes files that already contain recognized marker blocks.
- It updates `docs/README.md` between docs-index markers.
- It updates per-file heading TOCs between toc markers.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DOCS_INDEX_START = "<!-- docs-index:start -->"
DOCS_INDEX_END = "<!-- docs-index:end -->"
TOC_START = "<!-- toc:start -->"
TOC_END = "<!-- toc:end -->"

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
LINK_TEXT_CLEANUP_RE = re.compile(r"[`*_~]")
SLUG_REMOVE_RE = re.compile(r"[^a-z0-9\s-]")
SLUG_SPACE_RE = re.compile(r"[\s-]+")


@dataclass(frozen=True)
class Change:
    path: Path
    reason: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def iter_markdown_files(docs_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in docs_root.rglob("*.md"):
        if any(part.startswith(".") or part.startswith("_") for part in path.relative_to(docs_root).parts):
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(docs_root).as_posix())


def strip_inline_markdown(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = LINK_TEXT_CLEANUP_RE.sub("", text)
    return text.strip()


def slugify(text: str, seen: dict[str, int]) -> str:
    base = strip_inline_markdown(text).lower()
    base = SLUG_REMOVE_RE.sub("", base)
    base = SLUG_SPACE_RE.sub("-", base).strip("-") or "section"
    count = seen.get(base, 0)
    seen[base] = count + 1
    if count:
        return f"{base}-{count}"
    return base


def headings_for_toc(markdown: str) -> list[tuple[int, str, str]]:
    headings: list[tuple[int, str, str]] = []
    seen: dict[str, int] = {}
    in_code = False
    in_toc = False

    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if stripped == TOC_START:
            in_toc = True
            continue
        if stripped == TOC_END:
            in_toc = False
            continue
        if in_code or in_toc:
            continue

        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = strip_inline_markdown(match.group(2))
        if level == 1 or not title:
            # H1 is the page title; TOCs start at H2.
            continue
        slug = slugify(title, seen)
        headings.append((level, title, slug))
    return headings


def render_toc(markdown: str) -> str:
    headings = headings_for_toc(markdown)
    if not headings:
        return "_No section headings yet._"

    min_level = min(level for level, _, _ in headings)
    lines: list[str] = []
    for level, title, slug in headings:
        indent = "  " * max(level - min_level, 0)
        lines.append(f"{indent}- [{title}](#{slug})")
    return "\n".join(lines)


def first_h1(markdown: str, fallback: str) -> str:
    in_code = False
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) == 1:
            return strip_inline_markdown(match.group(2))
    return fallback


def render_docs_index(docs_root: Path) -> str:
    rows: list[str] = []
    for path in iter_markdown_files(docs_root):
        rel = path.relative_to(docs_root).as_posix()
        if rel == "README.md":
            continue
        title = first_h1(path.read_text(encoding="utf-8"), path.stem.replace("-", " ").title())
        label = rel[:-3]
        rows.append(f"- [{title}]({rel}) `{label}`")
    return "\n".join(rows) if rows else "_No documents yet._"


def replace_marker_block(markdown: str, start: str, end: str, replacement: str) -> tuple[str, bool]:
    if start not in markdown or end not in markdown:
        return markdown, False
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    block = f"{start}\n{replacement.rstrip()}\n{end}"
    updated, count = pattern.subn(block, markdown, count=1)
    return updated, bool(count)


def planned_updates(docs_root: Path) -> list[tuple[Path, str, str]]:
    updates: list[tuple[Path, str, str]] = []

    readme = docs_root / "README.md"
    if readme.exists():
        original = readme.read_text(encoding="utf-8")
        updated, touched = replace_marker_block(original, DOCS_INDEX_START, DOCS_INDEX_END, render_docs_index(docs_root))
        if touched and updated != original:
            updates.append((readme, updated, "docs index"))

    for path in iter_markdown_files(docs_root):
        original = path.read_text(encoding="utf-8")
        if TOC_START not in original or TOC_END not in original:
            continue
        updated, touched = replace_marker_block(original, TOC_START, TOC_END, render_toc(original))
        if touched and updated != original:
            updates.append((path, updated, "page TOC"))

    return updates


def run(docs_root: Path, check: bool = False) -> list[Change]:
    updates = planned_updates(docs_root)
    changes = [Change(path=path, reason=reason) for path, _, reason in updates]
    if check:
        return changes
    for path, updated, _ in updates:
        path.write_text(updated, encoding="utf-8")
    return changes


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update generated Markdown TOCs and docs index.")
    parser.add_argument("--docs-root", default=str(repo_root() / "docs"), help="Docs root to scan. Default: repo/docs")
    parser.add_argument("--check", action="store_true", help="Fail if generated content is stale.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    docs_root = Path(args.docs_root).resolve()
    if not docs_root.exists():
        print(f"error: docs root does not exist: {docs_root}", file=sys.stderr)
        return 2

    changes = run(docs_root, check=args.check)
    if args.check:
        if changes:
            print("Generated Markdown navigation is stale:", file=sys.stderr)
            for change in changes:
                print(f"- {change.path}: {change.reason}", file=sys.stderr)
            print("Run: python scripts/docs/update_toc.py", file=sys.stderr)
            return 1
        print("Generated Markdown navigation is up to date.")
        return 0

    if changes:
        for change in changes:
            print(f"updated {change.path} ({change.reason})")
    else:
        print("Generated Markdown navigation already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
