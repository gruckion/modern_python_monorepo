# Options Reference

## General Options

### `--yes, -y`

Use default configuration and skip interactive prompts.

```bash
mpm my-project --yes
```

When used, the following defaults are applied:

| Option | Default Value |
|--------|---------------|
| Structure | `monorepo` |
| Python Version | `3.13` |
| License | `MIT` |
| Features | None enabled |

### `--version, -v`

Display the CLI version and exit.

```bash
mpm --version
```

### `--help, -h`

Display help information for the command.

```bash
mpm --help
mpm new --help
mpm add --help
mpm add lib --help
```

## Project Structure Options

### `--monorepo, -m`

Create a monorepo structure with `libs/` and `apps/` workspaces.

```bash
mpm my-project --monorepo -y
```

**Generated structure:**

```
my-project/
├── apps/           # Application packages
├── libs/           # Library packages
├── pyproject.toml  # Workspace configuration
├── mpm.toml        # MPM configuration
└── ...
```

### `--single, -s`

Create a single package structure without workspaces.

```bash
mpm my-lib --single -y
```

**Generated structure:**

```
my-lib/
├── src/
│   └── my_lib/
│       └── __init__.py
├── tests/
├── pyproject.toml
├── mpm.toml
└── ...
```

!!! note
    If both `--monorepo` and `--single` are specified, `--monorepo` takes precedence.

## Python Version

### `--python, -p <version>`

Set the minimum Python version requirement.

**Valid values:** `3.11`, `3.12`, `3.13`

**Default:** `3.13`

```bash
mpm my-project --python 3.12 -y
```

This sets:

- `.python-version` file content
- `requires-python` in `pyproject.toml`
- Python version in GitHub Actions workflows (if CI enabled)

## Feature Options

### `--with-samples`

Include sample packages to demonstrate the project structure.

```bash
mpm my-project --monorepo --with-samples -y
```

**What it creates:**

- `libs/greeter/` - Sample library with a greeting function
- `apps/printer/` - Sample application that uses the greeter library

!!! note
    Only applicable to monorepo projects. Ignored for single package projects.

### `--with-docker`

Include Docker configuration files.

```bash
mpm my-project --with-docker -y
```

**What it creates for monorepo:**

- `.dockerignore`
- `docker-compose.yml` (if sample apps exist)
- `docker-bake.hcl` (if sample apps exist)
- `Dockerfile` in each app with `--with-samples`

**What it creates for single package:**

- `.dockerignore`
- `Dockerfile`
- `docker-compose.yml`
- `docker-bake.hcl`

### `--with-ci`

Include GitHub Actions CI workflow for pull requests.

```bash
mpm my-project --with-ci -y
```

**What it creates:**

- `.github/workflows/pr.yml` - Runs on pull requests with:
    - Dependency installation with `uv`
    - Linting with `ruff`
    - Type checking with `ty`
    - Tests with `pytest`

### `--with-pypi`

Include GitHub Actions workflow for PyPI publishing.

```bash
mpm my-project --with-pypi -y
```

**What it creates:**

- `.github/workflows/release.yml` - Publishes to PyPI on GitHub releases

!!! warning
    Consider enabling `--with-ci` alongside `--with-pypi` for a complete CI/CD setup.

### `--with-docs`

Include MkDocs documentation site.

```bash
mpm my-project --with-docs -y
```

**What it creates:**

- `mkdocs.yml` - MkDocs configuration
- `docs/index.md` - Documentation home page
- Documentation dependencies in `pyproject.toml`
- Poe tasks: `docs` (serve), `docs-build` (build)

### `--docs-theme <theme>`

Set the MkDocs theme when documentation is enabled.

**Valid values:** `material`, `shadcn`

**Default:** `material`

```bash
mpm my-project --with-docs --docs-theme shadcn -y
```

| Theme | Description |
|-------|-------------|
| `material` | Material for MkDocs - feature-rich, widely used |
| `shadcn` | shadcn-inspired theme - modern, minimal design |

## License Options

### `--license, -l <type>`

Set the project license.

**Valid values:** `MIT`, `Apache-2.0`, `GPL-3.0`, `none`

**Default:** `MIT`

```bash
mpm my-project --license Apache-2.0 -y
```

**What it creates:**

- `LICENSE` file with the appropriate license text
- License field in `pyproject.toml`

| License | Description |
|---------|-------------|
| `MIT` | Permissive, simple, widely used |
| `Apache-2.0` | Permissive with patent protection |
| `GPL-3.0` | Copyleft, requires derivative works to be open source |
| `none` | No license file created |

## Output Control

### `--no-git`

Skip Git repository initialization.

```bash
mpm my-project --no-git -y
```

By default, MPM initializes a Git repository and creates an initial commit. Use this flag to skip that step.

### `--no-sync`

Skip running `uv sync` after project generation.

```bash
mpm my-project --no-sync -y
```

By default, MPM runs `uv sync --all-packages` (monorepo) or `uv sync` (single) after generating files to create the virtual environment and lock file.

## Package Addition Options

### `mpm add lib` Options

| Option | Short | Description |
|--------|-------|-------------|
| `--description` | `-d` | Library description for `pyproject.toml` |

```bash
mpm add lib auth --description "Authentication utilities"
```

### `mpm add app` Options

| Option | Short | Description |
|--------|-------|-------------|
| `--description` | `-d` | Application description for `pyproject.toml` |
| `--docker` | | Include Dockerfile for the application |

```bash
mpm add app api --docker --description "REST API service"
```

## Feature Addition Options

### `mpm add docs` Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--theme` | `-t` | MkDocs theme (`material`, `shadcn`) | `material` |

```bash
mpm add docs --theme shadcn
```

## Valid Values Reference

### Python Versions

| Value | Meaning |
|-------|---------|
| `3.11` | Python 3.11 or higher |
| `3.12` | Python 3.12 or higher |
| `3.13` | Python 3.13 or higher |

### License Types

| Value | License |
|-------|---------|
| `MIT` | MIT License |
| `Apache-2.0` | Apache License 2.0 |
| `GPL-3.0` | GNU General Public License v3.0 |
| `none` | No license |

### Documentation Themes

| Value | Theme |
|-------|-------|
| `material` | Material for MkDocs |
| `shadcn` | shadcn-inspired theme |

### Project Structures

| Value | Structure |
|-------|-----------|
| `monorepo` | Workspace with `libs/` and `apps/` |
| `single` | Single package without workspaces |

## Examples

### Full Production Setup

```bash
mpm my-api \
  --monorepo \
  --python 3.13 \
  --with-samples \
  --with-docker \
  --with-ci \
  --with-pypi \
  --with-docs \
  --docs-theme material \
  --license MIT \
  -y
```

### Minimal Library

```bash
mpm my-lib \
  --single \
  --python 3.12 \
  --license MIT \
  --no-git \
  -y
```

### CI-Ready Monorepo

```bash
mpm my-project \
  --monorepo \
  --with-ci \
  --with-pypi \
  -y
```
