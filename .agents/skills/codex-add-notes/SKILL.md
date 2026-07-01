---
name: codex-add-notes
description: Transform raw learning notes from pasted text or arbitrary .md/.txt files into organized Markdown docs for any technical topic, with official-doc verification, outline-aware routing, diagrams when useful, glossary/parking-lot handling, and deterministic navigation maintenance.
---

# Codex Add Notes Skill

Use this skill when the user asks to add, refine, organize, document, review, reference, polish, or convert rough learning notes into Markdown documentation.

The notes may be about any technical topic: dbt, Snowflake, Airbyte, Airflow, SQL, Python, cloud services, data engineering, orchestration, modeling, testing, infrastructure, or a product not yet represented in the repository. The workflow must not rely on a fixed list of technologies.

## Core principle

The source notes are raw capture, not a contract. They may be bullets, fragments, pasted terminal output, prose, transcript snippets, or a mixed Markdown/Text file. Do not require headings, front matter, templates, tags, or any special source-note structure.

The output docs should be organized, accurate, reviewable Markdown.

## First files and commands

Before editing, read:

1. `AGENTS.md` when present.
2. The docs root README, usually `docs/README.md`.
3. `.agents/skills/codex-add-notes/references/official-docs.md`.
4. `.agents/skills/codex-add-notes/assets/topic-map.md`.
5. Any existing document that appears to match the requested topic.

Before deciding where content belongs, run the deterministic outline helper:

```bash
python scripts/docs/outline.py --docs-root docs --json
```

If the wrapper supplied a request packet, read `request.json`, `intent.txt`, every copied file under `input-files/`, and `stdin.txt` when present. The copied input files contain the user's original note text; treat them as unstructured raw input.

If the user set a different docs root, use that value in place of `docs` for outline and TOC commands.

## Mandatory workflow

1. **Collect the raw notes.** Read the intent text, copied input files, and piped stdin. Preserve the user's learning goal even when the wording is rough.
2. **Inspect the current library.** Use `scripts/docs/outline.py --json` plus `docs/README.md` to understand existing pages, headings, and top-level topic areas.
3. **Identify topic and product.** Determine the durable concept, the named product/tool if any, and adjacent concepts. A new product such as Airbyte or Airflow should be routed naturally; it does not need a pre-existing map entry.
4. **Verify claims with official docs.** Use live web search and official documentation before incorporating technical claims as fact. For unknown products, search for the product's official documentation and prefer vendor/project docs over blogs.
5. **Route before writing.** Prefer updating an existing page whose title/headings already cover the concept. Create a new page only when the concept is durable enough to deserve a URL or the existing page would become too broad.
6. **Create generic topic areas when needed.** If no existing area fits a named technology, create `docs/<technology-slug>/README.md` and a topic page such as `docs/<technology-slug>/<topic-slug>.md`. If the note is product-neutral, prefer a stable conceptual area such as `docs/sql/`, `docs/orchestration/`, `docs/ingestion/`, `docs/modeling/`, or `docs/concepts/`.
7. **Correct gently.** If a rough note is inaccurate, preserve the intent but rewrite the claim accurately. Add a short misconception or pitfall note when it helps later review.
8. **Ask only when needed.** In an interactive session, ask one concise clarifying question only when a blocking ambiguity or likely factual error cannot be resolved from official docs. In non-interactive mode, do not ask questions; move unresolved claims to `docs/parking-lot.md` with context.
9. **Write maintainable Markdown.** Use polished paragraphs, small examples, short sections, and stable headings. Use bullets for comparisons, checklists, or steps. Do not copy the user's source-note messiness into the polished docs.
10. **Use diagrams selectively.** Add Mermaid when it clarifies lineage, DAGs, data flow, orchestration, control flow, architecture, or state transitions. Keep diagrams small and close to the explanation they support.
11. **Link the knowledge graph.** Add related-note links and glossary entries for reusable terms when they help discoverability.
12. **Update generated navigation.** Run `python scripts/docs/update_toc.py --docs-root docs`, then `python scripts/docs/update_toc.py --docs-root docs --check` when practical. Use the caller's docs root if different.
13. **Report clearly.** End with changed files, official docs consulted, important corrections made, and parking-lot items.

## Output page shape

The concept template is a useful starting point, not a required schema. Choose only the sections that help the topic.

Common useful sections:

- `## Why it matters`
- `## Mental model`
- `## Practical usage`
- `## Example`
- `## Diagram`
- `## Common pitfalls`
- `## Related notes`
- `## Official references`

Every durable page should have a clear H1 and should include TOC markers unless the page is intentionally tiny:

```markdown
# Page Title

<!-- toc:start -->
<!-- toc:end -->
```

Official references should use Markdown links to official documentation. When a claim depends on docs, make the source easy to inspect from the final Markdown page.

## Routing guidance

Use `.agents/skills/codex-add-notes/assets/topic-map.md` as a convention guide, not as a whitelist.

Routing order:

1. Existing page with matching title or headings.
2. Existing technology/product area under `docs/<technology>/`.
3. Existing conceptual area such as `docs/orchestration/` or `docs/ingestion/`.
4. New `docs/<technology-slug>/` area for a named product/tool.
5. New `docs/concepts/` page for product-neutral ideas.
6. `docs/parking-lot.md` for unresolved, ambiguous, or unsupported claims.

## Librarian modes

If the user asks to `review`, `organize`, `audit`, or act as a note librarian, inspect the docs structure before editing.

For librarian-style requests:

- Run `python scripts/docs/outline.py --docs-root docs --json`.
- Find duplicate or overlapping pages, stale parking-lot items, broken local links, missing official references, and pages with weak headings.
- Prefer proposing moves/merges first when the change is broad.
- In non-interactive mode, make only low-risk local Markdown edits and report larger restructuring as recommendations.

## Quality bar

A good note page should answer:

- What is the concept?
- Why does it matter?
- What should I remember during review?
- What is the smallest useful example?
- What are common mistakes or misconceptions?
- Which official docs confirmed the important claims?

## Non-goals and boundaries

Do not:

- Commit, push, branch, tag, open pull requests, or mutate GitHub metadata.
- Run production, credentialed, destructive, warehouse, deployment, or remote write operations.
- Treat unofficial blog posts as the source of truth when official docs exist.
- Preserve a user note as fact when official documentation contradicts it.
- Create a new document for every small note when an existing page can absorb it cleanly.
- Treat the seed topic map or official-doc map as exhaustive.
