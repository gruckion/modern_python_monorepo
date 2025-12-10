# Frequently Asked Questions

Common questions about MPM CLI.

## General

??? question "What is MPM?"
    MPM (Modern Python Monorepo) is a CLI tool that scaffolds production-ready Python projects. It creates either monorepo structures with `apps/` and `libs/` directories, or single package projects. All projects come pre-configured with modern Rust-based tooling (uv, Ruff, ty, prek) and optional features like Docker, CI/CD, and documentation.

??? question "Do I need to install anything globally?"
    No. Run the CLI directly with your package manager:

    - `uvx mpm@latest` (recommended)
    - `pipx run modern-python-monorepo`

    See the [Quick Start](index.md) for all installation options.

??? question "What Python version is required?"
    Python 3.13+ is recommended. Python 3.11 and 3.12 are also supported. You can specify the version with `--python 3.12`.

??? question "Can I use this with an existing project?"
    MPM is designed for new projects. For existing projects, you can:

    - Use `mpm add` to add packages to an MPM-created monorepo
    - Manually copy the tooling configuration from a generated project
    - Start fresh and migrate code into the new structure

??? question "Where do generated files live?"
    See [Project Structure](project-structure.md) for detailed layouts of both monorepo and single package structures.

??? question "What's the difference between uvx, pipx, and pip?"
    - **uvx**: Runs the CLI in an isolated environment without permanent installation. Fastest option, recommended.
    - **pipx**: Similar to uvx, runs in isolation. Good if you already use pipx.
    - **pip**: Installs globally. Use if you want `mpm` permanently available.

## Choosing Options

??? question "Should I choose monorepo or single package?"
    **Choose monorepo** (`--monorepo`) when:

    - You have multiple related packages (apps and libraries)
    - You want to share code between packages
    - You're building a larger project that may grow

    **Choose single package** (`--single`) when:

    - You're building a standalone library or CLI tool
    - You want the simplest possible structure
    - You plan to publish a single package to PyPI

??? question "Which docs theme should I pick?"
    - **Material**: Classic, feature-rich, widely used. Great documentation and community support.
    - **Shadcn**: Modern, minimal aesthetic. Newer option with clean design.

    Both work well. Choose based on visual preference.

??? question "What do the sample packages include?"
    With `--with-samples`, you get:

    - `libs/greeter/`: A simple library using cowsay to generate greetings
    - `apps/printer/`: An application that uses the greeter library

    These demonstrate the dependency flow between libs and apps.

??? question "Should I enable all optional features?"
    Only enable what you need:

    - `--with-docker`: If you plan to containerize your applications
    - `--with-ci`: If you use GitHub Actions for continuous integration
    - `--with-pypi`: If you plan to publish packages to PyPI
    - `--with-docs`: If you want generated documentation site

    You can always add these manually later.

## Common Issues

??? question "Command not found: mpm"
    If you installed via pip but `mpm` isn't found:

    1. Ensure your Python scripts directory is in PATH
    2. Try running with full path: `python -m mpm`
    3. Use `uvx mpm@latest` instead (recommended)

??? question "Conflict with another `mpm` command"
    The name `mpm` may conflict with:

    - **Meta Package Manager**: A package management wrapper tool
    - **MiKTeX mpm**: LaTeX package manager (mostly Windows)

    Solutions:

    - Use `uvx modern-python-monorepo` (full package name, no conflict)
    - Uninstall the conflicting tool if you don't use it
    - Create an alias: `alias mpm='uvx mpm@latest'`

??? question "uv sync fails after project generation"
    If `uv sync --all-packages` fails:

    1. Ensure you have Python 3.13+ installed: `python --version`
    2. Install the correct Python version: `uv python install 3.13`
    3. Delete `.venv` and try again: `rm -rf .venv && uv sync --all-packages`
    4. Check for lockfile issues: `uv lock && uv sync --all-packages`

??? question "Git hooks not running"
    If pre-commit hooks don't run:

    1. Ensure prek is installed: `uv tool install prek`
    2. Install hooks: `uv run poe hooks`
    3. Verify `.git/hooks/pre-commit` exists

    To run hooks manually: `uv run poe hooks:run`

??? question "Type checker (ty) reports errors"
    ty is strict by default. Common fixes:

    1. Add type hints to all public functions
    2. Use `py.typed` marker files (included by default)
    3. Check that all dependencies have type stubs

??? question "Tests fail with import errors"
    Ensure all packages are installed in editable mode:

    ```bash
    uv sync --all-packages
    ```

    If still failing, check that the namespace structure is correct in each package.

## Adding Packages

??? question "How do I add a new package to my monorepo?"
    Use the `mpm add` command:

    ```bash
    # Interactive
    mpm add

    # Add a library
    mpm add lib my-lib

    # Add an application
    mpm add app my-app

    # Add an app with Docker support
    mpm add app my-api --docker
    ```

??? question "Can I add packages manually?"
    Yes. Create the directory structure following [Project Structure](project-structure.md), then run:

    ```bash
    uv sync --all-packages
    ```

    The `mpm add` command automates this for you.

??? question "How do packages depend on each other?"
    When your package imports from another internal package, you have two options:

    **Option 1: Auto-detect with `una sync` (recommended)**

    Simply write your imports, then run:

    ```bash
    uv run una sync
    ```

    This scans all packages, detects imports, and automatically updates `project.dependencies` and `tool.uv.sources` in each `pyproject.toml`.

    **Option 2: Manual configuration**

    In a package's `pyproject.toml`, add the dependency manually:

    ```toml
    [project]
    dependencies = ["greeter"]  # Name of the lib

    [tool.uv.sources]
    greeter = { workspace = true }
    ```

    Then import using the namespace:

    ```python
    from my_project import greeter
    ```

