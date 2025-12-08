# MPM CLI - Modern Python Monorepo CLI Tool

## Table of Contents

- [Overview](#overview)
- [CLI Name Conflict Analysis](#cli-name-conflict-analysis)
- [Research: Existing CLI Tools](#research-existing-cli-tools)
  - [Better T Stack CLI](#better-t-stack-cli)
  - [TanStack Start CLI](#tanstack-start-cli)
  - [Feature Comparison](#feature-comparison)
- [Python CLI Framework Evaluation](#python-cli-framework-evaluation)
  - [Typer](#1-typer-recommended)
  - [Click](#2-click)
  - [Questionary](#3-questionary)
  - [Recommendation](#framework-recommendation)
- [MPM CLI Specification](#mpm-cli-specification)
  - [Core Requirements](#core-requirements)
  - [Interactive Prompts Design](#interactive-prompts-design)
  - [Add Package Command](#add-package-command)
  - [CLI Flags](#cli-flag-support)
  - [Subcommands](#subcommands)
  - [Generated Project Structure](#project-structure-to-generate)
  - [Implementation Architecture](#implementation-architecture)
  - [Help Menu Design](#help-menu-design)
- [Technology Stack](#technology-stack-for-mpm-cli)

---

## Overview

The **Modern Python Monorepo (MPM) CLI** is a scaffolding tool for creating production-ready Python monorepo projects. Inspired by tools like `create-better-t-stack` and `@tanstack/create-start`, it provides both interactive prompts and CLI flags for flexible project generation.

### Usage

```bash
# Primary usage via uvx
uvx mpm@latest

# Alternative via pipx
pipx run mpm

# With project name
mpm my-project

# Non-interactive with flags
mpm my-project --monorepo --with-docker --with-ci -y

# Add packages to existing project
mpm add lib auth
mpm add app api --docker
```

---

## CLI Name Conflict Analysis

### Command Name: `mpm`

The CLI tool will be named `mpm` (Modern Python Monorepo). Research was conducted to identify potential conflicts with existing tools.

### Known Conflicts

| Tool | Domain | Likelihood of Conflict | Notes |
|------|--------|------------------------|-------|
| **Meta Package Manager** | Package management | **Medium** | Python package on PyPI (`meta-package-manager`), installs as `mpm`. Wraps multiple package managers (brew, apt, pip, npm, etc.). Available via Homebrew and AUR. |
| **MATLAB Package Manager** | MATLAB installation | **Low** | Used for MATLAB/Simulink installation. Typically invoked as `matlab -mpm` or from MATLAB install directory. Not commonly in PATH for Python developers. |
| **MiKTeX mpm** | LaTeX packages | **Low-Medium** | LaTeX package manager. Being deprecated in favor of `miktex` command. Only affects LaTeX users. |
| **Apache mpm** | Web server | **Very Low** | Apache Multi-Processing Modules. Not a CLI command, but a configuration directive. |

### Conflict Details

#### Meta Package Manager (Primary Concern)

**Source:** [GitHub](https://github.com/kdeldycke/meta-package-manager) | [PyPI](https://pypi.org/project/meta-package-manager/)

- **Installation:** `pip install meta-package-manager` or `brew install meta-package-manager`
- **Command:** `mpm`
- **Purpose:** Unified CLI wrapper for 30+ package managers (apt, brew, pip, npm, cargo, etc.)
- **Usage:** `mpm installed`, `mpm outdated`, `mpm upgrade`

**Risk Assessment:** Developers who have installed Meta Package Manager will have a conflict. However:

- It's a niche tool (not mainstream like npm or pip)
- Our tool installs via `uvx mpm` which uses isolated environments
- Users can use the full package name: `uvx modern-python-monorepo`

#### MATLAB Package Manager

**Source:** [MathWorks Documentation](https://www.mathworks.com/help/install/ug/mpminstall.html)

- **Installation:** Downloaded from MathWorks, typically in MATLAB install directory
- **Command:** `mpm install`, `mpm download`
- **Purpose:** Install MATLAB products from command line

**Risk Assessment:** Low risk. MATLAB developers typically:

- Run mpm from MATLAB installation directory
- Use `matlab -mpm` syntax
- Don't have MATLAB's mpm in global PATH

#### MiKTeX mpm

**Source:** [MiKTeX GitHub](https://github.com/MiKTeX/miktex)

- **Installation:** Part of MiKTeX LaTeX distribution
- **Command:** `mpm --update`, `mpm --install`
- **Purpose:** Manage LaTeX packages

**Risk Assessment:** Low-Medium risk. Being deprecated in favor of `miktex` command. Only affects LaTeX users, and MiKTeX is primarily Windows-focused.

### Mitigation Strategies

1. **Primary command:** `mpm` (short, memorable)
2. **Alternative invocation:** `uvx modern-python-monorepo` (no conflict possible)
3. **Package name on PyPI:** `modern-python-monorepo` (unique, descriptive)
4. **Documentation:** Clearly document potential conflicts and alternatives
5. **Isolated execution:** When run via `uvx mpm`, it uses an isolated environment

### Recommendation

**Proceed with `mpm` as the command name** because:

1. The primary conflict (Meta Package Manager) is a niche tool
2. `uvx` provides isolation, reducing conflict risk
3. The full package name (`modern-python-monorepo`) is always available
4. `mpm` is short, memorable, and matches our branding (Modern Python Monorepo)
5. MATLAB and MiKTeX conflicts are unlikely for Python developers

### Alternative Names Considered

| Name | Pros | Cons |
|------|------|------|
| `mpm` | Short, matches branding | Some conflicts exist |
| `pyrepo` | Python-specific | Generic, forgettable |
| `monopy` | Descriptive | Awkward to type |
| `uvm` | Short | Conflicts with Node version manager (nvm pattern) |
| `create-mpm` | npm-style convention | Longer, but clear intent |

**Final Decision:** Use `mpm` as primary command, with `modern-python-monorepo` as the PyPI package name for disambiguation.

---

## Research: Existing CLI Tools

### Better T Stack CLI

**Sources:**

- [GitHub Repository](https://github.com/AmanVarshney01/create-better-t-stack)
- [Official Website](https://www.better-t-stack.dev/)

#### What It Is

A modern CLI for scaffolding end-to-end type-safe TypeScript projects with best practices and customizable configurations.

#### Installation

```bash
# Using bun (recommended)
bun create better-t-stack@latest

# Using pnpm
pnpm create better-t-stack@latest

# Using npm
npx create-better-t-stack@latest
```

#### Key Features

| Feature | Description |
|---------|-------------|
| **Interactive Wizard** | Step-by-step prompts for stack selection |
| **Visual Stack Builder** | Web UI at `/new` to generate commands |
| **Modular Selection** | Pick only what you need, nothing extra |
| **Latest Dependencies** | Always uses current stable versions |
| **Free & Open Source** | MIT licensed, forever free |

#### Configuration Options

| Category | Available Choices |
|----------|-------------------|
| **Frontend** | React (TanStack Router/React Router/TanStack Start), Next.js, Nuxt, Svelte, Solid, React Native (NativeWind/Unistyles), or none |
| **Backend** | Hono, Express, Fastify, Elysia, Next API Routes, Convex, or none |
| **API Layer** | tRPC, oRPC, or none |
| **Runtime** | Bun, Node.js, Cloudflare Workers |
| **Database** | SQLite, PostgreSQL, MySQL, MongoDB, or none |
| **ORM** | Drizzle, Prisma, Mongoose, or none |
| **Authentication** | Better-Auth (optional) |
| **Addons** | Turborepo, PWA, Tauri, Biome, Husky, Starlight, Fumadocs, Oxlint |
| **DB Hosting** | Turso, Neon, Supabase, Prisma PostgreSQL, MongoDB Atlas, Cloudflare D1, Docker |
| **Example Templates** | Todo, AI |

#### How It Works

1. User runs the create command
2. Interactive wizard presents category-by-category choices
3. User selects options via arrow keys and space bar
4. CLI generates project with selected stack
5. Outputs next steps for the user

---

### TanStack Start CLI

**Sources:**

- [Quick Start Documentation](https://tanstack.com/start/latest/docs/framework/react/quick-start)
- [GitHub README](https://github.com/TanStack/create-tsrouter-app/blob/main/cli/create-start-app/README.md)
- [npm Package](https://www.npmjs.com/package/@tanstack/create-start)

#### What It Is

Official scaffolding tool for TanStack Start applications. Described as "everything you loved about CRA but implemented with modern tools and best practices."

#### Installation

```bash
npm create @tanstack/start@latest
pnpm create @tanstack/start@latest
bun create @tanstack/start@latest
```

#### CLI Flags

| Flag | Description |
|------|-------------|
| `--package-manager` | Choose: npm, yarn, pnpm, bun, or deno |
| `--toolchain` | `biome` or `eslint` (configures linting/formatting) |
| `--tailwind` | Auto-configure Tailwind CSS V4 |
| `--add-ons` | Comma-separated list (e.g., `shadcn,tanstack-query`) |
| `--list-add-ons` | Display all available add-ons |
| `--framework` | Specify framework (react, solid) |
| `--template` | `typescript` or `javascript` for routing style |
| `--no-git` | Skip git repository initialization |
| `--mcp` | Enable MCP support for AI-enabled IDEs |

#### Interactive Mode Prompts

When run without flags, the CLI prompts for:

- Project name
- Package manager selection
- Toolchain preference (Biome vs ESLint)
- Git repository initialization
- Add-ons selection

#### Example Templates

- Basic
- Basic + Auth / React Query / Clerk / Supabase
- Trellaux (with/without Convex)
- Material UI integration
- Auth.js Integration
- Static rendering variants
- Cloudflare/Netlify deployment variants

#### How It Works

1. User runs create command with optional flags
2. CLI displays which options were provided via flags
3. Prompts only for remaining choices
4. Generates Vite + TanStack Router application
5. Creates README with integration documentation

---

### Feature Comparison

| Feature | Better T Stack | TanStack Start |
|---------|----------------|----------------|
| **Interactive Wizard** | Yes - Full | Yes - Full |
| **CLI Flags** | Yes | Yes - Extensive |
| **Web-based Builder** | Yes - Stack Builder UI | No |
| **Multi-framework Support** | Yes - 7+ frameworks | Yes - React/Solid |
| **Backend Options** | Yes - 6+ backends | No (frontend-focused) |
| **Database Setup** | Yes - 5+ DBs + ORMs | No |
| **Monorepo Support** | Yes - Turborepo addon | No |
| **Docker Configuration** | Yes | No |
| **Authentication Setup** | Yes - Better-Auth | Yes - Via add-ons |
| **CI/CD Generation** | Yes - GitHub Actions | No |
| **MCP/AI IDE Support** | No | Yes |
| **Add-ons System** | Yes - Multiple | Yes - Extensible |

---

## Python CLI Framework Evaluation

**Sources:**

- [Typer Documentation](https://typer.tiangolo.com/)
- [Typer Alternatives Comparison](https://typer.tiangolo.com/alternatives/)
- [Questionary GitHub](https://github.com/tmbo/questionary)
- [Click vs Argparse Analysis](https://www.pythonsnacks.com/p/click-vs-argparse-python)
- [Python CLI Comparison](https://codecut.ai/comparing-python-command-line-interface-tools-argparse-click-and-typer/)

### 1. Typer (Recommended)

**What:** Modern CLI framework built on Click, leveraging Python type hints for a clean API.

#### Features

| Feature | Support |
|---------|---------|
| **Type Hints** | Native - drives the entire API |
| **Auto Help Generation** | Automatic from function signatures |
| **Shell Auto-Completion** | Bash, Zsh, Fish, PowerShell |
| **Commands/Subcommands** | Full hierarchy support |
| **Rich Integration** | Beautiful error formatting |
| **Testing Support** | Built-in test utilities |
| **Basic Prompts** | `typer.prompt()`, `typer.confirm()` |
| **Progress Bars** | Yes |
| **Password Input** | Yes, with confirmation |
| **Multi-select/Checkbox** | No (requires questionary) |

#### Example

```python
import typer

app = typer.Typer()

@app.command()
def create(
    name: str = typer.Argument(..., help="Project name"),
    monorepo: bool = typer.Option(False, "--monorepo", "-m", help="Create monorepo structure"),
    python_version: str = typer.Option("3.13", "--python", "-p", help="Python version"),
):
    """Create a new Modern Python Monorepo project."""
    typer.echo(f"Creating project: {name}")

if __name__ == "__main__":
    app()
```

#### Pros

- Minimal boilerplate via type annotations
- IDE autocompletion throughout codebase
- Built on battle-tested Click
- Described as "FastAPI of CLIs"
- Excellent documentation

#### Cons

- No native checkbox/multi-select prompts
- Requires external library for complex interactive UI

---

### 2. Click

**What:** The foundation Typer builds upon - mature, powerful, decorator-based CLI framework.

#### Features

| Feature | Support |
|---------|---------|
| **Commands** | Full hierarchy with groups |
| **Options/Arguments** | Comprehensive type system |
| **Help Generation** | Automatic |
| **File Types** | Paths, enums, choices, etc. |
| **Testing** | CliRunner for testing |
| **Context Passing** | Full context management |

#### Example

```python
import click

@click.command()
@click.argument('name')
@click.option('--monorepo', '-m', is_flag=True, help='Create monorepo structure')
@click.option('--python', '-p', default='3.13', help='Python version')
def create(name, monorepo, python):
    """Create a new Modern Python Monorepo project."""
    click.echo(f"Creating project: {name}")

if __name__ == "__main__":
    create()
```

#### Pros

- Mature, stable, widely adopted
- Powerful for complex CLI applications
- Excellent documentation
- Large ecosystem

#### Cons

- Verbose decorator syntax
- Code repetition (decorator names + parameter names)
- Originally designed with Python 2.x constraints
- Less IDE support due to decorator-based approach

---

### 3. Questionary

**What:** Interactive prompt library for building beautiful command-line interfaces with user input.

#### Available Prompt Types

| Prompt Type | Description | Example |
|-------------|-------------|---------|
| `text` | Basic text input | Project name |
| `password` | Secure password entry | API keys |
| `path` | File system path selection | Config file location |
| `confirm` | Yes/no prompts | "Include Docker?" |
| `select` | Single-choice selection | License type |
| `rawselect` | Numbered selection UI | Quick selection |
| `checkbox` | **Multi-select with checkboxes** | Features to include |
| `autocomplete` | Text input with suggestions | Package names |

#### Example

```python
import questionary

# Single select
structure = questionary.select(
    "Project structure:",
    choices=["Monorepo (libs/ and apps/)", "Single package"]
).ask()

# Multi-select checkbox
features = questionary.checkbox(
    "Select features to include:",
    choices=[
        questionary.Choice("Ruff (linting & formatting)", checked=True),
        questionary.Choice("ty (type checking)", checked=True),
        questionary.Choice("pytest (testing)", checked=True),
        questionary.Choice("GitHub Actions CI", checked=False),
        questionary.Choice("Docker support", checked=False),
    ]
).ask()

# Confirmation
include_samples = questionary.confirm(
    "Include sample packages?",
    default=True
).ask()
```

#### Pros

- Beautiful, intuitive prompts
- All interactive types needed for scaffolding tools
- Works seamlessly with Typer/Click
- Used by 18,000+ projects (including Rasa)
- MIT licensed

#### Cons

- Prompt-only library (not a full CLI framework)
- Must combine with Typer/Click for command structure

---

### Framework Recommendation

**Use Typer + Questionary together:**

| Responsibility | Tool |
|----------------|------|
| CLI structure, commands, flags | Typer |
| Interactive prompts, checkboxes | Questionary |
| Terminal styling, progress | Rich (bundled with Typer) |

This combination provides:

- Clean CLI definition via type hints
- Beautiful interactive prompts including checkboxes
- Rich terminal output with colors and formatting
- Auto-generated help documentation
- Shell completion for all major shells

---

## MPM CLI Specification

### Core Requirements

#### R1: Project Initialization

- Create a new named project directory
- Initialize git repository (optional)
- Generate `pyproject.toml` with workspace configuration
- Create `uv.lock` file
- Set up `.gitignore` with Python defaults
- Generate `README.md` with usage instructions

#### R2: Monorepo vs Single Package Mode

| Mode | Structure | Use Case |
|------|-----------|----------|
| **Monorepo** | `libs/` and `apps/` directories with workspace config | Multiple interdependent packages |
| **Single Package** | Flat `src/` structure | Simple projects, single distribution |

#### R3: Package Generation

- Generate new `libs/<name>` library packages
- Generate new `apps/<name>` application packages
- Proper namespace packaging (e.g., `my_project.greeter`)
- Include `py.typed` marker for type hint support
- Generate package-specific `pyproject.toml`

#### R4: Docker Support

- Optional Dockerfile generation for apps
- Multi-stage build template (builder + runtime)
- `docker-compose.yml` for local development
- `docker-bake.hcl` for multi-platform builds (amd64 + arm64)
- Health check configuration
- Non-root user execution

#### R5: CI/CD Pipelines

- GitHub Actions workflow for PR checks (lint, type-check, test)
- Optional PyPI publishing workflow with trusted publisher (OIDC)
- Support for TestPyPI pre-releases
- Tag-based release triggers

#### R6: Tooling Configuration

| Tool | Purpose | Configuration |
|------|---------|---------------|
| **Ruff** | Linting & formatting | `[tool.ruff]` in pyproject.toml |
| **ty** | Type checking | `[tool.ty]` in pyproject.toml |
| **pytest** | Testing with coverage | `[tool.pytest]` in pyproject.toml |
| **poethepoet** | Task runner | `[tool.poe.tasks]` in pyproject.toml |
| **pre-commit** | Git hooks | `.pre-commit-config.yaml` |

#### R7: Sample Code

- Optional sample `greeter` library with cowsay integration
- Optional sample `printer` application demonstrating library dependency
- Demonstrates proper import patterns and testing

---

### Interactive Prompts Design

```
$ mpm

? Project name: my-awesome-project

? Project structure:
  > Monorepo (libs/ and apps/ workspaces)
    Single package

? Python version requirement:
    3.11+
    3.12+
  > 3.13+

? Select features to include: (space to toggle, enter to confirm)
  [x] Ruff (linting & formatting)
  [x] ty (type checking)
  [x] pytest (testing)
  [x] poethepoet (task runner)
  [x] Pre-commit hooks
  [ ] GitHub Actions CI
  [ ] PyPI publishing workflow
  [ ] Docker support

? Include sample packages?
  > Yes (greeter lib + printer app)
    No (empty structure)

? License:
  > MIT
    Apache-2.0
    GPL-3.0
    None

Creating project...
 Created my-awesome-project/
 Initialized git repository
 Generated pyproject.toml
 Set up tooling configuration
 Created sample packages

Next steps:
  cd my-awesome-project
  uv sync --all-packages
  poe check
```

---

### Add Package Command

```
$ cd my-awesome-project
$ mpm add

? Package type:
  > Library (libs/)
    Application (apps/)

? Package name: auth

? Description: Authentication utilities

# If Application selected:
? Include Docker support?
  > Yes
    No

Creating package...
 Created libs/auth/
 Generated pyproject.toml
 Created namespace structure
 Added to workspace

Run 'uv sync --all-packages' to update dependencies
```

---

### CLI Flag Support

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--name` | | Project name (skip prompt) | Interactive |
| `--monorepo` | `-m` | Create monorepo structure | Interactive |
| `--single` | `-s` | Create single package structure | Interactive |
| `--python` | `-p` | Python version (3.11, 3.12, 3.13) | 3.13 |
| `--with-samples` | | Include sample packages | Interactive |
| `--with-docker` | | Include Docker configuration | False |
| `--with-ci` | | Include GitHub Actions CI | False |
| `--with-pypi` | | Include PyPI publishing workflow | False |
| `--license` | `-l` | License type (MIT, Apache-2.0, GPL-3.0, none) | MIT |
| `--no-git` | | Skip git initialization | False |
| `--yes` | `-y` | Accept all defaults (non-interactive) | False |
| `--version` | `-v` | Show version and exit | |
| `--help` | | Show help message and exit | |

---

### Subcommands

| Command | Description |
|---------|-------------|
| `mpm [NAME]` | Create new project (default command) |
| `mpm add` | Add package to existing project (interactive) |
| `mpm add lib <name>` | Add library package |
| `mpm add app <name>` | Add application package |
| `mpm add app <name> --docker` | Add application with Docker support |

---

### Project Structure to Generate

#### Monorepo Mode (Full Features)

```
my-project/
├── pyproject.toml              # Workspace root configuration
├── uv.lock                     # Locked dependencies
├── LICENSE                     # MIT/Apache/GPL license file
├── README.md                   # Project documentation
├── .gitignore                  # Python gitignore
├── .python-version             # Python version file
│
├── .pre-commit-config.yaml     # [if pre-commit selected]
│
├── .github/                    # [if CI selected]
│   └── workflows/
│       ├── pr.yml              # PR checks workflow
│       └── release.yml         # [if PyPI selected] Publishing workflow
│
├── docker-compose.yml          # [if Docker selected]
├── docker-bake.hcl             # [if Docker selected]
│
├── libs/                       # Library packages
│   └── greeter/                # [if samples selected]
│       ├── pyproject.toml
│       └── my_project/
│           └── greeter/
│               ├── __init__.py
│               └── py.typed
│
└── apps/                       # Application packages
    └── printer/                # [if samples selected]
        ├── pyproject.toml
        ├── Dockerfile          # [if Docker selected]
        └── my_project/
            └── printer/
                ├── __init__.py
                └── py.typed
```

#### Single Package Mode

```
my-project/
├── pyproject.toml
├── uv.lock
├── LICENSE
├── README.md
├── .gitignore
├── .python-version
├── .pre-commit-config.yaml     # [if selected]
├── .github/workflows/          # [if selected]
├── Dockerfile                  # [if selected]
└── src/
    └── my_project/
        ├── __init__.py
        └── py.typed
```

---

### Implementation Architecture

```
mpm/                            # CLI tool package (lives in this repo)
├── pyproject.toml              # Package configuration
├── README.md                   # CLI documentation
└── src/
    └── mpm/
        ├── __init__.py         # Package exports, version
        ├── cli.py              # Typer application entry point
        ├── prompts.py          # Questionary prompt definitions
        ├── config.py           # Pydantic configuration models
        ├── utils.py            # Helper utilities
        │
        ├── generators/         # Code generation modules
        │   ├── __init__.py
        │   ├── project.py      # Project scaffold generator
        │   ├── package.py      # Package scaffold generator
        │   ├── docker.py       # Docker file generator
        │   ├── ci.py           # GitHub Actions generator
        │   └── tooling.py      # Ruff, pytest, etc. configs
        │
        └── templates/          # Jinja2 templates
            ├── pyproject.toml.j2
            ├── README.md.j2
            ├── gitignore.j2
            ├── Dockerfile.j2
            ├── docker-compose.yml.j2
            ├── docker-bake.hcl.j2
            ├── pre-commit-config.yaml.j2
            ├── pr.yml.j2
            ├── release.yml.j2
            ├── lib_init.py.j2
            └── app_init.py.j2
```

---

### Help Menu Design

```
$ mpm --help

 Usage: mpm [OPTIONS] [PROJECT_NAME] COMMAND [ARGS]...

 Modern Python Monorepo CLI - Scaffold production-ready Python projects

 Create new monorepo or single-package Python projects with best practices:
 - uv for fast dependency management
 - Ruff for linting and formatting
 - ty for type checking
 - pytest for testing
 - Optional Docker, CI/CD, and PyPI publishing

╭─ Arguments ─────────────────────────────────────────────────────────────────╮
│   project_name      [PROJECT_NAME]  Project name [default: None]            │
╰─────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────╮
│ --monorepo        -m              Create monorepo structure (libs/ + apps/) │
│ --single          -s              Create single package structure           │
│ --python          -p  TEXT        Python version requirement [default: 3.13]│
│ --with-samples                    Include sample greeter lib and printer app│
│ --with-docker                     Include Docker configuration              │
│ --with-ci                         Include GitHub Actions CI workflow        │
│ --with-pypi                       Include PyPI publishing workflow          │
│ --license         -l  TEXT        License: MIT, Apache-2.0, GPL-3.0, none   │
│                                   [default: MIT]                            │
│ --no-git                          Skip git repository initialization        │
│ --yes             -y              Accept defaults (non-interactive mode)    │
│ --version         -v              Show version and exit                     │
│ --help                            Show this message and exit                │
╰─────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────╮
│ add         Add a new package to an existing project                        │
╰─────────────────────────────────────────────────────────────────────────────╯

 Examples:

   # Interactive mode - prompts for all options
   mpm

   # Create project with name
   mpm my-project

   # Create monorepo with all defaults
   mpm my-project --monorepo --yes

   # Full-featured project
   mpm my-project -m --with-samples --with-docker --with-ci --with-pypi

   # Add a library to existing project
   mpm add lib auth

   # Add an app with Docker support
   mpm add app api --docker

 Documentation: https://github.com/gruckion/modern_python_monorepo
```

#### Add Subcommand Help

```
$ mpm add --help

 Usage: mpm add [OPTIONS] COMMAND [ARGS]...

 Add a new package to an existing Modern Python Monorepo project.

 Must be run from within a project directory containing a pyproject.toml
 with workspace configuration.

╭─ Commands ──────────────────────────────────────────────────────────────────╮
│ lib         Add a new library package to libs/                              │
│ app         Add a new application package to apps/                          │
╰─────────────────────────────────────────────────────────────────────────────╯

 Examples:

   # Interactive mode
   mpm add

   # Add library
   mpm add lib auth
   mpm add lib utils --description "Shared utilities"

   # Add application
   mpm add app api
   mpm add app worker --docker
```

---

## Technology Stack for MPM CLI

| Component | Package | Version | Purpose |
|-----------|---------|---------|---------|
| **CLI Framework** | `typer` | ^0.12 | Command structure, flags, help generation |
| **Interactive Prompts** | `questionary` | ^2.1 | Checkbox, select, confirm prompts |
| **Terminal Styling** | `rich` | ^13.0 | Colors, panels, progress indicators |
| **Templating** | `jinja2` | ^3.1 | File content generation |
| **Validation** | `pydantic` | ^2.0 | Configuration validation |
| **Python Version** | | >=3.11 | Minimum supported version |

### Dependencies (pyproject.toml)

```toml
[project]
name = "modern-python-monorepo"
version = "0.1.0"
description = "Modern Python Monorepo CLI - Scaffold production-ready Python projects"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.12.0",
    "questionary>=2.1.0",
    "rich>=13.0.0",
    "jinja2>=3.1.0",
    "pydantic>=2.0.0",
]

[project.scripts]
mpm = "mpm.cli:app"
```

**Note:** The PyPI package name is `modern-python-monorepo` (unique, no conflicts), but the CLI command is `mpm` (short, memorable).

---

## Template Bundling Architecture

### Approach: Package Data with `importlib.resources`

**Decision:** Bundle templates inside the Python package and access via `importlib.resources.files()`.

**Rationale:**

- **Atomic versioning:** CLI and templates always match versions
- **Offline-first:** Works without internet connection
- **Simple:** No Git clone complexity
- **Fast:** Templates are local, no network latency
- **Proven:** Used internally by Cookiecutter, Copier

**Sources:**

- [Python Docs - importlib.resources](https://docs.python.org/3/library/importlib.resources.html)
- [Scientific Python Guide - Data Files](https://learn.scientific-python.org/development/patterns/data-files/)
- [importlib-resources Documentation](https://importlib-resources.readthedocs.io/en/latest/using.html)

### Template Directory Structure

```
src/mpm/
├── __init__.py
├── cli.py                        # Typer app entry point
├── prompts.py                    # Questionary interactive prompts
├── config.py                     # Pydantic configuration models
├── utils.py                      # Helper utilities
│
├── generators/                   # Code generation modules
│   ├── __init__.py
│   ├── project.py                # Main project generator
│   ├── package.py                # lib/app package generator
│   ├── renderer.py               # Jinja2 template renderer
│   ├── docker.py                 # Docker file generator
│   ├── ci.py                     # GitHub Actions generator
│   └── docs.py                   # MkDocs generator
│
└── templates/                    # Bundled templates (package data)
    ├── __init__.py               # Required: makes it a package
    │
    ├── base/                     # Always included in every project
    │   ├── pyproject.toml.jinja
    │   ├── README.md.jinja
    │   ├── LICENSE.jinja
    │   ├── .gitignore
    │   ├── .python-version.jinja
    │   └── main.py
    │
    ├── monorepo/                 # Monorepo-specific structure
    │   ├── libs/
    │   │   └── __package__/      # Placeholder for package_name
    │   │       ├── pyproject.toml.jinja
    │   │       ├── tests/
    │   │       │   └── test_import.py.jinja
    │   │       └── __namespace__/
    │   │           └── __package__/
    │   │               ├── __init__.py.jinja
    │   │               └── py.typed
    │   └── apps/
    │       └── __package__/
    │           ├── pyproject.toml.jinja
    │           ├── Dockerfile.jinja
    │           ├── tests/
    │           │   └── test_import.py.jinja
    │           └── __namespace__/
    │               └── __package__/
    │                   ├── __init__.py.jinja
    │                   └── py.typed
    │
    ├── single/                   # Single package mode structure
    │   └── src/
    │       └── __namespace__/
    │           ├── __init__.py.jinja
    │           └── py.typed
    │
    ├── tooling/                  # Optional dev tooling configs
    │   └── .pre-commit-config.yaml
    │
    ├── docker/                   # Optional Docker support
    │   ├── Dockerfile.jinja
    │   ├── docker-compose.yml.jinja
    │   ├── docker-bake.hcl.jinja
    │   └── .dockerignore
    │
    ├── ci/                       # Optional CI/CD workflows
    │   └── .github/
    │       └── workflows/
    │           ├── pr.yml.jinja
    │           └── release.yml.jinja
    │
    ├── docs/                     # Optional MkDocs documentation
    │   ├── material/             # Material theme templates
    │   │   ├── mkdocs.yml.jinja
    │   │   ├── index.md.jinja
    │   │   ├── getting-started.md.jinja
    │   │   ├── contributing.md
    │   │   ├── api/
    │   │   │   └── index.md.jinja
    │   │   ├── development/
    │   │   │   ├── setup.md.jinja
    │   │   │   ├── commands.md
    │   │   │   └── docker.md
    │   │   └── architecture/
    │   │       └── overview.md
    │   └── shadcn/               # shadcn theme templates
    │       ├── mkdocs.yml.jinja
    │       └── ... (same structure as material)
    │
    └── samples/                  # Optional sample packages
        ├── greeter/              # Sample library
        │   ├── pyproject.toml.jinja
        │   └── __namespace__/
        │       └── greeter/
        │           └── __init__.py.jinja
        └── printer/              # Sample app (depends on greeter)
            ├── pyproject.toml.jinja
            ├── Dockerfile.jinja
            └── __namespace__/
                └── printer/
                    └── __init__.py.jinja
```

### Template Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `project_name` | `my_awesome_project` | Python identifier (underscores) |
| `project_slug` | `my-awesome-project` | URL/PyPI slug (hyphens) |
| `project_description` | `A cool project` | Short description |
| `namespace` | `my_awesome_project` | Python import namespace |
| `python_version` | `3.13` | Minimum Python version |
| `author_name` | `John Doe` | Author full name |
| `author_email` | `john@example.com` | Author email |
| `github_owner` | `johndoe` | GitHub username/org |
| `github_repo` | `my-awesome-project` | GitHub repository name |
| `license_type` | `MIT` | License identifier |
| `package_name` | `greeter` | Individual package name |
| `package_description` | `Greeting utilities` | Package description |

### pyproject.toml Configuration

```toml
[tool.setuptools.package-data]
mpm = ["templates/**/*"]

[tool.setuptools.packages.find]
where = ["src"]

# Alternative with hatch:
[tool.hatch.build.targets.wheel]
packages = ["src/mpm"]

[tool.hatch.build.targets.wheel.force-include]
"src/mpm/templates" = "mpm/templates"
```

### Template Rendering Implementation

```python
from importlib.resources import files, as_file
from jinja2 import Environment, BaseLoader
from pathlib import Path
import shutil

class PackageTemplateLoader(BaseLoader):
    """Load templates from package resources."""

    def __init__(self, package: str = "mpm.templates"):
        self.package = package

    def get_source(self, environment, template):
        try:
            source = files(self.package).joinpath(template).read_text()
            return source, template, lambda: True
        except FileNotFoundError:
            raise TemplateNotFound(template)

class TemplateRenderer:
    """Render Jinja2 templates from package resources."""

    def __init__(self):
        self.env = Environment(
            loader=PackageTemplateLoader(),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_path: str, context: dict) -> str:
        """Render a template with the given context."""
        template = self.env.get_template(template_path)
        return template.render(**context)

    def render_to_file(self, template_path: str, output_path: Path, context: dict):
        """Render a template and write to output file."""
        content = self.render(template_path, context)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)

    def copy_static(self, src_path: str, dest_path: Path):
        """Copy a static (non-template) file."""
        ref = files("mpm.templates").joinpath(src_path)
        with as_file(ref) as src:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dest_path)
```

---

## Template Maintenance Strategy

### Challenge

The current repository IS the working reference implementation. We need to:

1. Keep the "live" repo as a working example
2. Extract templates for the CLI tool
3. Ensure both stay in sync

### Solution: Single Source of Truth

**Approach:** The templates in `src/mpm/templates/` ARE the source of truth. The root-level files in this repo are generated/maintained separately for demonstration purposes.

**Workflow:**

1. **Development:** Edit templates in `src/mpm/templates/`
2. **Testing:** Run `mpm` CLI locally to generate test projects
3. **Verification:** Compare generated output with expected structure
4. **Demo repo:** Manually maintain root-level files as a showcase (or regenerate periodically)

### Directory Naming Conventions

To avoid Jinja2 conflicts with directory names containing `{{}}`:

| Placeholder | Meaning | Replaced With |
|-------------|---------|---------------|
| `__package__` | Package name directory | `greeter`, `printer`, `auth`, etc. |
| `__namespace__` | Namespace directory | `my_project`, `modern_python_monorepo` |

**Example transformation:**

```
templates/monorepo/libs/__package__/__namespace__/__package__/__init__.py.jinja
                         ↓
output: libs/greeter/my_project/greeter/__init__.py
```

### Testing Templates

```python
# tests/test_templates.py
import tempfile
from pathlib import Path
from mpm.generators.project import generate_project
from mpm.config import ProjectConfig

def test_monorepo_generation():
    """Test that monorepo structure generates correctly."""
    config = ProjectConfig(
        project_name="test_project",
        structure="monorepo",
        python_version="3.13",
        with_samples=True,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "test_project"
        generate_project(config, output)

        # Verify structure
        assert (output / "pyproject.toml").exists()
        assert (output / "libs" / "greeter" / "pyproject.toml").exists()
        assert (output / "apps" / "printer" / "pyproject.toml").exists()

        # Verify content
        pyproject = (output / "pyproject.toml").read_text()
        assert "test_project" in pyproject
```

---

## MkDocs Documentation Options

### Theme Choices

Users can choose between two MkDocs themes:

#### Material for MkDocs (Default, Recommended)

**Source:** [Official Site](https://squidfunk.github.io/mkdocs-material/) | [GitHub](https://github.com/squidfunk/mkdocs-material)

| Metric | Value |
|--------|-------|
| GitHub Stars | 25,000+ |
| Maturity | 9 years (since 2016) |
| Used By | OpenAI, Microsoft, Google, Netflix, AWS |

**Features:**

- Responsive design, dark mode
- Full-text instant search
- Social cards generation
- Blog plugin, version selector
- Code annotations, copy button
- Mermaid diagrams
- 60+ languages

#### mkdocs-shadcn (Alternative)

**Source:** [GitHub](https://github.com/asiffer/mkdocs-shadcn) | [Documentation](https://asiffer.github.io/mkdocs-shadcn/)

| Metric | Value |
|--------|-------|
| GitHub Stars | 79 |
| Maturity | 1 year (since 2024) |
| Design | shadcn/ui aesthetic |

**Features:**

- Modern, clean design
- Dark/light mode
- Tailwind CSS based
- Built-in Excalidraw plugin
- mkdocstrings support

### Updated CLI Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--with-docs` | Include MkDocs documentation site | False |
| `--docs-theme` | Theme: `material` or `shadcn` | `material` |

### Updated Interactive Prompt

```
? Include documentation site (MkDocs)?
  > Yes - Material theme (recommended, enterprise-ready)
    Yes - shadcn theme (modern UI aesthetic)
    No
```

---

## Build & Distribution

### Package Format: Both Wheel and Sdist

**Source:** [Python Packaging Guide](https://packaging.python.org/en/latest/discussions/package-formats/) | [Real Python - Wheels](https://realpython.com/python-wheels/)

**Decision:** Publish both wheel (.whl) and source distribution (.tar.gz) to PyPI.

**Rationale:**

- **Wheel:** Fast installation, no build step required
- **Sdist:** Required by conda-forge, fallback for edge cases
- **Best Practice:** PyPI recommends uploading both

**Build Command:**

```bash
# Build both wheel and sdist
uv build
# or
python -m build

# Output:
# dist/modern_python_monorepo-0.1.0-py3-none-any.whl
# dist/modern_python_monorepo-0.1.0.tar.gz
```

**Wheel Type:** `py3-none-any` (pure Python, platform-independent)

---

## CI/CD Pipeline

### Automated PyPI Publishing with Trusted Publishers

**Source:** [PyPI Trusted Publishers](https://blog.pypi.org/posts/2023-04-20-introducing-trusted-publishers/) | [GitHub Action](https://github.com/pypa/gh-action-pypi-publish) | [Python Packaging Guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)

### Workflow Strategy

| Trigger | Action |
|---------|--------|
| PR to `main` | Run tests, lint, type-check |
| Push to `main` | Run tests + build verification |
| Tag `v*.*.*` | Build + publish to PyPI |

### GitHub Actions Workflow

```yaml
# .github/workflows/release.yml
name: Release to PyPI

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: "0.5.14"

      - name: Set up Python
        run: uv python install 3.13

      - name: Build package
        run: uv build

      - name: Upload dist artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  publish:
    needs: build
    runs-on: ubuntu-latest
    environment: pypi  # Recommended: use GitHub environment for extra security
    permissions:
      id-token: write  # Required for trusted publishing

    steps:
      - name: Download dist artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        # No token needed - uses OIDC trusted publishing
```

### PyPI Trusted Publisher Setup

1. **On PyPI:**
   - Go to project settings → "Publishing"
   - Add new trusted publisher:
     - Owner: `gruckion`
     - Repository: `modern_python_monorepo`
     - Workflow: `release.yml`
     - Environment: `pypi` (optional but recommended)

2. **On GitHub:**
   - Create environment named `pypi`
   - Add protection rules (optional):
     - Required reviewers
     - Deployment branches: only tags

### Release Process

```bash
# 1. Update version in pyproject.toml
# 2. Commit changes
git add pyproject.toml
git commit -m "chore: bump version to 0.2.0"

# 3. Create and push tag
git tag v0.2.0
git push origin main --tags

# 4. GitHub Actions automatically:
#    - Builds wheel + sdist
#    - Publishes to PyPI via trusted publisher
```

### PR Workflow

```yaml
# .github/workflows/pr.yml
name: PR Checks

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.13

      - name: Install dependencies
        run: uv sync --all-packages

      - name: Lint
        run: uv run ruff check .

      - name: Format check
        run: uv run ruff format --check .

      - name: Type check
        run: uv run ty check

      - name: Test
        run: uv run pytest --cov

      - name: Build verification
        run: uv build
```

---

## References

### CLI Tool Research

- [Better-T-Stack GitHub](https://github.com/AmanVarshney01/create-better-t-stack)
- [Better-T-Stack Website](https://www.better-t-stack.dev/)
- [TanStack Start Quick Start](https://tanstack.com/start/latest/docs/framework/react/quick-start)
- [TanStack Create Start README](https://github.com/TanStack/create-tsrouter-app/blob/main/cli/create-start-app/README.md)

### Python CLI Frameworks

- [Typer Documentation](https://typer.tiangolo.com/)
- [Typer Alternatives](https://typer.tiangolo.com/alternatives/)
- [Questionary GitHub](https://github.com/tmbo/questionary)
- [Click Documentation](https://click.palletsprojects.com/)
- [Rich Documentation](https://rich.readthedocs.io/)

### Project Scaffolding

- [Copier Documentation](https://copier.readthedocs.io/)
- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [From Cookiecutter to Copier](https://medium.com/@gema.correa/from-cookiecutter-to-copier-uv-and-just-the-new-python-project-stack-90fb4ba247a9)
