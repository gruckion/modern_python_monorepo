# Project Structure

Understanding the structure of projects created by MPM CLI.

## Overview

MPM CLI scaffolds either a **monorepo** with `apps/` and `libs/` directories, or a **single package** structure. The exact files generated depend on your choices (structure, Docker, CI, docs, samples). This page documents what the CLI actually writes.

## Root Layout

### Monorepo Structure

At the repository root you will see:

```
my-project/
├── apps/                    # Runnable applications
├── libs/                    # Reusable libraries
├── pyproject.toml           # Workspace root + all tool configs
├── uv.lock                  # Single lockfile for entire workspace
├── README.md                # Generated quickstart
├── LICENSE                  # (if license selected)
├── .gitignore               # Python/uv gitignore
├── .python-version          # Python version pin
├── prek.toml                # Git hooks configuration
├── docs/                    # (if --with-docs)
├── mkdocs.yml               # (if --with-docs)
├── docker-compose.yml       # (if --with-docker)
├── docker-bake.hcl          # (if --with-docker)
└── .github/                 # (if --with-ci or --with-pypi)
    └── workflows/
        ├── pr.yml           # (if --with-ci)
        └── publish.yml      # (if --with-pypi)
```

Notes:

- `apps/` contains runnable applications with entry points.
- `libs/` contains reusable libraries shared across apps.
- All tool configuration lives in the root `pyproject.toml`.

### Single Package Structure

```
my-lib/
├── src/
│   └── my_lib/
│       ├── __init__.py      # Package entry point
│       └── py.typed         # PEP 561 marker for type hints
├── tests/
│   └── test_my_lib.py       # Package tests
├── pyproject.toml           # Package configuration
├── uv.lock                  # Locked dependencies
├── README.md                # Generated quickstart
├── LICENSE                  # (if license selected)
├── .gitignore               # Python/uv gitignore
├── .python-version          # Python version pin
├── prek.toml                # Git hooks configuration
├── Dockerfile               # (if --with-docker)
├── docs/                    # (if --with-docs)
├── mkdocs.yml               # (if --with-docs)
└── .github/                 # (if --with-ci or --with-pypi)
    └── workflows/
        ├── pr.yml           # (if --with-ci)
        └── publish.yml      # (if --with-pypi)
```

## Monorepo with Samples

When you use `--with-samples`, MPM creates example packages:

```
my-project/
├── apps/
│   └── printer/             # Example app that uses greeter lib
│       ├── pyproject.toml
│       ├── Dockerfile       # (if --with-docker)
│       └── my_project/
│           └── printer/
│               ├── __init__.py
│               └── py.typed
└── libs/
    └── greeter/             # Example library with cowsay
        ├── pyproject.toml
        └── my_project/
            └── greeter/
                ├── __init__.py
                └── py.typed
```

## Package Structure

### Application Package (apps/)

Each application in `apps/` follows this structure:

```
apps/my-app/
├── pyproject.toml                    # Package metadata and dependencies
├── Dockerfile                        # (if --with-docker or mpm add app --docker)
├── my_project/                       # Namespace directory
│   └── my_app/                       # Actual package code
│       ├── __init__.py               # Package entry point with main()
│       └── py.typed                  # PEP 561 marker
└── tests/                            # Package-specific tests
    └── test_my_app.py
```

#### pyproject.toml (Application)

```toml
[project]
name = "my-app"
version = "0.1.0"
dependencies = ["greeter"]  # Can depend on libs
requires-python = ">=3.13"
dynamic = ["una"]

[project.scripts]
my-app = "my_project.my_app:main"

[build-system]
requires = ["hatchling", "hatch-una"]
build-backend = "hatchling.build"

[tool.hatch.build.hooks.una-build]
[tool.hatch.metadata.hooks.una-meta]
```

### Library Package (libs/)

Each library in `libs/` follows this structure:

```
libs/my-lib/
├── pyproject.toml                    # Package metadata and dependencies
├── my_project/                       # Namespace directory
│   └── my_lib/                       # Actual package code
│       ├── __init__.py               # Library functions
│       └── py.typed                  # PEP 561 marker
└── tests/                            # Package-specific tests
    └── test_my_lib.py
```

#### pyproject.toml (Library)

