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

## Features

- **Monorepo or Single Package**: Choose your project structure
- **uv Workspaces**: Fast dependency management with uv
- **Una Integration**: Seamless monorepo builds with hatch-una
- **Modern Tooling**: Ruff, ty, pytest, poethepoet out of the box
- **Docker Support**: Multi-stage Dockerfiles with docker-bake.hcl
- **CI/CD**: GitHub Actions workflows for PR checks and PyPI publishing
- **Documentation**: MkDocs with Material or shadcn theme

## CLI Options

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

## License

MIT License
