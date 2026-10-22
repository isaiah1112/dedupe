# Project Guidelines

## Project

`dedupe` is a Python command-line utility for finding duplicate files in one directory. Its CLI and hashing implementation are in `src/dedupe/__init__.py`; regression tests are in `tests/test_dedupe.py`.

Preserve the existing CLI behavior when changing it: MD5 is the default hash; SHA-1, SHA-256, and BLAKE3 are also supported. Hidden files and directories are skipped. Duplicates are moved into a `duplicates/` subdirectory unless `--remove` is selected.

## Python and dependencies

- Python 3.11 or newer is supported (`requires-python` in `pyproject.toml`); CI tests Python 3.11–3.15.
- Use `uv` and the repository-local `.venv` for setup and Python commands. Do not install packages into a global Python environment.
- `make install` runs the locked `uv sync` setup. Use `uv run --locked --group test ...` for direct commands.
- Keep dependency changes consistent between `pyproject.toml` and `uv.lock`.

## Validation

Prefer the Makefile targets:

```bash
make lint
make test
make coverage
```

`make lint` runs Ruff and `ty` on `src/`; `make test` runs pytest; `make coverage` runs pytest with a terminal coverage report. For a specific interpreter version, use `make docker-test PYTHON_VERSION=3.15`; `make docker-test-all` tests every version listed in the Makefile. The GitHub Actions workflow is `.github/workflows/python-tests.yml`; `ty` is informational there, while Ruff and the test matrix are required.

Run the relevant checks after changes. Update the README or CI/version matrix when changing user-facing behavior or supported Python versions.
