# Modern Python Monorepo

[![CI](https://github.com/gruckion/modern_python_monorepo/actions/workflows/pr.yml/badge.svg)](https://github.com/gruckion/modern_python_monorepo/actions/workflows/pr.yml)
[![codecov](https://codecov.io/gh/gruckion/modern_python_monorepo/branch/main/graph/badge.svg)](https://codecov.io/gh/gruckion/modern_python_monorepo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **uv + Una** Python monorepo template with best practices for modern Python development.

> **Note:** This project uses [**prek**](https://prek.j178.dev/) instead of pre-commit for git hooks.
> prek is a Rust-based reimplementation that's **10x faster**, uses **50% less disk space**,
> and requires no Python runtime. It's fully compatible with `.pre-commit-config.yaml`.

Designed for:

- Clean separation between reusable libraries and runnable apps
- Reproducible builds via Python wheels
- Fast development with Ruff, ty, pytest, and prek
- Docker support with multi-platform builds
- CI/CD with GitHub Actions and PyPI publishing

---

## Quick Start

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install prek for git hooks
uv tool install prek

# Clone and setup
git clone <repo-url>
cd modern_python_monorepo
uv sync --all-packages    # Install all deps + workspace packages
uv run poe hooks          # Install git hooks

# Verify setup
uv run poe all            # Format, lint, typecheck, test
```

---

## TL;DR

| Tool | Purpose |
|------|---------|
| [`uv`](https://docs.astral.sh/uv/) | Package management, virtualenvs, running commands |
| [`uv` Workspaces](https://docs.astral.sh/uv/concepts/workspaces/) | Monorepo layout |
| [`Una`](https://github.com/carderne/una) | Build wheels for apps with internal deps |

- If you only run code in Docker, `uv` alone is enough
- If you want to **package and distribute** apps as wheels, Una makes that practical

---

## Technology Stack

| Category | Tool | Notes |
|----------|------|-------|
| Package manager | [**uv**](https://docs.astral.sh/uv/) | Fast, Rust-based |
| Monorepo | [**Una**](https://github.com/carderne/una) | Workspace wiring + wheel builds |
| Python | [**3.13+**](https://www.python.org/) | Required minimum |
| Linting/Formatting | [**Ruff**](https://docs.astral.sh/ruff/) | Replaces black, isort, flake8 |
| Type checking | [**ty**](https://github.com/astral-sh/ty) | Astral's new Rust-based checker |
| Testing | [**pytest**](https://docs.pytest.org/) | With doctest support |
| Task runner | [**poethepoet**](https://poethepoet.naber.dev/) | Simple task definitions |
| Git hooks | [**prek**](https://prek.j178.dev/) | Rust-based pre-commit (10x faster) |

---

## Repository Layout

```text
.
├── pyproject.toml           # Workspace root + all tool configs
├── uv.lock                  # Lockfile (committed)
├── docker-compose.yml       # Container orchestration
├── docker-bake.hcl          # Multi-platform builds
├── .github/workflows/       # CI/CD
│   └── pr.yml
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

**Note:** All packages use the `modern_python_monorepo` namespace for consistent imports:

```python
from modern_python_monorepo import greeter
from modern_python_monorepo import printer
```

---

## Development Commands

All commands use `uv run poe <task>`:

```bash
# Individual tools
uv run poe fmt      # Format code (ruff)
uv run poe lint     # Lint + auto-fix (ruff)
uv run poe check    # Type check (ty)
uv run poe test     # Run tests (pytest)
uv run poe cov      # Run tests with coverage

# Run everything
uv run poe all      # fmt → lint → check → test

# CI versions (stricter, no auto-fix)
uv run poe ci:fmt   # Check formatting only
uv run poe ci:lint  # Lint without fixes
```

---

## Git Hooks (prek)

We use [**prek**](https://prek.j178.dev/) - a Rust-based reimplementation of pre-commit that's **10x faster** and requires no Python runtime. Hooks run automatically before each `git commit`.

### Why prek over pre-commit?

| Aspect | pre-commit | prek |
|--------|------------|------|
| Installation speed | ~187s | ~18s (10x faster) |
| Disk usage | 1.6 GB | 810 MB (50% less) |
| Dependencies | Requires Python | Single binary |
| Config compatibility | ✅ | ✅ (drop-in) |

### Setup (one-time)

```bash
# Install prek (if not installed)
uv tool install prek

# Install git hooks
uv run poe hooks
```

### What Runs on Commit

| Hook | Source | Action |
|------|--------|--------|
| `ruff --fix` | ruff-pre-commit | Lint and auto-fix issues |
| `ruff-format` | ruff-pre-commit | Auto-format code |
| `trailing-whitespace` | prek builtin | Remove trailing spaces |
| `end-of-file-fixer` | prek builtin | Ensure newline at EOF |
| `check-yaml` | prek builtin | Validate YAML files |
| `check-toml` | prek builtin | Validate TOML files |
| `check-added-large-files` | prek builtin | Prevent large file commits |
| `check-merge-conflict` | prek builtin | Detect merge conflicts |
| `detect-private-key` | prek builtin | Prevent key leaks |

### Run Manually

```bash
uv run poe hooks:run    # Run on all files
prek run --all-files    # Direct prek command
prek run ruff           # Run specific hook
```

If hooks make changes, the commit is blocked. Review the changes and commit again.

---

## Docker

### Build & Run

```bash
# Build production image
docker compose build printer

# Run container
docker compose up printer

# Development with live reload
docker compose watch printer-dev
```

### Multi-Platform Builds (Buildx Bake)

```bash
# Build for amd64 + arm64
docker buildx bake

# CI build with GitHub Actions cache
docker buildx bake ci
```

The Dockerfile uses:

- Multi-stage builds (smaller final image)
- BuildKit cache mounts (faster rebuilds)
- Non-root user (security)
- Pinned uv version (reproducibility)

---

## CI/CD

GitHub Actions runs on all PRs and pushes to `main`:

1. **prek hooks** – All hooks via [prek-action](https://github.com/j178/prek-action)
2. **Type check** – `ty check`
3. **Tests with coverage** – `pytest` with Codecov upload

See [`.github/workflows/pr.yml`](.github/workflows/pr.yml)

---

## Publishing to PyPI

### Automated Release (Recommended)

We use GitHub Actions with **Trusted Publishers** (OIDC) for secure, tokenless publishing.

#### Release via Git Tag

```bash
# Release all packages
git tag v0.1.0
git push origin v0.1.0

# Release specific package
git tag greeter-v0.1.0
git push origin greeter-v0.1.0
```

#### Manual Release via GitHub UI

1. Go to **Actions** → **Release to PyPI**
2. Click **Run workflow**
3. Select package (`all`, `greeter`, or `printer`)
4. Optionally check "Publish to TestPyPI" for testing

### First-Time Setup (PyPI Trusted Publisher)

Before the first release, configure PyPI to trust this repository:

1. Go to <https://pypi.org/manage/account/publishing/>
2. Add a pending publisher for each package:
   - **PyPI Project Name**: `greeter` or `printer`
   - **Owner**: Your GitHub username/org
   - **Repository**: `modern_python_monorepo`
   - **Workflow name**: `release.yml`
   - **Environment**: `pypi`

3. Create GitHub environments:
   - Go to repo **Settings** → **Environments**
   - Create `pypi` environment (optional: add reviewers for approval gate)
   - Create `test-pypi` environment for TestPyPI releases

### Manual Publishing (Local)

For local publishing without GitHub Actions:

```bash
# Build the package
uv build --package greeter

# Publish to PyPI
uv publish dist/greeter-*.whl dist/greeter-*.tar.gz

# Or publish to TestPyPI first
uv publish --publish-url https://test.pypi.org/legacy/ dist/*
```

#### Local Authentication

```bash
export UV_PUBLISH_USERNAME=__token__
export UV_PUBLISH_PASSWORD=pypi-xxxxx
```

---

## CLI Commands

After installing the packages, these CLI commands are available:

| Command | Package | Description |
|---------|---------|-------------|
| `greeter` | `greeter` | Run the greeter library |
| `printer` | `printer` | Run the printer application |

---

## Adding New Packages

### New Library

```bash
# Create structure
mkdir -p libs/mylib/modern_python_monorepo/mylib
touch libs/mylib/modern_python_monorepo/mylib/__init__.py
touch libs/mylib/modern_python_monorepo/mylib/py.typed
touch libs/mylib/modern_python_monorepo/py.typed

# Create pyproject.toml (copy from libs/greeter and modify)
cp libs/greeter/pyproject.toml libs/mylib/pyproject.toml
# Edit name, dependencies, etc.

# Sync workspace
uv sync --all-packages
```

### New App

Same pattern under `apps/`, plus add a `Dockerfile` if needed.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
