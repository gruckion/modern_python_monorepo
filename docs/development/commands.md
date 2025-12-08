# Commands Reference

All development tasks are managed through [poethepoet](https://poethepoet.naber.dev/) (poe), providing a unified interface for common operations.

## Running Commands

All commands are run via `uv run poe <task>`:

```bash
uv run poe <task>
```

## Available Tasks

### Code Quality

| Command | Description |
|---------|-------------|
| `uv run poe fmt` | Format code with Ruff |
| `uv run poe lint` | Lint code with Ruff (auto-fixes issues) |
| `uv run poe check` | Type check with ty |
| `uv run poe all` | Run fmt, lint, check, and test in sequence |

### Testing

| Command | Description |
|---------|-------------|
| `uv run poe test` | Run pytest |
| `uv run poe cov` | Run pytest with coverage report |

### CI Commands

These commands are stricter versions used in CI (no auto-fix):

| Command | Description |
|---------|-------------|
| `uv run poe ci:fmt` | Check formatting without fixing |
| `uv run poe ci:lint` | Lint without auto-fixing |

### Git Hooks

| Command | Description |
|---------|-------------|
| `uv run poe hooks` | Install prek git hooks |
| `uv run poe hooks:run` | Run all hooks on all files |

### Documentation

| Command | Description |
|---------|-------------|
| `uv run poe docs` | Start local docs server at http://127.0.0.1:8000 |
| `uv run poe docs:build` | Build static documentation site |

## Task Definitions

All tasks are defined in `pyproject.toml` under `[tool.poe.tasks]`:

```toml
[tool.poe.tasks]
# Code quality
fmt = "ruff format"
lint = "ruff check --fix"
check = "ty check"
test = "pytest"
cov = "pytest --cov=apps --cov=libs --cov-report=term-missing --cov-report=xml"
all = ["fmt", "lint", "check", "test"]

# CI versions (no auto-fix, stricter)
"ci:fmt" = "ruff format --check"
"ci:lint" = "ruff check"

# Git hooks
hooks = "prek install"
"hooks:run" = "prek run --all-files"

# Documentation
docs = "mkdocs serve"
"docs:build" = "mkdocs build"
```

## Command Details

### Formatting (`fmt`)

Runs `ruff format` to automatically format all Python files according to the project's style configuration.

```bash
uv run poe fmt
```

Ruff's formatter is compatible with Black and formats code consistently across the entire codebase.

### Linting (`lint`)

Runs `ruff check --fix` to lint code and automatically fix issues where possible.

```bash
uv run poe lint
```

The linter checks for:

- Pycodestyle errors and warnings (E, W)
- Pyflakes errors (F)
- Flake8-bugbear issues (B)
- Import sorting (I)
- PEP8 naming conventions (N)
- Modern Python syntax (UP)
- Built-in shadowing (A)
- Debugger breakpoints (T100)
- Ruff-specific rules (RUF)

### Type Checking (`check`)

Runs `ty check` for static type analysis.

```bash
uv run poe check
```

ty is Astral's Rust-based type checker, designed to be fast and compatible with Python's type system.

### Testing (`test`)

Runs pytest with verbose output and doctest support.

```bash
uv run poe test
```

Tests are discovered in `apps/` and `libs/` directories, matching files named `test_*.py`.

### Coverage (`cov`)

Runs pytest with coverage collection and reporting.

```bash
uv run poe cov
```

This generates:

- Terminal output with line-by-line coverage
- `coverage.xml` for CI integration
- Coverage data in `.coverage` file

### All Checks (`all`)

Runs the complete check sequence: format, lint, type check, test.

```bash
uv run poe all
```

This is the recommended command before committing changes.

## Direct Tool Access

You can also run tools directly if needed:

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest -xvs apps/printer/tests/
uv run ty check libs/greeter/
```
