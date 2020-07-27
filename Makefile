.PHONY: test lint type-check

all: test lint type-check

test:
	export FLASK_ENV=testing && \
	pytest -q

lint:
	flake8 tests/ springapi/ models/

type-check:
	mypy tests/*.py tests/**/*.py \
	springapi/*.py springapi/**/*.py \
	models/*.py models/**/*.py
