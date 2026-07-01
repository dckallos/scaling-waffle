# Learning Docs

This directory is the source of truth for learning and review notes.

## Generated index

<!-- docs-index:start -->
- [dbt Notes](dbt/README.md) `dbt/README`
- [ref() and Model Dependencies](dbt/models/ref.md) `dbt/models/ref`
- [source() and Source Definitions](dbt/sources/source.md) `dbt/sources/source`
- [Glossary](glossary.md) `glossary`
- [Parking Lot](parking-lot.md) `parking-lot`
- [Snowflake Notes](snowflake/README.md) `snowflake/README`
- [Snowflake CREATE TABLE](snowflake/tables/create-table.md) `snowflake/tables/create-table`
<!-- docs-index:end -->

## How to use these notes

- Keep rough capture files close to the repo, then run `codex-add-notes ...` to refine them.
- Prefer one durable page per concept rather than one large notebook.
- Keep official references on the page that depends on them.
- Use `docs/parking-lot.md` for uncertainty instead of forcing a polished answer too early.

## Local maintenance

```bash
python scripts/docs/update_toc.py
python scripts/docs/update_toc.py --check
```
