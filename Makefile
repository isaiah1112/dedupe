.PHONY: install
install:
	@python -m pip install -U .

.PHONY: install-dev
install-dev:
	@python -m pip install -U -e .

.PHONY: lint
lint:
	@uv run --group test ruff check src/dedupe/