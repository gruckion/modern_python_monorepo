# greeter

The `greeter` library provides greeting functionality using cowsay for ASCII art output.

## Overview

This library demonstrates:

- Simple function design with type hints
- Google-style docstrings for documentation
- Doctest examples for self-documenting code
- CLI entry point configuration

## Installation

The greeter library is part of the monorepo workspace. When developing locally:

```bash
uv sync --all-packages
```

To install as a standalone package (after publishing to PyPI):

```bash
pip install greeter
```

## Usage

### As a Library

```python
from modern_python_monorepo import greeter

# Generate a greeting with default message
result = greeter.greet()
print(result)

# Generate a greeting with custom message
result = greeter.greet("Custom message!")
print(result)
```

### As a CLI

```bash
uv run greeter
greeter
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| cowsay-python | 1.0.2 | ASCII art cow generation |

## API Reference

::: modern_python_monorepo.greeter
    options:
      show_root_heading: false
      show_source: true
      members:
        - greet
        - main
