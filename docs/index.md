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

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Getting Started**

    ---

    Get up and running with the monorepo in minutes

    [:octicons-arrow-right-24: Quick start guide](getting-started.md)

-   :material-cog:{ .lg .middle } **Development**

    ---

    Learn about development workflows and available commands

    [:octicons-arrow-right-24: Development guide](development/setup.md)

-   :material-docker:{ .lg .middle } **Docker**

    ---

    Build and run containers for production and development

    [:octicons-arrow-right-24: Docker guide](development/docker.md)

-   :material-file-tree:{ .lg .middle } **Architecture**

    ---

    Understand the monorepo structure and design decisions

    [:octicons-arrow-right-24: Architecture overview](architecture/overview.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Auto-generated API documentation from source code

    [:octicons-arrow-right-24: API docs](api/index.md)

-   :material-account-group:{ .lg .middle } **Contributing**

    ---

    Guidelines for contributing to the project

    [:octicons-arrow-right-24: Contributing guide](contributing.md)

</div>

## Why This Stack?

### Speed

All tooling is Rust-based where possible. `uv` is 10-100x faster than pip, `ruff` replaces multiple Python linters in milliseconds, and `prek` runs git hooks 10x faster than traditional pre-commit.

### Simplicity

One lockfile (`uv.lock`) for the entire workspace. One configuration file (`pyproject.toml`) for all tool settings. Consistent commands via `poe` tasks.

### Reliability

Deterministic builds with locked dependencies. Type checking catches errors before runtime. Automated CI/CD ensures code quality on every change.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/gruckion/modern_python_monorepo/blob/main/LICENSE) file for details.
