# Learning Docs

This directory is the source of truth for learning and review notes. It can contain any technical topic, not just the examples that already exist.

## Generated index

<!-- docs-index:start -->
- [Airbyte Notes](airbyte/README.md) `airbyte/README`
- [Running Airbyte from a Mac](airbyte/running-on-mac.md) `airbyte/running-on-mac`
- [dbt Notes](dbt/README.md) `dbt/README`
- [ref() and Model Dependencies](dbt/models/ref.md) `dbt/models/ref`
- [source() and Source Definitions](dbt/sources/source.md) `dbt/sources/source`
- [Glossary](glossary.md) `glossary`
- [Parking Lot](parking-lot.md) `parking-lot`
- [Snowflake Notes](snowflake/README.md) `snowflake/README`
- [Snowflake CREATE TABLE](snowflake/tables/create-table.md) `snowflake/tables/create-table`
<!-- docs-index:end -->

## How to use these notes

- Capture notes in whatever shape is fastest: bullets, prose, Markdown, text files, copied snippets, or stdin.
- Run `codex-add-notes ...` to refine the raw capture into organized docs.
- Prefer one durable page per concept rather than one giant notebook.
- Create new `docs/<technology>/` areas when a named product or framework deserves one.
- Keep official references on the page that depends on them.
- Use `docs/parking-lot.md` for uncertainty instead of forcing a polished answer too early.

## Local maintenance

```bash
python scripts/docs/outline.py --json
python scripts/docs/update_toc.py
python scripts/docs/update_toc.py --check
```
