# Contributing

How to set up your environment and contribute changes.

!!! warning "Important"
    Before starting work on any new features or major changes, **please open an issue first to discuss your proposal and get approval.** We don't want you to waste time on work that might not align with the project's direction or get merged.

## Overview

This project is a monorepo with the MPM CLI tool:

- **CLI**: `apps/mpm-cli/`
- **Documentation**: `docs/`

## Setup

### Prerequisites

- Python 3.13+
- uv
- Git

### Install

```bash
git clone https://github.com/gruckion/modern_python_monorepo.git
cd modern_python_monorepo
uv sync --all-packages
```

## Develop the CLI

```bash
cd apps/mpm-cli

# Run the CLI directly
uv run mpm --help

# Or install globally for testing anywhere
uv tool install -e .
```

Now you can run `mpm` from anywhere on your system to test your changes.

### Testing Changes

Create a test project to verify your changes work:

```bash
# Create a temp directory
cd /tmp
mkdir mpm-test && cd mpm-test

# Run your local CLI
mpm my-test-project --monorepo --with-samples -y

# Verify the generated project works
cd my-test-project
uv sync --all-packages
uv run poe all
```

## Develop the Docs

```bash
# From repo root
uv sync --all-packages --group docs

# Start local docs server
uv run poe docs
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to preview documentation changes.

## Contribution Flow

1. Open an issue/discussion before starting major work
2. Fork the repository
3. Create a feature branch
4. Make changes following existing code style
5. Update docs as needed
6. Test and format

```bash
# Run all checks
uv run poe all

# Or run individually
uv run poe fmt      # Format code
uv run poe lint     # Lint code
uv run poe check    # Type check
uv run poe test     # Run tests
uv run poe cov      # Run tests with coverage
```

7. Commit and push

```bash
git add .
git commit -m "feat(cli): add new feature"
git push origin your-branch
```

8. Open a Pull Request and link any related issues

## Commit Conventions

Use [Conventional Commits](https://www.conventionalcommits.org/) with the appropriate scope:

| Prefix | Use Case |
|--------|----------|
| `feat(cli):` | New CLI feature |
| `fix(cli):` | CLI bug fix |
| `feat(docs):` | New documentation |
| `fix(docs):` | Documentation fix |
| `chore:` | Maintenance tasks |
| `refactor:` | Code refactoring |
| `test:` | Adding or updating tests |

Examples:

```bash
git commit -m "feat(cli): add --with-precommit flag"
git commit -m "fix(cli): handle spaces in project names"
git commit -m "docs: update project structure examples"
git commit -m "chore: update dependencies"
```

## Code Style

- **Line length**: 120 characters maximum
- **Formatting**: Handled automatically by Ruff
- **Imports**: Sorted automatically by Ruff (isort rules)
- **Type hints**: Required for all public functions
- **Docstrings**: Google style

```python
def generate_project(config: ProjectConfig, output_path: Path) -> None:
    """Generate a new project from configuration.

    Args:
        config: Project configuration options.
        output_path: Directory to create the project in.

    Raises:
        FileExistsError: If the output directory already exists.
    """
    ...
```

## Testing

Tests are located in `apps/mpm-cli/tests/`:

```bash
# Run all tests
uv run poe test

# Run with coverage
uv run poe cov

# Run specific test file
uv run pytest apps/mpm-cli/tests/test_cli.py -v

# Run specific test
uv run pytest apps/mpm-cli/tests/test_cli.py::test_create_monorepo -v
```

### Test Categories

- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test CLI commands with various flag combinations
- **E2E tests**: Test that generated projects actually work

## Help

- **Issues**: [GitHub Issues](https://github.com/gruckion/modern_python_monorepo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/gruckion/modern_python_monorepo/discussions)

See the full contributor guide in the repository: `.github/CONTRIBUTING.md`.
