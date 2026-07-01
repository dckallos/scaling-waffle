# Codex Notes Workflow

A small, Git-ready workflow for turning rough learning notes into organized Markdown documentation with Codex.

The workflow is intentionally simple:

1. Capture notes anywhere as plain text, Markdown, pasted text, or piped stdin.
2. Run `codex-add-notes ...` from any directory.
3. Codex reads the current docs outline, verifies technical claims against official documentation, updates the right Markdown page, adds diagrams when useful, and runs deterministic navigation maintenance.

The input notes do **not** need a template. They can be messy bullets, fragments, paragraphs, copied docs snippets, or a normal `.txt` / `.md` file.

## Install for use from anywhere

From your local clone, make the wrapper executable:

```bash
cd ~/dev/scaling-waffle
chmod +x bin/codex-add-notes
```

Add this to `~/.zshrc` so the command works outside `~/dev/scaling-waffle`:

```bash
# codex-add-notes default workspace
export CODEX_ADD_NOTES_REPO="$HOME/dev/scaling-waffle"
export PATH="$CODEX_ADD_NOTES_REPO/bin:$PATH"
```

Then reload your shell:

```bash
source ~/.zshrc
```

Now these work from anywhere:

```bash
codex-add-notes reference ~/Desktop/today-notes.txt
codex-add-notes document ~/notes/airbyte.md
codex-add-notes airflow scheduling and backfill notes
cat ~/Desktop/snowflake-capture.txt | codex-add-notes snowflake loading
```

For a one-off different notes repo, use `--repo`:

```bash
codex-add-notes --repo ~/dev/python-learning reference ~/Desktop/python-notes.txt
```

## Interactive and non-interactive modes

By default, the wrapper launches the interactive Codex TUI. That lets Codex ask one concise clarification question when a note is ambiguous or appears factually wrong.

For an unattended pass, use:

```bash
codex-add-notes --exec reference ~/Desktop/today-notes.txt
```

In non-interactive mode, Codex should not ask questions. Ambiguous or unsupported claims should go to `docs/parking-lot.md` instead.

## What the wrapper does

`bin/codex-add-notes` creates an internal request packet under `.codex-add-notes/requests/`, then starts Codex with:

- the configured notes repo as the workspace;
- `workspace-write` sandboxing;
- live web search enabled by default;
- the `$codex-add-notes` skill as the required workflow.

The request packet is internal plumbing. It copies arbitrary note files into the workspace so the source files can live outside the repo and do not need any special structure.

## How structure stays intact

The workflow uses two layers:

1. **Deterministic scripts** inspect and maintain structure.
   - `scripts/docs/outline.py --json` emits the current docs map before Codex decides where notes belong.
   - `scripts/docs/update_toc.py` regenerates TOCs and the docs index from Markdown headings.
2. **Codex judgment** handles routing, rewriting, correction, diagrams, and official-reference selection.

That gives Codex enough context to make sound decisions without making the docs tree depend on fragile hardcoded topic lists.

## Repo layout

```text
.agents/skills/codex-add-notes/  # Codex skill and reference material
bin/codex-add-notes              # terminal wrapper; can be exported through ~/.zshrc
docs/                            # Markdown learning docs, source of truth
scripts/docs/outline.py           # deterministic docs-outline inspector
scripts/docs/update_toc.py        # deterministic TOC/index updater
tests/                           # tests for deterministic helper scripts and wrapper dry-run behavior
```

## Maintenance commands

```bash
python scripts/docs/outline.py --json
python scripts/docs/update_toc.py
python scripts/docs/update_toc.py --check
python -m unittest discover -s tests
```

Or run everything with:

```bash
make check
```

## Multiple documentation repos

Start with this repo containing both the workflow and your first docs library. That is the least fragile setup.

When you have multiple mature docs repos, use either:

- `CODEX_ADD_NOTES_REPO` for your default repo and `--repo` for one-off repos; or
- move the skill to `$HOME/.agents/skills/codex-add-notes` and keep repo-specific docs structure in each notes repo.

The wrapper already supports the first option. The second option is a later extraction step, not a requirement for getting value now.

## Design boundaries

This repo is for learning-note documentation. The skill may edit Markdown docs, Mermaid diagrams, glossary entries, parking-lot notes, and generated TOCs. It should not commit, push, create pull requests, call warehouses, run production systems, or treat rough notes as authoritative when official docs disagree.
