PYTHON_VERSION := "3.14" # Default Python Version
UV_PATH := $(shell which uv 2>/dev/null)
UV_INSTALL := 1

.PHONY: help
help:
	@echo "Usage: make <target> [option]"
	@echo "\nTargets:"
	@echo "  install [UV_INSTALL=1]    Install project"
	@echo "  lint    Run 'ruff' linting and 'ty' type-checking on project"
	@echo "  test    Run 'pytest' on project"
	@echo "  docker-test [PYTHON_VERSION=X.X]   Run unit tests in Docker container"
	@echo "\nSpecial Targets:"
	@echo "  docker-test-all    Run unit tests, in Docker, across all versions of Python"

# Install UV if it is not installed
.PHONY: uv-init
init:
	@if [ -z "$(UV_PATH)" ]; then curl -LsSf https://astral.sh/uv/install.sh | sh; fi

.PHONY: install
install:
	@if [ $(UV_INSTALL) -eq 1 ]; then\
		$(MAKE) uv-init && uv sync && echo "Please run the following to activate the virtualenv:\n source .venv/bin/activate";\
	else\
		python -m pip install -U .;\
	fi

.PHONY: lint
lint: uv-init
	@uv run --group test ruff check src/
	@uv run --group test ty check src/

.PHONY: test
test: uv-init
	@uv run --group test pytest

.PHONY: docker-test-all
docker-test-all:
	@$(MAKE) docker-test PYTHON_VERSION=3.10
	@$(MAKE) docker-test PYTHON_VERSION=3.11
	@$(MAKE) docker-test PYTHON_VERSION=3.12
	@$(MAKE) docker-test PYTHON_VERSION=3.13
	@$(MAKE) docker-test PYTHON_VERSION=3.14

# Private target for docker-tests
.PHONY: docker-test
docker-test:
	@echo "Testing Python:$(PYTHON_VERSION)"
	@docker run -it --rm -v "$(PWD)":/usr/src/app -w /usr/src/app python:$(PYTHON_VERSION)\
		sh -c 'python -m pip install --root-user-action=ignore uv && uv run --link-mode=copy --group test pytest'