#!/usr/bin/env python3
"""Inspect the Markdown docs tree and emit a deterministic outline.

This script gives Codex a compact, current map of the documentation library before
it decides where new notes belong. It performs no network calls and does not write
files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import update_toc

LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


@dataclass(frozen=True)
class Heading:
    level: int
    title: str
    slug: str


@dataclass(frozen=True)
class Link:
    text: str
    target: str
    kind: str


@dataclass(frozen=True)
class Document:
    path: str
    title: str
    headings: list[Heading]
    links: list[Link]
    has_toc_markers: bool


@dataclass(frozen=True)
class TopLevelArea:
    name: str
    readme: str | None
    document_count: int


@dataclass(frozen=True)
class Outline:
    docs_root: str
    document_count: int
    top_level_areas: list[TopLevelArea]
    documents: list[Document]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def without_code_fences(markdown: str) -> str:
    lines: list[str] = []
    in_code = False
    for line in markdown.splitlines():
        if FENCE_RE.match(line):
            in_code = not in_code
            continue
        if not in_code:
            lines.append(line)
    return "\n".join(lines)


def classify_link(target: str) -> str:
    stripped = target.strip()
    if stripped.startswith(("http://", "https://")):
        return "external"
    if stripped.startswith("#"):
        return "anchor"
    return "internal"


def markdown_links(markdown: str) -> list[Link]:
    visible = without_code_fences(markdown)
    links: list[Link] = []
    for match in LINK_RE.finditer(visible):
        text = update_toc.strip_inline_markdown(match.group(1))
        target = match.group(2).strip()
        links.append(Link(text=text, target=target, kind=classify_link(target)))
    return links


def document_for_path(path: Path, docs_root: Path) -> Document:
    markdown = path.read_text(encoding="utf-8")
    rel = path.relative_to(docs_root).as_posix()
    fallback = path.stem.replace("-", " ").title()
    headings = [Heading(level=level, title=title, slug=slug) for level, title, slug in update_toc.headings_for_toc(markdown)]
    return Document(
        path=rel,
        title=update_toc.first_h1(markdown, fallback),
        headings=headings,
        links=markdown_links(markdown),
        has_toc_markers=update_toc.TOC_START in markdown and update_toc.TOC_END in markdown,
    )


def build_top_level_areas(docs_root: Path, documents: list[Document]) -> list[TopLevelArea]:
    counts: dict[str, int] = {}
    readmes: dict[str, str] = {}

    for document in documents:
        parts = document.path.split("/")
        if len(parts) == 1:
            area = "root"
        else:
            area = parts[0]
        counts[area] = counts.get(area, 0) + 1
        if parts[-1] == "README.md":
            readmes[area] = document.path

    areas = [
        TopLevelArea(name=name, readme=readmes.get(name), document_count=counts[name])
        for name in sorted(counts)
    ]
    return areas


def build_outline(docs_root: Path) -> Outline:
    docs_root = docs_root.resolve()
    documents = [document_for_path(path, docs_root) for path in update_toc.iter_markdown_files(docs_root)]
    return Outline(
        docs_root=docs_root.as_posix(),
        document_count=len(documents),
        top_level_areas=build_top_level_areas(docs_root, documents),
        documents=documents,
    )


def outline_to_dict(outline: Outline) -> dict[str, Any]:
    return asdict(outline)


def render_text(outline: Outline) -> str:
    lines: list[str] = []
    lines.append(f"Docs root: {outline.docs_root}")
    lines.append(f"Documents: {outline.document_count}")
    lines.append("")
    lines.append("Top-level areas:")
    if outline.top_level_areas:
        for area in outline.top_level_areas:
            readme = f", README: {area.readme}" if area.readme else ""
            lines.append(f"- {area.name}: {area.document_count} document(s){readme}")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("Documents:")
    if outline.documents:
        for document in outline.documents:
            lines.append(f"- {document.path}: {document.title}")
            for heading in document.headings[:8]:
                lines.append(f"  - H{heading.level} {heading.title}")
            if len(document.headings) > 8:
                lines.append(f"  - ... {len(document.headings) - 8} more heading(s)")
    else:
        lines.append("- None")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit a deterministic outline of Markdown docs.")
    parser.add_argument("--docs-root", default=str(repo_root() / "docs"), help="Docs root to scan. Default: repo/docs")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a text outline.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    docs_root = Path(args.docs_root).resolve()
    if not docs_root.exists():
        print(f"error: docs root does not exist: {docs_root}", file=sys.stderr)
        return 2

    outline = build_outline(docs_root)
    if args.json:
        print(json.dumps(outline_to_dict(outline), indent=2, sort_keys=True))
    else:
        print(render_text(outline))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
