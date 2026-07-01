# Topic Map

Use this map to keep notes discoverable. Prefer existing files before creating new ones.

## dbt

| Topic hints | Preferred file |
| --- | --- |
| `ref`, dependency graph, DAG ordering, upstream/downstream models | `docs/dbt/models/ref.md` |
| `source`, raw tables, source freshness, `sources.yml`, source lineage | `docs/dbt/sources/source.md` |
| descriptions, docs blocks, `dbt docs generate`, catalog/docs site | `docs/dbt/documentation.md` |
| generic models, staging/intermediate/marts, model SQL | `docs/dbt/models/README.md` or a specific file under `docs/dbt/models/` |
| tests, generic tests, singular tests, constraints | `docs/dbt/tests.md` |
| materialized view, table, view, incremental, ephemeral | `docs/dbt/materializations.md` |
| selectors, `--select`, state selection, build/run ordering | `docs/dbt/node-selection.md` |
| macros, Jinja, adapter dispatch | `docs/dbt/jinja-and-macros.md` |

## Snowflake

| Topic hints | Preferred file |
| --- | --- |
| `CREATE TABLE`, CTAS, clone, temp/transient tables, DDL | `docs/snowflake/tables/create-table.md` |
| stages, files, `COPY INTO`, loading data | `docs/snowflake/loading/copy-into.md` |
| streams, CDC, change tracking | `docs/snowflake/streams.md` |
| tasks, scheduling, task graph | `docs/snowflake/tasks.md` |
| dynamic tables, target lag, refresh | `docs/snowflake/dynamic-tables.md` |
| roles, grants, privileges, RBAC | `docs/snowflake/access-control.md` |
| warehouse size, query profile, clustering, performance | `docs/snowflake/performance.md` |

## General SQL and analytics engineering

| Topic hints | Preferred file |
| --- | --- |
| SQL joins, windows, CTEs, semi/anti joins | `docs/sql/` topic file |
| dimensional modeling, facts, dimensions, marts | `docs/analytics-engineering/modeling.md` |
| ingestion tools, ELT, connectors | `docs/ingestion/` topic file |
| orchestration, DAG scheduling | `docs/orchestration/` topic file |
| reusable definition | `docs/glossary.md` |
| unresolved or possibly wrong claim | `docs/parking-lot.md` |

## File creation rules

Create a new file when:

- The topic is likely to receive future notes.
- The existing page would become too broad.
- The topic has a distinct review mental model.

Update an existing file when:

- The note extends a concept already present.
- The note is an example, pitfall, diagram, or official reference for an existing concept.
- The note is too small to justify a durable URL.
