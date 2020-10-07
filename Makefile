.PHONY: test lint type-check

SHELL := /bin/bash

all: test lint type-check

test:
	set -a && set +a && \
	python3 -m pytest -q --disable-pytest-warnings

run:
	@set -a && set +a && \
	export DATABASE_URI=$(shell python3 -m bin.config $(DB)) && \
	export AUTH=$(shell python3 -m bin.config --protocol=auth $(AUTH)) && \
	python3 -m springapi.app

lint:
	python3 -m flake8 tests/ springapi/

type-check:
	python3 -m mypy tests/*.py tests/**/*.py \
	springapi/*.py springapi/**/*.py springapi/**/**/*.py
