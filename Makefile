PYTHON := uv run python

.PHONY: sync toc check test

sync:
	uv sync

toc:
	$(PYTHON) scripts/docs/update_toc.py

check:
	$(PYTHON) scripts/docs/update_toc.py --check
	$(PYTHON) -m unittest discover -s tests

test:
	$(PYTHON) -m unittest discover -s tests
