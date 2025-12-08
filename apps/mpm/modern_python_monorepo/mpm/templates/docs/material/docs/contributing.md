# Contributing

Thank you for your interest in contributing!

## Development Setup

1. Fork the repository
2. Clone your fork
3. Install dependencies: `uv sync --all-packages`
4. Install git hooks: `uv run poe hooks`

## Making Changes

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Run checks: `uv run poe all`
4. Commit with a descriptive message
5. Push and create a pull request

## Code Style

- Follow PEP 8 (enforced by Ruff)
- Add type hints to all functions
- Write docstrings for public APIs
- Include tests for new features

## Pull Request Guidelines

- Keep PRs focused on a single change
- Include tests for new functionality
- Update documentation as needed
- Ensure all checks pass
