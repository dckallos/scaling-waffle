.PHONY: toc check test

toc:
	python scripts/docs/update_toc.py

check:
	python scripts/docs/update_toc.py --check
	python -m unittest discover -s tests

test:
	python -m unittest discover -s tests
