PYTHON_VERSION ?= 3.14
UV_INSTALL ?= 1
UV := $(or $(shell command -v uv 2>/dev/null),$(HOME)/.local/bin/uv)

.DEFAULT_GOAL := help

.PHONY: help
help:
	@printf '%s\n' \
		'Usage: make <target> [option]' \
		'' \
		'Targets:' \
		'  install [UV_INSTALL=1]             Install the project with uv' \
		'  lint                                Run ruff and ty checks' \
		'  test                                Run pytest' \
		'  docker-test [PYTHON_VERSION=X.X]   Run tests in a Docker container' \
		'  docker-test-all                    Run Docker tests across Python versions'

# Install UV if it is not installed
.PHONY: uv-init
uv-init:
	@if command -v uv >/dev/null 2>&1; then \
		exit 0; \
	fi; \
	echo 'Installing uv...'; \
	curl --fail --location --silent --show-error https://astral.sh/uv/install.sh | sh; \
	test -x "$(UV)"

.PHONY: install
install:
ifeq ($(UV_INSTALL),1)
	@$(MAKE) uv-init
	@$(UV) sync --locked
	@printf '%s\n' 'Run: source .venv/bin/activate'
else
	@python -m pip install --upgrade .
endif

.PHONY: lint
lint: uv-init
	@$(UV) run --locked --group test ruff check src/
	@$(UV) run --locked --group test ty check src/

.PHONY: test
test: uv-init
	@$(UV) run --locked --group test pytest

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
	@docker run --rm -v "$(PWD)":/usr/src/app -w /usr/src/app python:$(PYTHON_VERSION) \
		sh -c 'python -m pip install --root-user-action=ignore uv && uv run --locked --link-mode=copy --group test pytest'