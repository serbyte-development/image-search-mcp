.PHONY: lint test check

PYTHON ?= python3

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m pyrefly check

test:
	$(PYTHON) -m unittest -v test_manager

check: lint test
