# Codex Notes Workflow

A small, Git-ready workflow for turning rough learning notes, minimal topic requests, or interactive intake answers into organized Markdown documentation with Codex.

The workflow is intentionally simple:

1. Capture notes anywhere as plain text, Markdown, pasted text, or piped stdin — or do not capture notes first at all.
2. Run `codex-add-notes ...` from any directory, or run `codex-add-notes` by itself to start an intake session.
3. Codex reads the current docs outline, asks helpful questions when appropriate, verifies technical claims against official documentation, updates the right Markdown page, adds diagrams when useful, and runs deterministic navigation maintenance.

The input notes do **not** need a template. They can be messy bullets, fragments, paragraphs, copied docs snippets, or a normal `.txt` / `.md` file. You can also skip files entirely and give a direct topic request.

## Install for use from anywhere

From your local clone, make the wrapper executable:

```bash
cd ~/dev/scaling-waffle
chmod +x bin/codex-add-notes
```

Add this to `~/.zshrc` so the command works outside `~/dev/scaling-waffle`:

```bash
# scaling-waffle documentation workflow
export CODEX_ADD_NOTES_REPO="$HOME/dev/scaling-waffle"
export PATH="$CODEX_ADD_NOTES_REPO/bin:$PATH"

# Personal alias: use `scaling-waffle` anywhere you would use `codex-add-notes`.
alias scaling-waffle='codex-add-notes'
```

Then reload your shell:

```bash
source ~/.zshrc
```

Now these work from anywhere:

```bash
scaling-waffle
scaling-waffle document ways for me to run Airbyte from my Mac
scaling-waffle reference ~/Desktop/today-notes.txt
scaling-waffle document ~/notes/airbyte.md
scaling-waffle airflow scheduling and backfill notes
cat ~/Desktop/snowflake-capture.txt | scaling-waffle snowflake loading
```

The public script is still named `codex-add-notes`; `scaling-waffle` is only your personal shell alias.

For a one-off different notes repo, use `--repo`:

```bash
scaling-waffle --repo ~/dev/python-learning reference ~/Desktop/python-notes.txt
```

## Ways to start

### 1. Start an intake session

```bash
scaling-waffle
```

This opens interactive Codex and tells it to ask you:

- what you want to add documentation about;
- whether you want specific citations or official docs URLs included, defaulting to no;
- whether you have a preferred destination/topic area, defaulting to auto;
- what depth you want, defaulting to a review-friendly practical overview;
- whether you have rough bullets, examples, constraints, or misconceptions to include.

Codex should not edit files until you answer with at least a topic.

### 2. Give a minimal inline topic

```bash
scaling-waffle document ways for me to run Airbyte from my Mac
```

This does **not** require a Markdown or text file. Codex treats the inline text as the documentation request, checks official docs, then creates or updates the appropriate Markdown page.

### 3. Point at a note file

```bash
scaling-waffle reference ~/Desktop/today-notes.txt
```

The wrapper copies the source file into an ignored internal request packet so Codex can read it inside the workspace. Your source file can live outside the repo and does not need a structure.

### 4. Pipe notes through stdin

```bash
cat ~/Desktop/capture.txt | scaling-waffle dbt source freshness
```

The piped text is captured as raw input.

## Interactive and non-interactive modes

By default, the wrapper launches the interactive Codex TUI. That gives Codex room to ask helpful questions before editing when your request is broad, ambiguous, preference-sensitive, or likely to benefit from user context.

For an unattended pass, use:

```bash
scaling-waffle --exec reference ~/Desktop/today-notes.txt
scaling-waffle --exec document ways for me to run Airbyte from my Mac
```

If you run zero-input non-interactive mode:

```bash
scaling-waffle --exec
```

the wrapper asks a local terminal intake questionnaire first, because `codex exec` is designed for non-interactive scripted runs. After you answer, it launches `codex exec` with those answers preloaded.

In non-interactive mode, Codex should not ask questions. Ambiguous or unsupported claims should go to `docs/parking-lot.md` instead.

## What the wrapper does

`bin/codex-add-notes` creates an internal request packet under `.codex-add-notes/requests/`, then starts Codex with:

- the configured notes repo as the workspace;
- `workspace-write` sandboxing;
- live web search enabled by default;
- the `$codex-add-notes` skill as the required workflow.

The request packet is internal plumbing. It copies arbitrary note files into the workspace so the source files can live outside the repo and do not need any special structure. If you only provide inline intent text, the packet records that as the topic request. If you provide no input in interactive mode, the packet records that Codex should run an intake interview.

The wrapper uses the Codex CLI's interactive TUI for normal sessions and `codex exec` for scripted sessions. The Codex CLI docs describe the interactive `codex` command as launching the terminal UI, and they recommend `--sandbox workspace-write --ask-for-approval on-request` for low-friction local work. The non-interactive docs describe `codex exec` as the scripted/CI entry point and recommend `--sandbox workspace-write` when file edits are needed.

## How structure stays intact

The workflow uses two layers:

1. **Deterministic scripts** inspect and maintain structure.
   - `scripts/docs/outline.py --json` emits the current docs map before Codex decides where notes belong.
   - `scripts/docs/update_toc.py` regenerates TOCs and the docs index from Markdown headings.
2. **Codex judgment** handles routing, rewriting, correction, diagrams, questions, and official-reference selection.

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
