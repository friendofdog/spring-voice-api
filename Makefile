.PHONY: test clean

all: test lint type-check

test:
	pytest -q

lint:
	flake8 tests/ app.py

type-check:
	mypy tests/**/*.py tests/*.py app.py
