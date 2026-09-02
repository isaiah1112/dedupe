# AGENTS.md

## Project overview
This repository contains the `dedupe` Python utility, which scans directories for duplicate files using different hash algorithms (`md5`, `sha1`, `sha256`, and `blake3`).

Key project files:
- `pyproject.toml` — project metadata and dependencies
- `src/dedupe/__init__.py` — CLI and hashing logic
- `tests/test_dedupe.py` — regression tests
- `Makefile` — common setup and validation commands

## Required environment
Use `uv` as the default package manager. The project-managed environment is `.venv`.

Rules for agents:
- Do not install packages into global Python environments.
- Prefer the Makefile targets for setup and validation.
- Use the repository-local virtual environment at `.venv` for direct Python commands.
- Use commands such as:
  - `.venv/bin/python`
  - `.venv/bin/pip`
  - `.venv/bin/pytest`
  - `.venv/bin/ruff`
  - `.venv/bin/ty`
- If you need to activate the environment in a shell, use:
  - `source .venv/bin/activate`

## Setup
From the repository root, use the project-managed setup flow:

```bash
make install
```

This installs uv if needed and runs `uv sync --locked`, creating or updating `.venv` from `uv.lock`. Activate it when direct environment commands are needed:

source .venv/bin/activate

The Makefile’s `lint` and `test` targets use uv and install the test dependency group on demand:

```bash
make lint
make test
```

For the explicit pip fallback:

```bash
make install UV_INSTALL=0
```

Docker-based tests are available for one or all supported Python versions:

```bash
make docker-test PYTHON_VERSION=3.14
make docker-test-all
```

## Testing and validation
Prefer the Makefile targets:

```bash
make lint
make test
```

Equivalent direct uv commands are:

```bash
uv run --locked --group test ruff check src/
uv run --locked --group test ty check src/
uv run --locked --group test pytest
```

The GitHub Actions workflow runs linting and type checking once, then runs tests across Python 3.10 through 3.14. `ty` is informational in CI, while Ruff and tests remain required.

Dependabot checks the uv lockfile and GitHub Actions dependencies weekly.

## Agent expectations
- Prefer working inside the repo root and using `.venv` for all Python commands.
- If a command needs a Python interpreter or package install, use `.venv/bin/...` explicitly.
- Prefer editing source files in `src/` and tests in `tests/`.
- Keep changes consistent with the project’s current packaging and CLI behavior.
- Validate with the relevant test or lint command before concluding work.

## Notes
The repository is configured to use `uv` and `.venv` for dependency management, and the Makefile targets already assume a local virtual environment. Follow that pattern consistently for any agent or automation working in this project.
