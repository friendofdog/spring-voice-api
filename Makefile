.PHONY: test lint type-check

all: test lint type-check

test:
	pytest -q

lint:
	flake8 tests/ springapi/

type-check:
	mypy tests/**/*.py tests/*.py springapi/*.py springapi/**/*.py
