---
name: codex-add-notes
description: Transform raw or missing learning-note input into organized Markdown docs for any technical topic. Supports pasted text, arbitrary .md/.txt files, inline topic requests, and zero-input intake sessions; verifies claims against official docs, routes with the live docs outline, asks helpful questions in interactive mode, and updates deterministic navigation.
---

# Codex Add Notes Skill

Use this skill when the user asks to add, refine, organize, document, review, reference, polish, or convert learning notes into Markdown documentation.

The input may be any of these:

- rough notes from pasted text, stdin, or arbitrary `.md` / `.txt` files;
- a minimal inline topic request, such as `document ways for me to run Airbyte from my Mac`;
- no topic at all, where the correct behavior is to start an intake interview.

The notes may be about any technical topic: dbt, Snowflake, Airbyte, Airflow, SQL, Python, cloud services, data engineering, orchestration, modeling, testing, infrastructure, or a product not yet represented in the repository. The workflow must not rely on a fixed list of technologies.

## Core principle

The source input is raw capture, not a contract. It may be bullets, fragments, pasted terminal output, prose, transcript snippets, or a mixed Markdown/Text file. It may also be a short topic request rather than a note file. Do not require headings, front matter, templates, tags, or any special source-note structure.

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

If the wrapper supplied a request packet, read `request.json`, `intent.txt`, every copied file under `input-files/`, `stdin.txt` when present, and `intake-answers.txt` when present. The copied input files contain the user's original note text; treat them as unstructured raw input.

If the user set a different docs root, use that value in place of `docs` for outline and TOC commands.

## Intake modes

The wrapper records an `input_mode` in `request.json`. Use it to choose the correct behavior.

### `codex_interview`

This means the user ran `codex-add-notes` with no topic, no note file, and no stdin in interactive mode.

Start by asking the user a concise intake batch. Do not edit files until the user answers with at least a topic.

Ask these questions:

1. What do you want to add documentation about?
2. Do you want to include specific citations or official docs URLs? Default: no.
3. Do you have a preferred destination/topic area, or should I choose automatically? Default: auto.
4. What depth should the page target? Default: review-friendly practical overview.
5. Do you have rough bullets, examples, constraints, or misconceptions to include? Optional.

Ask the questions together so the user can answer naturally. After the user answers, proceed through the normal workflow.

### `inline_topic`

This means the user supplied a topic request but no source note file, for example:

```bash
codex-add-notes document ways for me to run Airbyte from my Mac
```

Treat the intent text as a valid documentation request. Do not ask the user to create a Markdown or text file. Use official docs to build the documentation, ask follow-up questions only if the topic is too broad or preference-sensitive, and otherwise proceed.

### `shell_intake`

This means the user ran zero-input `codex-add-notes --exec`, so the wrapper collected a local terminal questionnaire before launching non-interactive Codex.

Read `intake-answers.txt`. Do not ask additional questions inside `codex exec`; proceed using the collected answers and put unresolved claims in `docs/parking-lot.md`.

### Other input modes

For file, stdin, or mixed modes, read the provided material and proceed. In interactive mode, ask helpful follow-up questions when they would materially improve the final documentation. In non-interactive mode, do not ask questions.

## Mandatory workflow

1. **Collect the raw input.** Read the intent text, copied input files, piped stdin, and intake answers. Preserve the user's learning goal even when the wording is rough.
2. **Interview when appropriate.** For zero-input interactive sessions, ask the intake batch before editing. For broad inline requests, ask useful follow-up questions before editing when user preferences would materially change the page.
3. **Inspect the current library.** Use `scripts/docs/outline.py --json` plus `docs/README.md` to understand existing pages, headings, and top-level topic areas.
4. **Identify topic and product.** Determine the durable concept, the named product/tool if any, and adjacent concepts. A new product such as Airbyte or Airflow should be routed naturally; it does not need a pre-existing map entry.
5. **Verify claims with official docs.** Use live web search and official documentation before incorporating technical claims as fact. For unknown products, search for the product's official documentation and prefer vendor/project docs over blogs.
6. **Route before writing.** Prefer updating an existing page whose title/headings already cover the concept. Create a new page only when the concept is durable enough to deserve a URL or the existing page would become too broad.
7. **Create generic topic areas when needed.** If no existing area fits a named technology, create `docs/<technology-slug>/README.md` and a topic page such as `docs/<technology-slug>/<topic-slug>.md`. If the note is product-neutral, prefer a stable conceptual area such as `docs/sql/`, `docs/orchestration/`, `docs/ingestion/`, `docs/modeling/`, or `docs/concepts/`.
8. **Correct gently.** If a rough note is inaccurate, preserve the intent but rewrite the claim accurately. Add a short misconception or pitfall note when it helps later review.
9. **Write maintainable Markdown.** Use polished paragraphs, small examples, short sections, and stable headings. Use bullets for comparisons, checklists, or steps. Do not copy the user's source-note messiness into the polished docs.
10. **Use diagrams selectively.** Add Mermaid when it clarifies lineage, DAGs, data flow, orchestration, control flow, architecture, or state transitions. Keep diagrams small and close to the explanation they support.
11. **Link the knowledge graph.** Add related-note links and glossary entries for reusable terms when they help discoverability.
12. **Update generated navigation.** Run `python scripts/docs/update_toc.py --docs-root docs`, then `python scripts/docs/update_toc.py --docs-root docs --check` when practical. Use the caller's docs root if different.
13. **Report clearly.** End with changed files, official docs consulted, important corrections made, and parking-lot items.

## Question posture

Questions are a usability feature, not a failure.

In interactive mode:

- Ask the intake batch for zero-input sessions.
- Ask a short batch of follow-up questions when the request is broad, ambiguous, preference-sensitive, or likely to benefit from user context.
- Good follow-up targets include desired scope, preferred destination, depth, official citation requirements, local environment assumptions, examples to include, and misconceptions to correct.
- Do not block on nonessential preferences when the user gave a clear, actionable topic. Make a sensible default choice and report it.

In non-interactive mode:

- Do not ask questions inside Codex.
- Use wrapper-collected intake answers when present.
- If required information is missing, make conservative assumptions, verify against official docs, and put unresolved claims in `docs/parking-lot.md`.

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
- Require the user to create a note file when they only want to request documentation on a topic.
