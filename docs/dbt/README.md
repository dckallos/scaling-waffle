# dbt Notes

Use this section for dbt concepts, workflows, and review notes.

<!-- toc:start -->
- [Core concepts](#core-concepts)
- [Review habits](#review-habits)
<!-- toc:end -->

## Core concepts

- [Models and `ref()`](models/ref.md)
- [Profiles, environments, and CI promotion](profiles.md)
- [Sources and `source()`](sources/source.md)

## Review habits

When adding dbt notes, distinguish between:

- what dbt parses into the project graph;
- what dbt compiles into SQL;
- what dbt runs in the warehouse;
- what is represented in docs, lineage, and selection syntax;
- what belongs in project code versus local or deployment connection profiles;
- whether a schema name is the target schema or a custom schema suffix;
- which identity and target are allowed to write to development, CI, staging, or production;
- which CI failures are merge blockers versus warnings for human review.
