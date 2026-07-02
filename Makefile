DOCS_HOST ?= 127.0.0.1
DOCS_PORT ?= 8000
DOCS_EDIT_URI_TEMPLATE ?= vscode://file$(CURDIR)/docs/{path}:1

.PHONY: toc outline docs-preview docs-serve docs-build check test

toc:
	python scripts/docs/update_toc.py

outline:
	python scripts/docs/outline.py --json

docs-preview:
	bin/docs-preview

docs-serve:
	MKDOCS_EDIT_URI_TEMPLATE="$(DOCS_EDIT_URI_TEMPLATE)" uv run mkdocs serve --dev-addr $(DOCS_HOST):$(DOCS_PORT)

docs-build:
	MKDOCS_EDIT_URI_TEMPLATE="$(DOCS_EDIT_URI_TEMPLATE)" uv run mkdocs build --strict

check:
	python scripts/docs/outline.py --json >/dev/null
	python scripts/docs/update_toc.py --check
	python -m unittest discover -s tests
	MKDOCS_EDIT_URI_TEMPLATE="$(DOCS_EDIT_URI_TEMPLATE)" uv run mkdocs build --strict

test:
	python -m unittest discover -s tests