```toml
[project]
name = "my-lib"
version = "0.1.0"
dependencies = []
requires-python = ">=3.13"
dynamic = ["una"]

[build-system]
requires = ["hatchling", "hatch-una"]
build-backend = "hatchling.build"

[tool.hatch.build.hooks.una-build]
[tool.hatch.metadata.hooks.una-meta]
```

## Namespace Package

All packages use a shared namespace based on your project name:

```python
# Import from any package in the monorepo
from my_project import greeter
from my_project import printer

# Use the library
greeting = greeter.greet("Hello!")
```

This provides:

- **Consistent imports** across the entire codebase
- **Collision avoidance** with external PyPI packages
- **Clear ownership** of code within the project

## Configuration Files

### Root pyproject.toml

The root `pyproject.toml` contains workspace configuration and all tool settings:

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.13"

[tool.uv.workspace]
members = ["apps/*", "libs/*"]

[tool.una]
namespace = "my_project"
requires-python = ">=3.13"

[tool.poe.tasks]
fmt = "ruff format"
lint = "ruff check --fix"
check = "ty check"
test = "pytest"
cov = "pytest --cov=apps --cov=libs --cov-report=term-missing"
all = ["fmt", "lint", "check", "test"]

[tool.ruff]
line-length = 120

[tool.ruff.lint]
select = ["A", "B", "E", "F", "I", "N", "UP", "W", "RUF", "T100"]

[tool.pytest.ini_options]
testpaths = ["apps", "libs"]
python_files = ["test_*.py"]
addopts = "--doctest-modules -v"

[tool.coverage.run]
source = ["apps", "libs"]
omit = ["*/tests/*"]
```

### Docker Configuration

When `--with-docker` is selected:

#### Dockerfile (per app)

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY . .
RUN uv build apps/printer --wheel --out-dir dist

FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY --from=builder /app/dist/*.whl /tmp/
RUN uv pip install --system /tmp/*.whl && rm /tmp/*.whl
ENTRYPOINT ["printer"]
```

#### docker-compose.yml

```yaml
services:
  printer:
    build:
      context: .
      dockerfile: apps/printer/Dockerfile
```

#### docker-bake.hcl

```hcl
group "default" {
  targets = ["printer"]
}

target "printer" {
  dockerfile = "apps/printer/Dockerfile"
  tags = ["my-project/printer:latest"]
}
```

### CI/CD Configuration

When `--with-ci` is selected:

#### .github/workflows/pr.yml

```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync --all-packages
      - run: uv run poe ci:fmt
      - run: uv run poe ci:lint
      - run: uv run poe check
      - run: uv run poe cov
```

When `--with-pypi` is selected:

#### .github/workflows/publish.yml

```yaml
name: Publish to PyPI
on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv build apps/printer --wheel
      - uses: pypa/gh-action-pypi-publish@release/v1
```

### Documentation Configuration

When `--with-docs` is selected:

#### mkdocs.yml

```yaml
site_name: My Project
theme:
  name: material  # or shadcn based on --docs-theme

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - API Reference:
      - Overview: api/index.md

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
```

## Development Scripts

All projects include [poethepoet](https://poethepoet.naber.dev/) tasks:

| Command | Description |
|---------|-------------|
| `uv run poe fmt` | Format code with Ruff |
| `uv run poe lint` | Lint code with Ruff (auto-fixes) |
| `uv run poe check` | Type check with ty |
| `uv run poe test` | Run pytest |
| `uv run poe cov` | Run pytest with coverage |
| `uv run poe all` | Run fmt, lint, check, test in sequence |
| `uv run poe docs` | Start local docs server (if --with-docs) |
| `uv run poe docs:build` | Build static docs (if --with-docs) |

## Key Details

- **Monorepo**: `apps/` for applications, `libs/` for libraries
- **Single package**: `src/` layout with tests alongside
- **Namespace**: All packages share `{project_name}.{package_name}` imports
- **Una integration**: Builds self-contained wheels with internal dependencies bundled
- **Tool config**: All tools configured in root `pyproject.toml`
- **Git hooks**: prek runs Ruff formatting/linting on commit
- **Docker**: Multi-stage builds with uv for fast, small images
- **CI/CD**: GitHub Actions with trusted PyPI publishing

This reflects the actual files written by the CLI so new projects match what's documented here.
