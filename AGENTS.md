# Agent Instructions

This repository is a Markdown-first learning system for dbt, Snowflake, SQL, analytics engineering, and adjacent data tooling.

When the user asks to add, refine, document, organize, reference, polish, or convert rough notes, use the repo-scoped `$codex-add-notes` skill.

## Documentation rules

- Treat user notes as rough, possibly incomplete, and possibly wrong.
- Verify technical claims against official documentation before incorporating them as fact.
- Prefer official docs domains such as `docs.getdbt.com`, `docs.snowflake.com`, and the official docs for any other named tool.
- Preserve the user's intended learning goal, but correct inaccuracies gently.
- Prefer organized prose with examples over raw bullet lists.
- Use Mermaid diagrams only when they improve understanding of lineage, DAGs, control flow, architecture, or data movement.
- Update local links, glossary entries, and the generated TOC/index after documentation edits.
- Put unresolved, ambiguous, or unverified claims in `docs/parking-lot.md` with enough context to revisit them later.

## Write boundaries

Allowed by default:

- Create or update Markdown files under `docs/`.
- Create or update Mermaid diagrams under `docs/` when useful.
- Run `python scripts/docs/update_toc.py` and related local tests.
- Read Git status or diffs to summarize changed files.

Not allowed unless the user explicitly asks for that exact action:

- Commit, push, tag, branch, or open pull requests.
- Mutate GitHub issues, pull requests, labels, projects, or milestones.
- Run warehouse, production, destructive, credentialed, or network write operations.
- Treat LLM output or rough notes as a source of truth when official docs are available.
