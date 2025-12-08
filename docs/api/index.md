# API Reference

This section contains auto-generated API documentation from the source code docstrings.

## Available Packages

The monorepo contains the following packages:

### Libraries

| Package | Description |
|---------|-------------|
| [greeter](greeter.md) | Greeting library using cowsay for ASCII art output |

### Applications

| Package | Description |
|---------|-------------|
| [printer](printer.md) | Application that demonstrates using the greeter library |

## Package Hierarchy

```
modern_python_monorepo/
├── greeter/          # Library: Generates greetings with cowsay
│   ├── greet()       # Generate greeting message
│   └── main()        # CLI entry point
└── printer/          # App: Uses greeter to display output
    └── run()         # Run the printer application
```

## Import Examples

```python
# Import the greeter library
from modern_python_monorepo import greeter

# Use the greet function
message = greeter.greet("Hello, World!")
print(message)

# Import and run the printer app
from modern_python_monorepo import printer
printer.run()
```

## CLI Commands

After installing the packages, these CLI commands are available:

| Command | Package | Description |
|---------|---------|-------------|
| `greeter` | greeter | Run the greeter library directly |
| `printer` | printer | Run the printer application |

## Type Hints

All packages include type hints and are marked as typed packages (PEP 561) with `py.typed` marker files. This enables:

- IDE autocompletion
- Static type checking with tools like mypy or ty
- Better documentation generation

## Documentation Generation

This API documentation is automatically generated using [mkdocstrings](https://mkdocstrings.github.io/) from the docstrings in the source code. The docstrings follow the [Google style guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
