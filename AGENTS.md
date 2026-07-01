# Agent Instructions

This repository is a Markdown-first learning system. It can hold notes for any technical topic, including technologies that do not yet have a folder in `docs/`.

When the user asks to add, refine, document, organize, review, reference, polish, or convert rough notes, use the `$codex-add-notes` skill.

## Documentation rules

- Treat user notes as rough, possibly incomplete, and possibly wrong.
- Do not require any structure in source notes. They may be bullets, fragments, pasted prose, transcripts, or mixed Markdown/Text.
- Verify technical claims against official documentation before incorporating them as fact.
- Prefer official docs for the named product or project. If the product is new to this repo, find its official docs instead of forcing the note into an existing dbt/Snowflake area.
- Preserve the user's intended learning goal, but correct inaccuracies gently.
- Prefer organized prose with examples over raw bullet lists.
- Use Mermaid diagrams only when they improve understanding of lineage, DAGs, control flow, architecture, state transitions, or data movement.
- Run `python scripts/docs/outline.py --json` before broad organization or routing decisions.
- Update local links, glossary entries, and generated TOCs/indexes after documentation edits.
- Put unresolved, ambiguous, or unverified claims in `docs/parking-lot.md` with enough context to revisit them later.

## Write boundaries

Allowed by default:

- Create or update Markdown files under `docs/`.
- Create new `docs/<technology>/` areas for named tools when no existing area fits.
- Create or update Mermaid diagrams under `docs/` when useful.
- Run `python scripts/docs/outline.py`, `python scripts/docs/update_toc.py`, and related local tests.
- Read Git status or diffs to summarize changed files.

Not allowed unless the user explicitly asks for that exact action:

- Commit, push, tag, branch, or open pull requests.
- Mutate GitHub issues, pull requests, labels, projects, or milestones.
- Run warehouse, production, destructive, credentialed, deployment, or network write operations.
- Treat LLM output, rough notes, or third-party blog posts as a source of truth when official docs are available.
