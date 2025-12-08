# Development Setup

This guide covers the complete development environment setup and workflow for the Modern Python Monorepo.

## Environment Overview

The development environment consists of:

| Component | Tool | Purpose |
|-----------|------|---------|
| Package Manager | uv | Dependency management and virtual environments |
| Task Runner | poethepoet (poe) | Unified command interface |
| Linter/Formatter | Ruff | Code quality and formatting |
| Type Checker | ty | Static type analysis |
| Test Framework | pytest | Testing with coverage |
| Git Hooks | prek | Pre-commit checks |

## Initial Setup

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Install

```bash
git clone https://github.com/gruckion/modern_python_monorepo.git
cd modern_python_monorepo
uv sync --all-packages
```

### 3. Set Up Git Hooks

Install git hooks to automatically run checks before commits:

```bash
uv tool install prek
uv run poe hooks
```

After this, every `git commit` will automatically run:

- Ruff linting with auto-fix
- Ruff formatting
- Trailing whitespace removal
- YAML/TOML validation
- Large file detection
- Merge conflict detection
- Private key leak detection

## Development Workflow

### Daily Workflow

```bash
uv run poe fmt
uv run poe lint
uv run poe check
uv run poe test
uv run poe all
git commit -m "Your message"
```

### Adding Dependencies

To add a dependency to a specific package:

```bash
cd libs/greeter
uv add some-package
```

```bash
cd apps/printer
uv add some-package
```

To add a workspace dependency (one internal package depending on another):

```bash
cd apps/printer
uv add greeter --editable
```

### Running Tests with Coverage

```bash
uv run poe cov
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## IDE Configuration

### VS Code

The repository includes VS Code settings in `.vscode/`. Recommended extensions:

- **Python** - Microsoft's Python extension
- **Ruff** - For integrated linting and formatting
- **Even Better TOML** - For pyproject.toml editing

Create or update `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": "explicit",
            "source.organizeImports.ruff": "explicit"
        }
    },
    "python.analysis.typeCheckingMode": "basic"
}
```

### PyCharm

1. Open the project root folder
2. Go to **Settings** > **Project** > **Python Interpreter**
3. Select **Add Interpreter** > **Add Local Interpreter**
4. Choose **Existing** and select `.venv/bin/python`
5. Enable **Ruff** plugin for linting

## Virtual Environment

uv creates and manages a virtual environment in `.venv/`:

```bash
source .venv/bin/activate
deactivate
which python
```

!!! tip "You rarely need to activate manually"
    Using `uv run <command>` automatically uses the correct virtual environment. Only activate manually when you need an interactive Python session.

## Sync Dependencies

When `pyproject.toml` or `uv.lock` changes (e.g., after git pull):

```bash
uv sync --all-packages
uv sync --all-packages --group docs
```

## Useful Commands

| Command | Description |
|---------|-------------|
| `uv sync --all-packages` | Install/update all dependencies |
| `uv run poe all` | Run all checks (fmt, lint, check, test) |
| `uv run python` | Start Python REPL with project packages |
| `uv tree` | Show dependency tree |
| `uv lock --upgrade` | Upgrade all dependencies |
