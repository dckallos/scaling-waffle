# Topic Map

This map describes routing conventions. It is not a whitelist and should not block new technologies.

When a note mentions a product or technology that is not listed here, infer a stable path from the product name and topic:

```text
docs/<technology-slug>/README.md
docs/<technology-slug>/<topic-slug>.md
```

Examples:

```text
Airbyte connector notes      -> docs/airbyte/connectors.md
Airflow scheduling notes     -> docs/airflow/scheduling.md
Kafka consumer group notes   -> docs/kafka/consumer-groups.md
DuckDB parquet notes         -> docs/duckdb/parquet.md
Terraform state notes        -> docs/terraform/state.md
```

Use `scripts/docs/outline.py --json` before relying on this file. The live outline is the source of truth for what already exists.

## Generic routing order

1. Update an existing page with matching title, headings, or related links.
2. Update an existing technology area under `docs/<technology>/`.
3. Update an existing conceptual area such as `docs/orchestration/`, `docs/ingestion/`, `docs/sql/`, `docs/modeling/`, or `docs/concepts/`.
4. Create a new technology area for a named product/tool.
5. Create a new product-neutral concept page.
6. Use `docs/glossary.md` for reusable definitions.
7. Use `docs/parking-lot.md` for unresolved or suspect claims.

## Suggested top-level areas

These areas are intentionally broad. Create them only when useful.

| Area | Use for |
| --- | --- |
| `docs/<technology>/` | Notes about a named product, framework, service, library, or platform. |
| `docs/sql/` | SQL syntax, query patterns, joins, windows, CTEs, set operations, and database-neutral SQL concepts. |
| `docs/ingestion/` | ELT/ETL patterns, connectors, replication, CDC, file movement, batch/stream ingestion. |
| `docs/orchestration/` | Scheduling, DAGs, dependencies, retries, sensors, backfills, and workflow engines. |
| `docs/modeling/` | Dimensional modeling, facts/dimensions, marts, staging, semantic layers, metrics. |
| `docs/testing/` | Data tests, software tests, validation, assertions, quality gates. |
| `docs/operations/` | Deployments, CI, observability, incidents, cost, performance, maintenance. |
| `docs/concepts/` | Product-neutral concepts that do not fit a specific area yet. |

## Existing seed examples

These examples are present because the first notes were about dbt and Snowflake. They are examples, not limits.

| Topic hints | Preferred file |
| --- | --- |
| dbt `ref`, dependency graph, DAG ordering, upstream/downstream models | `docs/dbt/models/ref.md` |
| dbt `source`, raw tables, source freshness, `sources.yml`, source lineage | `docs/dbt/sources/source.md` |
| Snowflake `CREATE TABLE`, CTAS, clone, temp/transient tables, DDL | `docs/snowflake/tables/create-table.md` |
| Reusable definition | `docs/glossary.md` |
| Unresolved, ambiguous, or possibly wrong claim | `docs/parking-lot.md` |

## File creation rules

Create a new file when:

- The topic is likely to receive future notes.
- The existing page would become too broad.
- The topic has a distinct review mental model.
- The note introduces a named technology with no existing area.

Update an existing file when:

- The note extends a concept already present.
- The note is an example, pitfall, diagram, or official reference for an existing concept.
- The note is too small to justify a durable URL.

## Slug conventions

Use lowercase kebab-case paths:

```text
Apache Airflow -> airflow
GitHub Actions -> github-actions
CREATE TABLE -> create-table
Consumer groups -> consumer-groups
```

Prefer stable nouns over one-off note titles. For example, use `docs/airflow/scheduling.md`, not `docs/airflow/things-i-learned-tuesday.md`.
