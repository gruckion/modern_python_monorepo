# Modern Python Monorepo

A **uv + Una** Python monorepo template with best practices for modern Python development.

[![CI](https://github.com/gruckion/modern_python_monorepo/actions/workflows/pr.yml/badge.svg)](https://github.com/gruckion/modern_python_monorepo/actions/workflows/pr.yml)
[![codecov](https://codecov.io/gh/gruckion/modern_python_monorepo/branch/main/graph/badge.svg)](https://codecov.io/gh/gruckion/modern_python_monorepo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is this?

This is a production-ready monorepo template for Python projects that demonstrates how to structure, build, and maintain multiple related Python packages in a single repository. It combines the speed of modern Rust-based tooling with established Python best practices.

## Key Features

- **Clean separation** between reusable libraries (`libs/`) and runnable applications (`apps/`)
- **Reproducible builds** via Python wheels using Una for internal dependency bundling
- **Fast development** with Ruff (linting/formatting), ty (type checking), and pytest
- **Docker support** with multi-stage builds and BuildKit optimizations
- **CI/CD ready** with GitHub Actions and PyPI publishing via trusted publishers

## Technology Stack

| Category | Tool | Purpose |
|----------|------|---------|
| Package manager | [**uv**](https://docs.astral.sh/uv/) | Fast, Rust-based package management |
| Monorepo | [**Una**](https://github.com/carderne/una) | Workspace wiring + wheel builds |
| Python | **3.13+** | Required minimum version |
| Linting/Formatting | [**Ruff**](https://docs.astral.sh/ruff/) | Replaces black, isort, flake8 |
| Type checking | [**ty**](https://github.com/astral-sh/ty) | Astral's Rust-based type checker |
| Testing | [**pytest**](https://docs.pytest.org/) | With doctest support |
| Task runner | [**poethepoet**](https://poethepoet.naber.dev/) | Simple task definitions |
| Git hooks | [**prek**](https://prek.j178.dev/) | Rust-based pre-commit (10x faster) |

## Quick Navigation

| Section | Description |
|---------|-------------|
| [**Getting Started**](getting-started.md) | Get up and running with the monorepo in minutes |
| [**Development Setup**](development/setup.md) | Learn about development workflows and environment |
| [**Commands Reference**](development/commands.md) | All available poe tasks and commands |
| [**Docker Guide**](development/docker.md) | Build and run containers for production and development |
| [**Architecture**](architecture/overview.md) | Understand the monorepo structure and design decisions |
| [**API Reference**](api/index.md) | Auto-generated API documentation from source code |
| [**Contributing**](contributing.md) | Guidelines for contributing to the project |

## Why This Stack?

### Speed

All tooling is Rust-based where possible. `uv` is 10-100x faster than pip, `ruff` replaces multiple Python linters in milliseconds, and `prek` runs git hooks 10x faster than traditional pre-commit.

### Simplicity

One lockfile (`uv.lock`) for the entire workspace. One configuration file (`pyproject.toml`) for all tool settings. Consistent commands via `poe` tasks.

### Reliability

Deterministic builds with locked dependencies. Type checking catches errors before runtime. Automated CI/CD ensures code quality on every change.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/gruckion/modern_python_monorepo/blob/main/LICENSE) file for details.
