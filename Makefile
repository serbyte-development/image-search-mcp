.PHONY: lint

PYTHON ?= .venv/bin/python

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m pyrefly check
