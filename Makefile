.PHONY: pycheck pipcheck dev test clean

PY_SYS = python3
VENV_PATH = venv
PY_VENV = ${VENV_PATH}/bin/${PY_SYS}

PYTHON_VER := $(subst ., ,$(shell ${PY_SYS} --version 2>/dev/null))
PYTHON_VER_MAJOR := $(word 2,${PYTHON_VER})
PYTHON_VER_MINOR := $(word 3,${PYTHON_VER})

PIP_VER := $(subst ., ,$(shell ${PY_SYS} -m pip --version))
PIP_VER_MAJOR := $(word 2,${PIP_VER})

all: test

pycheck:
ifeq ($(shell [[ ${PYTHON_VER_MAJOR} == 3 && ${PYTHON_VER_MINOR} -ge 7 ]] \
&& echo true),true)
	@echo "Found version $(PYTHON_VER)"
else
	@echo "You need Python 3.7 or higher"
	@exit 1
endif

pipcheck:
ifeq (${PIP_VER_MAJOR}, 20)
	@echo "Found version $(PIP_VER)"
else
	@echo "You need PIP 20 or higher"
	@exit 1
endif

dev: pycheck pipcheck
ifeq ($(shell [[ ! -d "venv" ]] && echo true), true)
	@${PY_SYS} -s -m venv $(VENV_PATH)
	@. ./$(VENV_PATH)/bin/activate; \
	${PY_VENV} -m pip install -r requirements.txt; \
	${PY_VENV} -m pip install -r requirements-dev.txt
endif

test: dev
	@. ./$(VENV_PATH)/bin/activate; \
	pytest -q

clean:
	@rm -rf venv
