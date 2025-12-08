# Architecture Overview

This document explains the architecture and design decisions of the Modern Python Monorepo.

## Monorepo Structure

```
modern_python_monorepo/
├── pyproject.toml           # Workspace root + all tool configs
├── uv.lock                  # Single lockfile for entire workspace
├── mkdocs.yml               # Documentation configuration
├── docker-compose.yml       # Container orchestration
├── docker-bake.hcl          # Multi-platform builds
├── .github/workflows/       # CI/CD pipelines
│   └── pr.yml
├── docs/                    # Documentation source (MkDocs)
├── apps/                    # Runnable applications
│   └── printer/
│       ├── pyproject.toml
│       ├── Dockerfile
│       └── modern_python_monorepo/
│           └── printer/
│               ├── __init__.py
│               └── py.typed
└── libs/                    # Reusable libraries
    └── greeter/
        ├── pyproject.toml
        └── modern_python_monorepo/
            └── greeter/
                ├── __init__.py
                └── py.typed
```

## Key Concepts

### Apps vs Libs

The monorepo separates code into two categories:

| Category | Location | Purpose | Can Depend On |
|----------|----------|---------|---------------|
| **Libraries** | `libs/` | Reusable code shared across apps | Other libs only |
| **Applications** | `apps/` | Runnable programs with entry points | Libs and other apps |

This separation enforces a clear dependency hierarchy and prevents circular dependencies.

### Namespace Package

All packages use the `modern_python_monorepo` namespace:

```python
from modern_python_monorepo import greeter
from modern_python_monorepo import printer
```

This provides:

- **Consistent imports** across the entire codebase
- **Collision avoidance** with external packages
- **Clear ownership** of code within the organization

### Workspace Management

#### uv Workspaces

uv manages the workspace through `pyproject.toml`:

```toml
[tool.uv.workspace]
members = ["apps/*", "libs/*"]
```

This tells uv to:

- Discover all packages in `apps/` and `libs/`
- Install them in editable mode during development
- Share a single lockfile (`uv.lock`)

#### Una Integration

[Una](https://github.com/carderne/una) handles building distributable wheels:

```toml
[tool.una]
namespace = "modern_python_monorepo"
requires-python = ">=3.13"
```

When building a wheel for `printer`, Una automatically bundles the `greeter` dependency into the wheel, making it self-contained for distribution.

## Dependency Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     External PyPI Packages                   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ depends on
                              │
┌─────────────────────────────────────────────────────────────┐
│                          libs/                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  greeter                                             │    │
│  │  - cowsay-python (external)                         │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ depends on
                              │
┌─────────────────────────────────────────────────────────────┐
│                          apps/                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  printer                                             │    │
│  │  - greeter (workspace)                              │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Package Structure

Each package follows this structure:

```
package_name/
├── pyproject.toml                    # Package metadata and dependencies
├── modern_python_monorepo/           # Namespace directory
│   └── package_name/                 # Actual package code
│       ├── __init__.py               # Package entry point
│       └── py.typed                  # PEP 561 marker for type hints
└── tests/                            # Package-specific tests
    └── test_*.py
```

### pyproject.toml (Package)

Each package has its own `pyproject.toml`:

```toml
[project]
name = "greeter"
version = "0.1.0"
dependencies = ["cowsay-python==1.0.2"]
requires-python = ">=3.13"
dynamic = ["una"]

[project.scripts]
greeter = "modern_python_monorepo.greeter:main"

[build-system]
requires = ["hatchling", "hatch-una"]
build-backend = "hatchling.build"

[tool.hatch.build.hooks.una-build]
[tool.hatch.metadata.hooks.una-meta]
```

## Tool Configuration

All tool configuration lives in the root `pyproject.toml`:

### Ruff (Linting & Formatting)

```toml
[tool.ruff]
line-length = 120

[tool.ruff.lint]
select = ["A", "B", "E", "F", "I", "N", "UP", "W", "RUF", "T100"]

[tool.ruff.lint.isort]
known-first-party = ["modern_python_monorepo"]
```

### Pytest (Testing)

```toml
[tool.pytest.ini_options]
testpaths = ["apps", "libs"]
python_files = ["test_*.py"]
addopts = "--doctest-modules -v"
```

### Coverage

```toml
[tool.coverage.run]
source = ["apps", "libs"]
omit = ["*/tests/*", "*/__pycache__/*"]
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/pr.yml`) runs on every PR:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Checkout  │───▶│  Setup uv   │───▶│ Install deps│───▶│ Check lock  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                │
                                                                ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Codecov   │◀───│  Tests+Cov  │◀───│  Type check │◀───│ prek hooks  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Design Decisions

### Why uv?

- **10-100x faster** than pip for dependency resolution
- **Single lockfile** for deterministic builds
- **Built-in workspace support** for monorepos
- **Rust-based** reliability and speed

### Why Una?

- Solves the "wheel bundling" problem for monorepos
- Apps can include internal library code in their wheels
- Makes packages truly distributable to PyPI

### Why Namespace Packages?

- Prevents import collisions with external packages
- Provides organizational clarity
- Enables future package splitting if needed

### Why Separate apps/ and libs/?

- Enforces dependency direction (apps depend on libs, not vice versa)
- Clear distinction between "runnable" and "importable" code
- Mirrors common enterprise patterns
