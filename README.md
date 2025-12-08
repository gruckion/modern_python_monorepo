# GPT Architecture – Neural Architecture Experiments (uv + Una + MPS)

A **uv + Una** Python monorepo for experimenting with neural network architectures on Apple Silicon (M2/M3, MPS backend).

Designed for:
- Fast iteration on new model architectures
- Clean separation between reusable libraries and runnable apps
- Reproducible builds via Python wheels
- Local training on MPS with PyTorch

---

## Quick Start

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone <repo-url>
cd gpt_architecture
uv sync --all-packages    # Install all deps + workspace packages

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
| Package manager | **uv** | Fast, Rust-based |
| Monorepo | **Una** | Workspace wiring + wheel builds |
| Python | **3.13+** | Required minimum |
| Linting/Formatting | **Ruff** | Replaces black, isort, flake8 |
| Type checking | **ty** | Astral's new Rust-based checker |
| Testing | **pytest** | With doctest support |
| Task runner | **poethepoet** | Simple task definitions |
| Pre-commit | **pre-commit** | Git hooks for code quality |
| ML Framework | **PyTorch** | MPS backend for Apple Silicon |

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
│       └── gpt_architecture/
│           └── printer/
│               ├── __init__.py
│               └── py.typed
└── libs/                    # Reusable libraries
    └── greeter/
        ├── pyproject.toml
        └── gpt_architecture/
            └── greeter/
                ├── __init__.py
                └── py.typed
```

**Note:** All packages use the `gpt_architecture` namespace for consistent imports:
```python
from gpt_architecture import greeter
from gpt_architecture import printer
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

# Run everything
uv run poe all      # fmt → lint → check → test

# CI versions (stricter, no auto-fix)
uv run poe ci:fmt   # Check formatting only
uv run poe ci:lint  # Lint without fixes
```

---

## Pre-commit Hooks

Pre-commit hooks run automatically before each `git commit` to enforce code quality.

### Setup (one-time)

```bash
uv run poe hooks
```

### What Runs on Commit

| Hook | Action |
|------|--------|
| `ruff --fix` | Lint and auto-fix issues |
| `ruff-format` | Auto-format code |
| `trailing-whitespace` | Remove trailing spaces |
| `end-of-file-fixer` | Ensure newline at EOF |
| `check-yaml` | Validate YAML files |
| `check-toml` | Validate TOML files |
| `check-added-large-files` | Prevent large file commits |

### Run Manually

```bash
uv run poe hooks:run    # Run on all files
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

1. **Format check** – `ruff format --check`
2. **Lint check** – `ruff check`
3. **Type check** – `ty check`
4. **Tests** – `pytest`

See [`.github/workflows/pr.yml`](.github/workflows/pr.yml)

---

## Publishing to PyPI

We use `uv publish` for publishing packages to PyPI:

```bash
# Build the package
uv build --package greeter

# Publish to PyPI
uv publish dist/greeter-*.whl dist/greeter-*.tar.gz

# Or publish to TestPyPI first
uv publish --index-url https://test.pypi.org/simple/ dist/greeter-*.whl
```

### Authentication

Configure PyPI credentials via environment variables:
```bash
export UV_PUBLISH_USERNAME=__token__
export UV_PUBLISH_PASSWORD=pypi-xxxxx
```

Or use a `.pypirc` file for token-based authentication.

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
mkdir -p libs/mylib/gpt_architecture/mylib
touch libs/mylib/gpt_architecture/mylib/__init__.py
touch libs/mylib/gpt_architecture/mylib/py.typed
touch libs/mylib/gpt_architecture/py.typed

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

[Add your license here]
