# Getting Started

This guide will help you get the Modern Python Monorepo up and running on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.13+** - The monorepo requires Python 3.13 or later
- **Git** - For cloning the repository

## Installation

### Step 1: Install uv

[uv](https://docs.astral.sh/uv/) is the package manager used by this project. Install it with:

=== "macOS/Linux"

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Windows"

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

=== "pip"

    ```bash
    pip install uv
    ```

### Step 2: Clone the Repository

```bash
git clone https://github.com/gruckion/modern_python_monorepo.git
cd modern_python_monorepo
```

### Step 3: Install Dependencies

Install all workspace packages and development dependencies:

```bash
uv sync --all-packages
```

This command:

- Creates a virtual environment in `.venv/`
- Installs all workspace packages (`apps/*` and `libs/*`)
- Installs development dependencies (ruff, ty, pytest, etc.)

### Step 4: Verify Installation

Run all checks to verify everything is working:

```bash
uv run poe all
```

This runs formatting, linting, type checking, and tests in sequence.

## Project Structure

After cloning, you'll see this structure:

```text
modern_python_monorepo/
├── pyproject.toml       # Workspace root configuration
├── uv.lock              # Locked dependencies
├── apps/                # Runnable applications
│   └── printer/         # Example app that uses greeter lib
└── libs/                # Reusable libraries
    └── greeter/         # Example library with cowsay
```

## Running the Example Application

The monorepo includes an example `printer` application that uses the `greeter` library:

```bash
uv run printer
uv run greeter
```

Both commands display an ASCII cow with a greeting message.

## Next Steps

Now that you have the project running:

1. **[Development Setup](development/setup.md)** - Learn about the development workflow
2. **[Commands Reference](development/commands.md)** - See all available poe tasks
3. **[Architecture Overview](architecture/overview.md)** - Understand how the monorepo is structured
4. **[Docker Guide](development/docker.md)** - Build and run containers

## Troubleshooting

### Python Version Mismatch

If you see an error about Python version, ensure you have Python 3.13+ installed:

```bash
python --version
```

You can install it via uv:

```bash
uv python install 3.13
```

### Lockfile Out of Date

If you see lockfile errors, regenerate it:

```bash
uv lock
uv sync --all-packages
```

### Permission Errors

If you encounter permission errors during installation, ensure you have write access to the directory and try running without sudo (uv manages its own virtual environment).
