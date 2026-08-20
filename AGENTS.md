# AGENTS.md

## Project overview
This repository contains the `dedupe` Python utility, which scans directories for duplicate files using different hash algorithms (`md5`, `sha1`, `sha256`, and `blake3`).

Key project files:
- `pyproject.toml` — project metadata and dependencies
- `src/dedupe/__init__.py` — CLI and hashing logic
- `tests/test_dedupe.py` — regression tests
- `Makefile` — common setup and validation commands

## Required environment
All Python package installation and management must use the repository-local virtual environment at `.venv`.

Rules for agents:
- Do not install packages with system `python`, `pip`, or `pip3`.
- Do not use global interpreter state for this repo.
- Always prefer the project virtual environment located at `.venv`.
- Use commands such as:
  - `.venv/bin/python`
  - `.venv/bin/pip`
  - `.venv/bin/pytest`
  - `.venv/bin/ruff`
  - `.venv/bin/ty`
- If you need to activate the environment in a shell, use:
  - `source .venv/bin/activate`

## Setup
Use the project-managed setup flow from the repo root:

```bash
make install
```

This repo expects uv-managed dependency resolution and creates or uses `.venv` under the project root. If the environment is missing, initialize it before other Python work:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

If you need dev/test dependencies:

```bash
source .venv/bin/activate
python -m pip install -e '.[test]'
```

Or, when working with the project’s preferred tooling:

```bash
make install
```

## Testing and validation
Run checks with the project environment, not the system interpreter:

```bash
source .venv/bin/activate
pytest
```

Or directly from the venv:

```bash
.venv/bin/python -m pytest
```

Project lint/type-check commands:

```bash
source .venv/bin/activate
ruff check src/
ty check src/
```

Equivalent direct venv invocations:

```bash
.venv/bin/ruff check src/
.venv/bin/ty check src/
```

## Agent expectations
- Prefer working inside the repo root and using `.venv` for all Python commands.
- If a command needs a Python interpreter or package install, use `.venv/bin/...` explicitly.
- Prefer editing source files in `src/` and tests in `tests/`.
- Keep changes consistent with the project’s current packaging and CLI behavior.
- Validate with the relevant test or lint command before concluding work.

## Notes
The repository is configured to use `uv` and `.venv` for dependency management, and the Makefile targets already assume a local virtual environment. Follow that pattern consistently for any agent or automation working in this project.
