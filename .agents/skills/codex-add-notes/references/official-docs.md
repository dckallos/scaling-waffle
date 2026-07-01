# Official Documentation Reference Map

This file is a starting map, not an exhaustive list. Always search official docs for the specific claim being added.

## Source-of-truth hierarchy

Prefer sources in this order:

1. Official product, project, vendor, or standards documentation.
2. Official API references, command references, release notes, or GitHub repositories owned by the project/vendor.
3. Vendor-maintained tutorials or examples.
4. Third-party articles only as optional framing or further reading.

Do not use a blog post, forum answer, or LLM response as the only support for a factual product claim when official docs are available.

## Discovery rule for unknown technologies

When the product is not listed below, search for:

```text
<product> official docs <specific topic>
<product> documentation <specific topic>
site:<official-domain-if-known> <specific topic>
```

Then add the official docs link to the Markdown page when it materially supports the explanation.

## Seed official-doc domains

These are common data/platform tools. The list is intentionally incomplete.

| Product / topic | Official docs |
| --- | --- |
| dbt | `https://docs.getdbt.com/` |
| Snowflake | `https://docs.snowflake.com/` |
| Airbyte | `https://docs.airbyte.com/` |
| Apache Airflow | `https://airflow.apache.org/docs/` |
| Fivetran | `https://fivetran.com/docs` |
| Databricks | `https://docs.databricks.com/` |
| Dagster | `https://docs.dagster.io/` |
| Prefect | `https://docs.prefect.io/` |
| DuckDB | `https://duckdb.org/docs/` |
| PostgreSQL | `https://www.postgresql.org/docs/` |
| Apache Spark | `https://spark.apache.org/docs/` |
| Apache Kafka | `https://kafka.apache.org/documentation/` |
| GitHub Actions | `https://docs.github.com/actions` |
| Terraform | `https://developer.hashicorp.com/terraform/docs` |
| Kubernetes | `https://kubernetes.io/docs/` |
| Python | `https://docs.python.org/3/` |
| pandas | `https://pandas.pydata.org/docs/` |
| OpenAI / Codex | `https://developers.openai.com/codex/` |

## Common seed references

Use these only when relevant. Still verify the exact claim.

### dbt

- `ref()` function: `https://docs.getdbt.com/reference/dbt-jinja-functions/ref`
- `source()` function: `https://docs.getdbt.com/reference/dbt-jinja-functions/source`
- Sources guide: `https://docs.getdbt.com/docs/build/sources`
- Source properties: `https://docs.getdbt.com/reference/source-properties`
- Source freshness: `https://docs.getdbt.com/reference/resource-properties/freshness`
- Documentation: `https://docs.getdbt.com/docs/build/documentation`
- Data tests: `https://docs.getdbt.com/docs/build/data-tests`
- Models: `https://docs.getdbt.com/docs/build/models`
- Materializations: `https://docs.getdbt.com/docs/build/materializations`
- Node selection syntax: `https://docs.getdbt.com/reference/node-selection/syntax`
- Jinja functions: `https://docs.getdbt.com/reference/dbt-jinja-functions`

### Snowflake

- CREATE TABLE: `https://docs.snowflake.com/en/sql-reference/sql/create-table`
- ALTER TABLE: `https://docs.snowflake.com/en/sql-reference/sql/alter-table`
- COPY INTO table: `https://docs.snowflake.com/en/sql-reference/sql/copy-into-table`
- CREATE STAGE: `https://docs.snowflake.com/en/sql-reference/sql/create-stage`
- Snowpipe: `https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro`
- Streams: `https://docs.snowflake.com/en/user-guide/streams`
- Tasks: `https://docs.snowflake.com/en/user-guide/tasks-intro`
- Dynamic tables: `https://docs.snowflake.com/en/user-guide/dynamic-tables-about`
- Time Travel: `https://docs.snowflake.com/en/user-guide/data-time-travel`
- Access control: `https://docs.snowflake.com/en/user-guide/security-access-control-overview`

### Airbyte

- Airbyte docs root: `https://docs.airbyte.com/`
- Connectors: `https://docs.airbyte.com/integrations/`

### Apache Airflow

- Airflow docs root: `https://airflow.apache.org/docs/`
- Stable documentation: `https://airflow.apache.org/docs/apache-airflow/stable/`

## Source handling rules

- Add official-reference links to the Markdown page when they materially support the explanation.
- Summarize official docs in your own words; avoid long copied excerpts.
- If official docs are unavailable or inconclusive, write the claim as uncertain and add it to `docs/parking-lot.md`.
- If a third-party article is useful for framing, place it under `Further reading`, not `Official references`.
