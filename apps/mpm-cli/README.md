# MPM - Modern Python Monorepo CLI

A scaffolding tool for creating production-ready Python monorepo projects.

## Installation

```bash
# Via uvx (recommended)
uvx mpm@latest

# Via pipx
pipx run modern-python-monorepo

# Via pip
pip install modern-python-monorepo
```

## Usage

### Create a New Project

```bash
# Interactive mode
mpm

# With project name
mpm my-project

# Non-interactive with flags
mpm my-project --monorepo --with-docker --with-ci -y

# Single package mode
mpm my-project --single -y
```

### Add Packages to Existing Project

```bash
# Interactive
mpm add

# Add library
mpm add lib auth

# Add application with Docker support
mpm add app api --docker
```

### Add Features to Existing Project

After creating a project, you can add features incrementally:

```bash
# Add Docker configuration
mpm add docker

# Add GitHub Actions CI
mpm add ci

# Add PyPI publishing workflow
mpm add pypi

# Add MkDocs documentation (default: material theme)
mpm add docs

# Add docs with shadcn theme
mpm add docs --theme shadcn
```

#### Feature Commands

| Command | Description |
|---------|-------------|
| `mpm add docker` | Adds `.dockerignore`, and for single packages: `Dockerfile`, `docker-compose.yml`, `docker-bake.hcl` |
| `mpm add ci` | Adds GitHub Actions PR workflow (`.github/workflows/pr.yml`) |
| `mpm add pypi` | Adds PyPI release workflow (`.github/workflows/release.yml`) |
| `mpm add docs` | Adds MkDocs with `mkdocs.yml`, `docs/index.md`, and updates `pyproject.toml` with docs dependencies |

## mpm.toml Configuration

When you create a project with `mpm`, it generates an `mpm.toml` file at the project root. This file stores your project configuration and is used by `mpm add` commands to maintain consistency.

### Schema

```toml
[mpm]
version = "0.1.0"
created_at = "2024-01-15T10:30:00"

[project]
name = "my-project"
slug = "my_project"
structure = "monorepo"  # or "single"
python_version = "3.13"
license = "MIT"

[features]
docker = false
ci = false
pypi = false
docs = false
docs_theme = "material"  # or "shadcn"
samples = false
```

### How It Works

1. **Project Creation**: `mpm new` generates `mpm.toml` with your initial choices
2. **Adding Packages**: `mpm add lib/app` reads namespace and Python version from `mpm.toml`
3. **Adding Features**: `mpm add docker/ci/pypi/docs` updates the `[features]` section
4. **Idempotency**: Running a feature command twice is safe - it warns if already enabled

### Backward Compatibility

Projects without `mpm.toml` (created before this feature) are still supported. The `mpm add lib/app` commands will fall back to reading from `[tool.una]` in `pyproject.toml`.

## Features

- **Monorepo or Single Package**: Choose your project structure
- **uv Workspaces**: Fast dependency management with uv
- **Una Integration**: Seamless monorepo builds with hatch-una
- **Modern Tooling**: Ruff, ty, pytest, poethepoet out of the box
- **Docker Support**: Multi-stage Dockerfiles with docker-bake.hcl
- **CI/CD**: GitHub Actions workflows for PR checks and PyPI publishing
- **Documentation**: MkDocs with Material or shadcn theme
- **Incremental Features**: Add Docker, CI, PyPI, or Docs after project creation

## CLI Options

### Project Creation (`mpm new`)

| Flag | Description |
|------|-------------|
| `--monorepo`, `-m` | Create monorepo structure |
| `--single`, `-s` | Create single package structure |
| `--python`, `-p` | Python version (3.11, 3.12, 3.13) |
| `--with-samples` | Include sample packages |
| `--with-docker` | Include Docker configuration |
| `--with-ci` | Include GitHub Actions CI |
| `--with-pypi` | Include PyPI publishing workflow |
| `--with-docs` | Include MkDocs documentation |
| `--docs-theme` | Docs theme: material or shadcn |
| `--license`, `-l` | License: MIT, Apache-2.0, GPL-3.0, none |
| `--no-git` | Skip git initialization |
| `--yes`, `-y` | Accept defaults (non-interactive) |

### Adding Packages (`mpm add lib/app`)

| Flag | Description |
|------|-------------|
| `--docker` | Add Dockerfile to the app (apps only) |

### Adding Features (`mpm add docker/ci/pypi/docs`)

| Command | Options |
|---------|---------|
| `mpm add docker` | None |
| `mpm add ci` | None |
| `mpm add pypi` | None |
| `mpm add docs` | `--theme` (material, shadcn) |

## License

MIT License
