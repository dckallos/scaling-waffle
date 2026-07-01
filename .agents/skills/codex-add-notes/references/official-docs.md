# Official Documentation Reference Map

This file gives Codex a starting map. It is not exhaustive. Always search official docs for the specific claim being added.

## dbt

Use `https://docs.getdbt.com/` as the default source of truth for dbt behavior.

Common dbt references:

- `ref()` function: `https://docs.getdbt.com/reference/dbt-jinja-functions/ref`
- `source()` function: `https://docs.getdbt.com/reference/dbt-jinja-functions/source`
- Sources guide: `https://docs.getdbt.com/docs/build/sources`
- Source properties: `https://docs.getdbt.com/reference/source-properties`
- Source freshness: `https://docs.getdbt.com/reference/resource-properties/freshness`
- dbt documentation: `https://docs.getdbt.com/docs/build/documentation`
- dbt docs command: `https://docs.getdbt.com/reference/commands/cmd-docs`
- Data tests: `https://docs.getdbt.com/docs/build/data-tests`
- Models: `https://docs.getdbt.com/docs/build/models`
- Materializations: `https://docs.getdbt.com/docs/build/materializations`
- Node selection syntax: `https://docs.getdbt.com/reference/node-selection/syntax`
- Node selector methods: `https://docs.getdbt.com/reference/node-selection/methods`
- Jinja functions: `https://docs.getdbt.com/reference/dbt-jinja-functions`

## Snowflake

Use `https://docs.snowflake.com/` as the default source of truth for Snowflake behavior.

Common Snowflake references:

- CREATE TABLE: `https://docs.snowflake.com/en/sql-reference/sql/create-table`
- ALTER TABLE: `https://docs.snowflake.com/en/sql-reference/sql/alter-table`
- SHOW TABLES: `https://docs.snowflake.com/en/sql-reference/sql/show-tables`
- DESCRIBE TABLE: `https://docs.snowflake.com/en/sql-reference/sql/desc-table`
- COPY INTO table: `https://docs.snowflake.com/en/sql-reference/sql/copy-into-table`
- CREATE STAGE: `https://docs.snowflake.com/en/sql-reference/sql/create-stage`
- Snowpipe: `https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro`
- Streams: `https://docs.snowflake.com/en/user-guide/streams`
- Tasks: `https://docs.snowflake.com/en/user-guide/tasks-intro`
- Dynamic tables: `https://docs.snowflake.com/en/user-guide/dynamic-tables-about`
- Time Travel: `https://docs.snowflake.com/en/user-guide/data-time-travel`
- Access control: `https://docs.snowflake.com/en/user-guide/security-access-control-overview`

## Other data tools

Prefer official docs for the named product:

- Airbyte: `https://docs.airbyte.com/`
- Fivetran: `https://fivetran.com/docs`
- Databricks: `https://docs.databricks.com/`
- Apache Airflow: `https://airflow.apache.org/docs/`
- Dagster: `https://docs.dagster.io/`
- Prefect: `https://docs.prefect.io/`
- GitHub Actions: `https://docs.github.com/actions`

## Source handling rules

- Add official-reference links to the Markdown page when they materially support the explanation.
- If official docs are unavailable or inconclusive, write the claim as uncertain and add it to `docs/parking-lot.md`.
- If a third-party article is useful for framing, it may be added under "Further reading," but not as the source of truth for product behavior.
