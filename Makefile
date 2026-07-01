.PHONY: toc outline check test

toc:
	python scripts/docs/update_toc.py

outline:
	python scripts/docs/outline.py --json

check:
	python scripts/docs/outline.py --json >/dev/null
	python scripts/docs/update_toc.py --check
	python -m unittest discover -s tests

test:
	python -m unittest discover -s tests
