.PHONY: test lint type-check

all: test lint type-check

test:
	pytest -q

lint:
	flake8 tests/ app/

type-check:
	mypy tests/**/*.py tests/*.py app/**/*.py
