---
name: codex-add-notes
description: Transform rough dbt, Snowflake, SQL, and data-engineering notes from pasted bullets or .md/.txt files into organized Markdown learning docs with official-doc verification, diagrams, glossary updates, parking-lot handling, and TOC maintenance.
---

# Codex Add Notes Skill

Use this skill when the user asks to add, refine, document, organize, reference, polish, or convert rough learning notes about dbt, Snowflake, SQL, analytics engineering, data ingestion, orchestration, modeling, testing, documentation, or adjacent data tools.

The goal is not to make the notes longer for their own sake. The goal is to turn rough notes into maintainable, reviewable Markdown that a learner can revisit later.

## First files to read

Before editing, read:

1. `AGENTS.md`
2. `docs/README.md`
3. `.agents/skills/codex-add-notes/references/official-docs.md`
4. `.agents/skills/codex-add-notes/assets/topic-map.md`
5. Any existing document that appears to match the requested topic

If invoked by the wrapper, also read the request manifest under `.codex-add-notes/requests/` and every note file listed in it.

## Mandatory workflow

1. **Understand the input.** Identify the subject, intended audience, source files, and whether the request is asking for a new document, an update to an existing document, a glossary entry, or a parking-lot note.
2. **Route before writing.** Prefer updating an existing durable topic page over creating a new page. Create a new page only when the concept is stable enough to deserve its own URL.
3. **Verify with official docs.** Use live web search and official documentation before incorporating technical claims as fact. Prefer:
   - dbt: `docs.getdbt.com`
   - Snowflake: `docs.snowflake.com`
   - Airbyte: `docs.airbyte.com`
   - Fivetran: `fivetran.com/docs`
   - Databricks: `docs.databricks.com`
   - OpenAI/Codex: `developers.openai.com`
4. **Correct gently.** If the user's rough note is wrong, preserve the learning intent but rewrite the statement accurately. Add a short misconception/pitfall note when useful.
5. **Ask only when needed.** In an interactive session, ask one concise clarifying question only when a blocking ambiguity or likely factual error cannot be resolved from official docs. In non-interactive mode, do not ask questions; move unresolved claims to `docs/parking-lot.md`.
6. **Write maintainable Markdown.** Prefer paragraphs, short examples, and stable section headings over long loose bullet lists. Use bullets for checklists, comparisons, or steps.
7. **Use diagrams selectively.** Add Mermaid when it clarifies DAGs, lineage, data flow, orchestration, control flow, or architecture. Keep diagrams small and close to the explanation they support.
8. **Link the knowledge graph.** Add related-note links and glossary entries for reusable terms.
9. **Update generated navigation.** Run `python scripts/docs/update_toc.py`. Then run `python scripts/docs/update_toc.py --check` when practical.
10. **Report clearly.** End with changed files, official docs consulted, important corrections made, and any parking-lot items.

## Markdown shape

Use this shape for durable concept pages. Omit sections that do not help the topic.

```markdown
# Concept Name

<!-- toc:start -->
<!-- toc:end -->

## Why it matters

## Mental model

## Practical usage

## Example

## Diagram

## Common pitfalls

## Related notes

## Official references
```

Official references should use Markdown links to official documentation. When a claim depends on docs, make the source easy to inspect from the final Markdown page.

## Routing defaults

Use `.agents/skills/codex-add-notes/assets/topic-map.md` for detailed routing. Common defaults:

- `ref()`, model dependencies, DAG order: `docs/dbt/models/ref.md`
- `source()`, source freshness, source YAML: `docs/dbt/sources/source.md`
- dbt documentation, docs blocks, descriptions: `docs/dbt/documentation.md`
- dbt tests: `docs/dbt/tests.md`
- dbt materializations: `docs/dbt/materializations.md`
- Snowflake table DDL, CTAS, clone, transient/temp tables: `docs/snowflake/tables/create-table.md`
- Snowflake loading, stages, `COPY INTO`: `docs/snowflake/loading/copy-into.md`
- reusable definitions: `docs/glossary.md`
- unresolved or suspect notes: `docs/parking-lot.md`

## Quality bar

A good note page should answer:

- What is the concept?
- Why does it matter?
- What should I remember during review?
- What is the smallest useful example?
- What are the common mistakes?
- Which official docs confirmed the important claims?

## Non-goals and boundaries

Do not:

- Commit, push, branch, tag, open pull requests, or mutate GitHub metadata.
- Run dbt against real credentials, call a data warehouse, or execute production-impacting commands.
- Use unofficial blog posts as the only source for factual claims when official docs exist.
- Preserve a user note as fact if official documentation contradicts it.
- Create a new document for every small note when an existing page can absorb it cleanly.
