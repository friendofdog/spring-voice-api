.PHONY: test lint type-check

SHELL := /bin/bash

all: test lint type-check

test:
	set -a && set +a && \
	python3 -m pytest -q --disable-pytest-warnings

run:
	@set -a && set +a && \
	export SUBMISSION=$(shell python3 -m bin.config --protocol=firebase $(SUB)) && \
	export AUTH=$(shell python3 -m bin.config --protocol=google $(AUTH)) && \
	export USER=$(shell python3 -m bin.config --protocol=firebase $(USER)) && \
	export TOKEN=$(shell python3 -m bin.config --protocol=firebase $(TOKEN)) && \
	python3 -m springapi.app

lint:
	python3 -m flake8 tests/ springapi/

type-check:
	python3 -m mypy tests/*.py tests/**/*.py \
	springapi/*.py springapi/**/*.py springapi/**/**/*.py