??? question "When should I run `uv run una sync`?"
    Run `una sync` whenever you:

    - Add a new package with `mpm add lib/app`
    - Write imports from one internal package to another
    - Want to verify all dependencies are correctly declared

    ```bash
    uv run una sync
    ```

    This command scans your code for imports and ensures they're properly declared as dependencies. It's safe to run frequently—it only updates what's needed.

## Technology Choices

MPM uses an opinionated, modern Python toolstack. For detailed comparisons and justifications, see the full [Technology Choices](technology-choices.md) documentation.

??? question "Why uv instead of pip, poetry, or pipenv?"
    **uv** is 10-100x faster than pip (written in Rust), provides all-in-one functionality (replaces pip + venv + pip-tools + pyenv), and has native monorepo workspace support. Poetry and pipenv are Python-based (slower) and have poor monorepo support.

    [Read full comparison →](technology-choices.md#1-package-manager-uv)

??? question "Why Ruff instead of black, isort, flake8, or pylint?"
    **Ruff** is 10-100x faster (Rust-based) and replaces all of these tools with a single binary. One `[tool.ruff]` config replaces `.flake8`, `.isort.cfg`, and `[tool.black]`. Most issues are auto-fixable.

    [Read full comparison →](technology-choices.md#2-linting-formatting-ruff)

??? question "Why prek instead of pre-commit?"
    **prek** is a Rust-based pre-commit alternative with faster hook execution and built-in offline-capable hooks. It uses the same `.pre-commit-config.yaml` format for easy migration.

    [Read full comparison →](technology-choices.md#3-pre-commit-hooks-prek)

??? question "Why pytest instead of unittest?"
    **pytest** has 90%+ adoption in modern Python. It offers simple `assert` syntax (vs verbose `self.assertEqual`), powerful fixtures, and a rich plugin ecosystem (pytest-cov, pytest-xdist, pytest-asyncio).

    [Read full comparison →](technology-choices.md#4-testing-pytest)

??? question "How do I speed up test runs during development?"
    Use `poe test:changed` instead of `poe test`. MPM includes **pytest-testmon** which tracks code dependencies and only runs tests affected by your changes:

    ```bash
    # First run builds dependency database
    uv run poe test:changed
    → 50 tests in 10s

    # After that, only changed tests run
    uv run poe test:changed
    → 0 tests in 0.1s (nothing changed!)
    ```

    This is the Python equivalent of Turborepo's test caching. Use `poe test` for full runs before committing.

    [Read full explanation →](technology-choices.md#pytest-testmon-turborepo-like-test-caching)

??? question "Why MkDocs instead of Sphinx?"
    **MkDocs** uses Markdown (more widely known than reStructuredText), has beautiful themes (Material, Shadcn), simple YAML config, and fast live reload. mkdocstrings generates API docs from docstrings.

    [Read full comparison →](technology-choices.md#5-documentation-mkdocs)

??? question "Why ty instead of mypy or pyright?"
    **ty** is Astral's Rust-based type checker offering 10-100x speed improvements over mypy. It's part of the unified Astral toolchain (uv, Ruff, ty) and auto-infers Python version from pyproject.toml.

    [Read full comparison →](technology-choices.md#6-type-checking-ty)

??? question "Why pyproject.toml instead of requirements.txt?"
    **pyproject.toml** is the modern Python standard (PEP 517/518/621). It provides a single source of truth for metadata, dependencies, build config, and all tool settings. No more juggling setup.py, requirements.txt, .flake8, and pytest.ini.

    [Read full comparison →](technology-choices.md#7-project-configuration-pyprojecttoml)

??? question "Why docker-bake instead of docker-compose build?"
    **docker buildx bake** enables parallel multi-target builds (80% faster for monorepos), multi-platform support (amd64 + arm64), declarative HCL config, and native GitHub Actions cache integration.

    [Read full comparison →](technology-choices.md#8-docker-builds-docker-bake)

??? question "Why Poe the Poet instead of Makefile?"
    **Poe the Poet** defines tasks directly in pyproject.toml (no separate file), works cross-platform (Windows, macOS, Linux), and integrates seamlessly with `uv run poe <task>`.

    [Read full comparison →](technology-choices.md#9-task-runner-poe-the-poet)

??? question "Why hatchling instead of setuptools?"
    **hatchling** is a modern PEP 517 build backend with a plugin system. The `hatch-una` plugin properly inlines internal monorepo dependencies into wheels, solving Python's monorepo packaging challenge.

    [Read full comparison →](technology-choices.md#10-build-backend-hatchling)

??? question "Why una instead of pants or bazel?"
    **una** is a lightweight Python monorepo tool designed for uv workspaces. It provides monorepo benefits (shared deps, namespace packages) without the massive complexity of enterprise build systems like pants or bazel.

    [Read full comparison →](technology-choices.md#11-monorepo-tool-una)

## Getting Help

- **Documentation**: [Quick Start](index.md), [Project Structure](project-structure.md), [Technology Choices](technology-choices.md)
- **Issues**: [GitHub Issues](https://github.com/gruckion/modern_python_monorepo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/gruckion/modern_python_monorepo/discussions)
