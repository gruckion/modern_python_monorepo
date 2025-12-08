# Contributing

Thank you for considering contributing to the Modern Python Monorepo! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/modern_python_monorepo.git
   cd modern_python_monorepo
   ```
3. **Set up the development environment**:
   ```bash
   uv sync --all-packages
   uv run poe hooks
   ```

## Development Workflow

### 1. Create a Branch

Create a branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

Write your code following the project conventions:

- Use type hints for all functions
- Write docstrings in Google style
- Add tests for new functionality
- Keep changes focused and atomic

### 3. Run Checks

Before committing, run all checks:

```bash
uv run poe all
```

This runs:

- **fmt**: Code formatting with Ruff
- **lint**: Linting with Ruff (auto-fixes issues)
- **check**: Type checking with ty
- **test**: Tests with pytest

### 4. Commit Changes

Commit with a descriptive message:

```bash
git add .
git commit -m "feat: add new greeting style option"
```

Git hooks will automatically run checks before the commit is accepted.

#### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Use Case |
|--------|----------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation changes |
| `style:` | Code style changes (formatting, etc.) |
| `refactor:` | Code refactoring |
| `test:` | Adding or updating tests |
| `chore:` | Maintenance tasks |

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style

### Python

- **Line length**: 120 characters maximum
- **Formatting**: Handled automatically by Ruff
- **Imports**: Sorted automatically by Ruff (isort rules)
- **Type hints**: Required for all public functions

### Docstrings

Use Google-style docstrings:

```python
def greet(message: str = "Hello!") -> str:
    """Generate a greeting message.

    Args:
        message: The message to display.

    Returns:
        A string containing the formatted greeting.

    Example:
        >>> greet("Hi")
        'Hi'
    """
    return message
```

### Testing

- Place tests in `tests/` directory within each package
- Name test files `test_*.py`
- Name test functions `test_*`
- Use pytest fixtures for shared setup
- Include doctest examples in docstrings when helpful

Example test:

```python
def test_greet_default_message():
    """Test greet with default message."""
    result = greet()
    assert "Hello" in result


def test_greet_custom_message():
    """Test greet with custom message."""
    result = greet("Custom")
    assert "Custom" in result
```

## Adding New Packages

### New Library

1. Create the directory structure:
   ```bash
   mkdir -p libs/mylib/modern_python_monorepo/mylib
   touch libs/mylib/modern_python_monorepo/mylib/__init__.py
   touch libs/mylib/modern_python_monorepo/mylib/py.typed
   ```

2. Create `libs/mylib/pyproject.toml`:
   ```toml
   [project]
   name = "mylib"
   version = "0.1.0"
   dependencies = []
   requires-python = ">=3.13"
   dynamic = ["una"]

   [build-system]
   requires = ["hatchling", "hatch-una"]
   build-backend = "hatchling.build"

   [tool.hatch.build.hooks.una-build]
   [tool.hatch.metadata.hooks.una-meta]
   ```

3. Sync the workspace:
   ```bash
   uv sync --all-packages
   ```

### New Application

Follow the same pattern under `apps/`, and add a `Dockerfile` if containerization is needed.

## Pull Request Guidelines

### Before Submitting

- [ ] All checks pass (`uv run poe all`)
- [ ] Tests cover new functionality
- [ ] Documentation is updated if needed
- [ ] Commit messages follow conventions

### PR Description

Include in your PR description:

- **What**: Brief description of changes
- **Why**: Motivation for the changes
- **How**: Technical approach (if complex)
- **Testing**: How to test the changes

### Review Process

1. CI checks must pass
2. At least one maintainer review required
3. Address review feedback
4. Squash and merge when approved

## Reporting Issues

When reporting issues, please include:

- Python version (`python --version`)
- uv version (`uv --version`)
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

## Questions?

Feel free to open an issue for questions or join discussions on GitHub.
