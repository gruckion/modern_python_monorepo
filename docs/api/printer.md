# printer

The `printer` application demonstrates how to use workspace libraries in an application.

## Overview

This application:

- Imports the `greeter` library from the workspace
- Provides a simple `run()` function as the entry point
- Shows the pattern for apps depending on libs in a monorepo

## Installation

The printer app is part of the monorepo workspace. When developing locally:

```bash
uv sync --all-packages
```

To install as a standalone package (after publishing to PyPI):

```bash
pip install printer
```

!!! note "Bundled Dependencies"
    When built with Una, the printer wheel includes the greeter library code, making it self-contained for distribution.

## Usage

### As a Library

```python
from modern_python_monorepo import printer

# Run the printer
printer.run()
```

### As a CLI

```bash
# Run via uv in development
uv run printer

# Run directly after installation
printer
```

### Via Docker

```bash
# Build and run
docker compose build printer
docker compose up printer
```

## Dependencies

| Package | Type | Purpose |
|---------|------|---------|
| greeter | Workspace | Provides the greeting functionality |

## How It Works

The printer app is intentionally simple to demonstrate the workspace dependency pattern:

```python
from modern_python_monorepo import greeter

def run() -> None:
    """Run the printer application, displaying a greeting."""
    print(greeter.greet())
```

1. **Import**: The app imports `greeter` from the shared namespace
2. **Call**: It calls `greeter.greet()` to generate the ASCII art
3. **Output**: The result is printed to stdout

This pattern scales to more complex applications with multiple library dependencies.

## API Reference

::: modern_python_monorepo.printer
    options:
      show_root_heading: false
      show_source: true
      members:
        - run
