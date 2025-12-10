# Quick Start

Create production-ready Python monorepo projects in minutes.

## Philosophy

- **Roll your own stack**: pick only what you need, nothing extra.
- **Modern tooling**: Rust-based tools (uv, Ruff, ty, prek) for 10-100x speed.
- **Production-ready**: CI/CD, Docker, PyPI publishing out of the box.
- **Free and open source**: forever.

## Get Started

### Prerequisites

- **Python 3.13+** - [Download from python.org](https://www.python.org/downloads/) or install via `uv python install 3.13`
- **uv** (recommended) - [Install from astral.sh](https://docs.astral.sh/uv/getting-started/installation/)
- **Git** (optional) - [Download from git-scm.com](https://git-scm.com/) - if you want to initialize a git repository

### CLI (Interactive)

=== "uvx"

    ```bash
    uvx mpm@latest
    ```

=== "pipx"

    ```bash
    pipx run modern-python-monorepo
    ```

=== "pip"

    ```bash
    pip install modern-python-monorepo
    mpm
    ```

Follow the interactive prompts to choose your project structure, Python version, and optional features.

### Skip Prompts (Defaults)

=== "uvx"

    ```bash
    uvx mpm@latest my-project --yes
    ```

=== "pipx"

    ```bash
    pipx run modern-python-monorepo my-project --yes
    ```

=== "pip"

    ```bash
    mpm my-project --yes
    ```

## Common Setups

### Default Monorepo

A monorepo with sample packages to get you started:

=== "uvx"

    ```bash
    uvx mpm@latest my-project \
      --monorepo \
      --with-samples \
      --with-ci \
      -y
    ```

=== "pipx"

    ```bash
    pipx run modern-python-monorepo my-project \
      --monorepo \
      --with-samples \
      --with-ci \
      -y
    ```

=== "pip"

    ```bash
    mpm my-project \
      --monorepo \
      --with-samples \
      --with-ci \
      -y
    ```

### Minimal Single Package

A single library or application without monorepo overhead:

=== "uvx"

    ```bash
    uvx mpm@latest my-lib \
      --single \
      -y
    ```

=== "pipx"

    ```bash
    pipx run modern-python-monorepo my-lib \
      --single \
      -y
    ```

=== "pip"

    ```bash
    mpm my-lib \
      --single \
      -y
    ```

### Full Production Setup

Everything enabled for a production-ready project:

=== "uvx"

    ```bash
    uvx mpm@latest my-api \
      --monorepo \
      --with-samples \
      --with-docker \
      --with-ci \
      --with-pypi \
      --with-docs \
      --docs-theme material \
      -y
    ```

=== "pipx"

    ```bash
    pipx run modern-python-monorepo my-api \
      --monorepo \
      --with-samples \
      --with-docker \
      --with-ci \
      --with-pypi \
      --with-docs \
      --docs-theme material \
      -y
    ```

=== "pip"

    ```bash
    mpm my-api \
      --monorepo \
      --with-samples \
      --with-docker \
      --with-ci \
      --with-pypi \
      --with-docs \
      --docs-theme material \
      -y
    ```

### Empty Monorepo

A clean monorepo structure without sample packages:

=== "uvx"

    ```bash
    uvx mpm@latest my-workspace \
      --monorepo \
      -y
    ```

=== "pipx"

    ```bash
    pipx run modern-python-monorepo my-workspace \
      --monorepo \
      -y
    ```

=== "pip"

    ```bash
    mpm my-workspace \
      --monorepo \
      -y
    ```

## Flags Cheat Sheet

See the full list in the [CLI Commands](cli/commands.md). Key flags:

| Flag | Short | Description |
|------|-------|-------------|
| `--monorepo` | `-m` | Create monorepo structure (default) |
| `--single` | `-s` | Create single package structure |
| `--with-samples` | | Include sample packages |
| `--with-docker` | | Include Docker configuration |
| `--with-ci` | | Include GitHub Actions CI |
| `--with-docs` | | Include MkDocs documentation |
| `--yes` | `-y` | Accept defaults (non-interactive) |

## Adding Packages

Add new packages to an existing monorepo (see [CLI Commands](cli/commands.md#add) for full details):

=== "uvx"

    ```bash
    # Interactive
    uvx mpm@latest add

    # Add a library
    uvx mpm@latest add lib auth

    # Add an application with Docker
    uvx mpm@latest add app api --docker
    ```

=== "pipx"

    ```bash
    # Interactive
    pipx run modern-python-monorepo add

    # Add a library
    pipx run modern-python-monorepo add lib auth

    # Add an application with Docker
    pipx run modern-python-monorepo add app api --docker
    ```

=== "pip"

    ```bash
    # Interactive
    mpm add

    # Add a library
    mpm add lib auth

    # Add an application with Docker
    mpm add app api --docker
    ```

## Adding Features

Add features to an existing project after creation:

```bash
cd my-project

# Add Docker configuration
mpm add docker

# Add GitHub Actions CI
mpm add ci

# Add PyPI publishing workflow
mpm add pypi

# Add MkDocs documentation
mpm add docs --theme material
```

These commands update your [mpm.toml](mpm-toml.md) configuration file. See [CLI Commands](cli/commands.md#add) for details.

## Next Steps

| Section | Description |
|---------|-------------|
| [**CLI Commands**](cli/commands.md) | Full reference for all CLI commands and options |
| [**mpm.toml**](mpm-toml.md) | Configuration file schema and usage |
| [**Project Structure**](project-structure.md) | How monorepo and single package layouts are generated |
| [**Contributing**](contributing.md) | Dev setup and contribution flow |
| [**FAQ**](faq.md) | Common questions and troubleshooting |
