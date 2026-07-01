# Snowflake `CREATE TABLE`

<!-- toc:start -->
- [Why it matters](#why-it-matters)
- [Common variants to compare](#common-variants-to-compare)
- [Related notes](#related-notes)
- [Official references](#official-references)
<!-- toc:end -->

## Why it matters

`CREATE TABLE` is the base Snowflake DDL command for creating tables. Snowflake also supports related variants such as creating a table from a query, copying table structure, cloning, and creating temporary or transient tables.

## Common variants to compare

- Plain `CREATE TABLE`: define columns and table properties.
- `CREATE TABLE AS SELECT` / CTAS: create and populate a table from a query.
- `CREATE TABLE LIKE`: copy column definitions without copying the data.
- `CREATE TABLE CLONE`: create a zero-copy clone of an existing table at a point in time, subject to Snowflake behavior and retention rules.

## Related notes

- [Snowflake notes](../README.md)

## Official references

- [Snowflake docs: CREATE TABLE](https://docs.snowflake.com/en/sql-reference/sql/create-table)
