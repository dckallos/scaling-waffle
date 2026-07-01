# Codex Notes Workflow

A small, Git-ready starter repo for turning rough dbt, Snowflake, SQL, and data-engineering notes into organized Markdown learning docs with Codex.

The workflow is intentionally simple:

1. Put notes in this repo as `.md` or `.txt`, paste them into the wrapper, or type a short request.
2. Run `codex-add-notes ...` from your terminal, or invoke `$codex-add-notes ...` inside Codex.
3. Codex verifies claims against official documentation, updates the right Markdown file, adds diagrams when they clarify the concept, and runs the deterministic TOC updater.

## Quick start

```bash
git init
chmod +x bin/codex-add-notes
export PATH="$PWD/bin:$PATH"
```

Then use any of these forms:

```bash
codex-add-notes dbt: create a couple paragraphs on the potential of the ref function to ensure the table in the ref is created before the model that uses ref
codex-add-notes reference today-notes.txt
codex-add-notes document dbt bullet points from dbt-notes.md
cat today-notes.txt | codex-add-notes dbt sources and freshness
```

By default, the wrapper launches an interactive Codex session so Codex can ask a clarification question before editing when your notes are ambiguous or appear factually wrong.

For an unattended pass, use:

```bash
codex-add-notes --exec document dbt bullet points from dbt-notes.md
```

In non-interactive mode, Codex should not ask questions. Ambiguous or unsupported claims should go to `docs/parking-lot.md` instead.

## What the wrapper does

`bin/codex-add-notes` creates a small request manifest in `.codex-add-notes/requests/`, then starts Codex with:

- the repo as the workspace;
- `workspace-write` sandboxing;
- live web search enabled;
- the repo-scoped `$codex-add-notes` skill as the required workflow.

The manifest keeps large note files out of the command-line prompt and lets Codex read the files directly from the repo.

## Repo layout

```text
.agents/skills/codex-add-notes/  # Codex skill and reference material
bin/codex-add-notes              # terminal wrapper
docs/                            # Markdown learning docs, source of truth
scripts/docs/update_toc.py        # deterministic TOC/index updater
tests/                           # tests for deterministic helper scripts
```

## Maintenance commands

```bash
python scripts/docs/update_toc.py
python scripts/docs/update_toc.py --check
python -m unittest discover -s tests
```

Or run everything with:

```bash
make check
```

## Design boundaries

This repo is for learning-note documentation. The skill may edit Markdown docs, Mermaid diagrams, glossary entries, and generated TOCs. It should not commit, push, create pull requests, call warehouses, run dbt against production, or treat rough notes as authoritative when official docs disagree.
