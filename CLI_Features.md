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
- [Build Backend Considerations](#build-backend-considerations)
  - [Two-Tier Build Strategy](#two-tier-build-strategy)
  - [TOML Linter Warning](#toml-linter-warning-dynamic--una)
  - [Generated Project Configuration](#generated-project-configuration)
- [Implementation Guide](#implementation-guide)
  - [Phase 1: Project Setup](#phase-1-project-setup)
  - [Phase 2: Core Implementation Files](#phase-2-core-implementation-files)
  - [Phase 3: Template Files](#phase-3-template-files)
  - [Phase 4: Comprehensive Testing Strategy](#phase-4-comprehensive-testing-strategy)
    - [Test Directory Structure](#41-test-directory-structure)
    - [Test Fixtures](#42-test-fixtures-conftestpy)
    - [Unit Tests - CLI](#43-unit-tests---cli-commands-test_clipy)
    - [Unit Tests - Config](#44-unit-tests---config-models-test_configpy)
    - [Unit Tests - Renderer](#45-unit-tests---template-renderer-test_rendererpy)
    - [Integration Tests](#46-integration-tests---cli-with-various-configurations-test_integrationpy)
    - [End-to-End Tests](#47-end-to-end-tests---generated-projects-actually-work-test_e2epy)
    - [Test Configuration](#48-test-configuration-pyprojecttoml-additions)
    - [Running Tests](#49-running-tests-during-development)
    - [Manual Testing Workflow](#410-manual-testing-workflow)
    - [Test Matrix Coverage](#411-test-matrix-coverage)
  - [Phase 5: Build and Verify](#phase-5-build-and-verify)
  - [Implementation Checklist](#implementation-checklist)

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

### pyproject.toml Configuration for MPM CLI

The MPM CLI tool uses `uv_build` as its build backend (not hatchling). Since templates are stored inside the module directory (`src/mpm/templates/`), they are automatically included in the wheel.

```toml
[project]
name = "modern-python-monorepo"
version = "0.1.0"
description = "Modern Python Monorepo CLI - Scaffold production-ready Python projects"
readme = "README.md"
license = { text = "MIT" }
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

[build-system]
requires = ["uv_build>=0.9.16,<0.10.0"]
build-backend = "uv_build"

[tool.uv.build-backend]
module-root = "src"
# Templates at src/mpm/templates/ are automatically included
# No additional configuration needed for files inside the module
```

**Why uv_build?**
- 10-35x faster than hatchling/setuptools
- No Python required to build
- Simpler configuration
- Files inside module directory auto-included

**Note:** This configuration is for the MPM CLI tool itself. Projects *generated* by MPM CLI use hatchling (required by Una for monorepo workspace builds) - see [Build Backend Considerations](#build-backend-considerations).

---

## Build Backend Considerations

### Two-Tier Build Strategy

The MPM CLI project uses **two different build backends** depending on the context:

| Project Type | Build Backend | Reason |
|--------------|---------------|--------|
| **MPM CLI tool** (this package) | `uv_build` | Standalone package, fastest build times (10-35x faster) |
| **Generated monorepo projects** (user's projects) | `hatchling + hatch-una` | Required for Una workspace dependency injection |

### Why the Distinction?

**MPM CLI Tool (`uv_build`):**
- Self-contained Python package with no workspace dependencies
- Dependencies are standard PyPI packages (typer, jinja2, etc.)
- Benefits from fastest possible build times
- No need for workspace dependency rewriting

**Generated Projects (`hatchling + hatch-una`):**
- Use uv workspaces with `workspace = true` sources
- Una's `hatch-una` plugin is essential for:
  - Rewriting workspace dependencies to actual version constraints at build time
  - Injecting metadata via the `dynamic = ["una"]` hook
  - Enabling `una-build` hooks for proper wheel generation
- Without hatch-una, workspace dependencies wouldn't be resolvable when published to PyPI

### TOML Linter Warning: `dynamic = ["una"]`

**Issue:** The "Even Better TOML" VS Code extension flags this error:

```
"una" is not one of ["version","description","readme","requires-python",...]
```

**Explanation:** This is a **linter false positive**, not an actual error.

- **PEP 621** defines a standard set of dynamic metadata fields
- The `hatch-una` plugin extends this with a custom `"una"` dynamic field
- The linter validates strictly against PEP 621 and doesn't recognize custom extensions
- **The build works correctly** because Hatchling's plugin system allows custom dynamic fields

**Source:** Looking at the Una source code (`files.py`), this is intentionally generated:

```python
_TEMPLATE_PYPROJ = """\
[project]
name = "{name}"
...
dynamic = ["una"]          # needed for hatch-una metadata hook to work
```

The `hatch-una` metadata hook (`UnaMetaHook` in `build.py`) processes this custom dynamic field to inject workspace dependencies.

**Mitigation Options:**
1. **Ignore the warning** - it's safe, builds work correctly
2. **Add a comment** explaining it's for hatch-una
3. **Configure the linter** to allow custom dynamic fields (if supported)

### Generated Project Configuration

Projects generated by MPM CLI will have this structure in each package:

```toml
# libs/greeter/pyproject.toml or apps/printer/pyproject.toml
[project]
name = "greeter"
version = "0.1.0"
dependencies = ["some-library"]
dynamic = ["una"]          # For hatch-una metadata hook

[build-system]
requires = ["hatchling", "hatch-una"]
build-backend = "hatchling.build"

[tool.hatch.build.hooks.una-build]
[tool.hatch.metadata.hooks.una-meta]

[tool.uv.sources.some-workspace-dep]
workspace = true
```

The root `pyproject.toml` will have:

```toml
[tool.uv.workspace]
members = ["apps/*", "libs/*"]

[tool.una]
namespace = "project_namespace"
requires-python = ">=3.13"
```

### Verifying Template Inclusion

After building, verify templates are in the wheel:

```bash
# Build the package
uv build

# Inspect wheel contents (wheel is a ZIP file)
unzip -l dist/modern_python_monorepo-*.whl | grep templates

# Expected output:
# mpm/templates/__init__.py
# mpm/templates/base/pyproject.toml.jinja
# mpm/templates/base/README.md.jinja
# ...
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

## Implementation Guide

This section provides step-by-step instructions for implementing the MPM CLI tool.

### Phase 1: Project Setup

**Goal:** Create the MPM CLI package structure within this repository.

1. **Create the MPM package directory structure:**
   ```
   mpm/
   ├── pyproject.toml          # MPM CLI package config (uses uv_build)
   ├── README.md               # CLI documentation
   └── src/
       └── mpm/
           ├── __init__.py     # Version: __version__ = "0.1.0"
           ├── cli.py          # Typer app entry point
           ├── prompts.py      # Questionary prompts
           ├── config.py       # Pydantic models
           ├── utils.py        # Helper functions
           ├── generators/
           │   ├── __init__.py
           │   ├── project.py
           │   ├── package.py
           │   ├── renderer.py
           │   ├── docker.py
           │   ├── ci.py
           │   └── docs.py
           └── templates/
               └── (see Template Directory Structure section)
   ```

2. **Create `mpm/pyproject.toml`:**
   ```toml
   [project]
   name = "modern-python-monorepo"
   version = "0.1.0"
   description = "Modern Python Monorepo CLI - Scaffold production-ready Python projects"
   readme = "README.md"
   license = { text = "MIT" }
   requires-python = ">=3.11"
   keywords = ["cli", "scaffold", "monorepo", "python", "uv", "una"]
   classifiers = [
       "Development Status :: 4 - Beta",
       "Environment :: Console",
       "Intended Audience :: Developers",
       "License :: OSI Approved :: MIT License",
       "Programming Language :: Python :: 3.11",
       "Programming Language :: Python :: 3.12",
       "Programming Language :: Python :: 3.13",
       "Topic :: Software Development :: Code Generators",
   ]
   dependencies = [
       "typer>=0.12.0",
       "questionary>=2.1.0",
       "rich>=13.0.0",
       "jinja2>=3.1.0",
       "pydantic>=2.0.0",
   ]

   [project.scripts]
   mpm = "mpm.cli:app"

   [build-system]
   requires = ["uv_build>=0.9.16,<0.10.0"]
   build-backend = "uv_build"

   [tool.uv.build-backend]
   module-root = "src"
   ```

3. **Add MPM to workspace** - Update root `pyproject.toml`:
   ```toml
   [tool.uv.workspace]
   members = ["apps/*", "libs/*", "mpm"]
   ```

### Phase 2: Core Implementation Files

#### 2.1 `src/mpm/__init__.py`
```python
"""Modern Python Monorepo CLI."""

__version__ = "0.1.0"
```

#### 2.2 `src/mpm/config.py` - Pydantic Models
```python
"""Configuration models for MPM CLI."""

from enum import Enum
from pydantic import BaseModel, Field


class ProjectStructure(str, Enum):
    MONOREPO = "monorepo"
    SINGLE = "single"


class PythonVersion(str, Enum):
    PY311 = "3.11"
    PY312 = "3.12"
    PY313 = "3.13"


class LicenseType(str, Enum):
    MIT = "MIT"
    APACHE = "Apache-2.0"
    GPL = "GPL-3.0"
    NONE = "none"


class DocsTheme(str, Enum):
    MATERIAL = "material"
    SHADCN = "shadcn"


class ProjectConfig(BaseModel):
    """Configuration for project generation."""

    project_name: str = Field(..., description="Project name (Python identifier)")
    project_slug: str = Field(..., description="URL-safe project slug")
    project_description: str = Field(default="", description="Project description")
    structure: ProjectStructure = Field(default=ProjectStructure.MONOREPO)
    python_version: PythonVersion = Field(default=PythonVersion.PY313)
    license_type: LicenseType = Field(default=LicenseType.MIT)

    # Optional features
    with_samples: bool = Field(default=False)
    with_docker: bool = Field(default=False)
    with_ci: bool = Field(default=False)
    with_pypi: bool = Field(default=False)
    with_docs: bool = Field(default=False)
    docs_theme: DocsTheme = Field(default=DocsTheme.MATERIAL)

    # Git
    init_git: bool = Field(default=True)

    # Metadata
    author_name: str = Field(default="")
    author_email: str = Field(default="")
    github_owner: str = Field(default="")
    github_repo: str = Field(default="")

    @property
    def namespace(self) -> str:
        """Python import namespace (underscores)."""
        return self.project_name.replace("-", "_")


class PackageConfig(BaseModel):
    """Configuration for package generation (add lib/app)."""

    package_name: str
    package_type: str  # "lib" or "app"
    description: str = ""
    with_docker: bool = False  # Only for apps
```

#### 2.3 `src/mpm/prompts.py` - Interactive Prompts
```python
"""Questionary prompts for interactive mode."""

import questionary
from questionary import Choice

from mpm.config import (
    DocsTheme,
    LicenseType,
    ProjectConfig,
    ProjectStructure,
    PythonVersion,
)


def prompt_project_name() -> str:
    """Prompt for project name."""
    return questionary.text(
        "Project name:",
        validate=lambda x: len(x) > 0 or "Project name is required",
    ).ask()


def prompt_structure() -> ProjectStructure:
    """Prompt for project structure."""
    choice = questionary.select(
        "Project structure:",
        choices=[
            Choice("Monorepo (libs/ and apps/ workspaces)", ProjectStructure.MONOREPO),
            Choice("Single package", ProjectStructure.SINGLE),
        ],
    ).ask()
    return choice


def prompt_python_version() -> PythonVersion:
    """Prompt for Python version."""
    return questionary.select(
        "Python version requirement:",
        choices=[
            Choice("3.11+", PythonVersion.PY311),
            Choice("3.12+", PythonVersion.PY312),
            Choice("3.13+", PythonVersion.PY313),
        ],
        default=PythonVersion.PY313,
    ).ask()


def prompt_features() -> dict[str, bool]:
    """Prompt for features to include."""
    features = questionary.checkbox(
        "Select features to include:",
        choices=[
            Choice("Ruff (linting & formatting)", checked=True, value="ruff"),
            Choice("ty (type checking)", checked=True, value="ty"),
            Choice("pytest (testing)", checked=True, value="pytest"),
            Choice("poethepoet (task runner)", checked=True, value="poe"),
            Choice("Pre-commit hooks", checked=True, value="precommit"),
            Choice("GitHub Actions CI", checked=False, value="ci"),
            Choice("PyPI publishing workflow", checked=False, value="pypi"),
            Choice("Docker support", checked=False, value="docker"),
        ],
    ).ask()
    return {f: f in features for f in ["ruff", "ty", "pytest", "poe", "precommit", "ci", "pypi", "docker"]}


def prompt_samples() -> bool:
    """Prompt for sample packages."""
    return questionary.select(
        "Include sample packages?",
        choices=[
            Choice("Yes (greeter lib + printer app)", True),
            Choice("No (empty structure)", False),
        ],
    ).ask()


def prompt_docs() -> tuple[bool, DocsTheme | None]:
    """Prompt for documentation setup."""
    choice = questionary.select(
        "Include documentation site (MkDocs)?",
        choices=[
            Choice("Yes - Material theme (recommended)", "material"),
            Choice("Yes - shadcn theme (modern UI)", "shadcn"),
            Choice("No", "none"),
        ],
    ).ask()
    if choice == "none":
        return False, None
    return True, DocsTheme(choice)


def prompt_license() -> LicenseType:
    """Prompt for license type."""
    return questionary.select(
        "License:",
        choices=[
            Choice("MIT", LicenseType.MIT),
            Choice("Apache-2.0", LicenseType.APACHE),
            Choice("GPL-3.0", LicenseType.GPL),
            Choice("None", LicenseType.NONE),
        ],
    ).ask()


def gather_project_config(name: str | None = None) -> ProjectConfig:
    """Gather all configuration via interactive prompts."""
    project_name = name or prompt_project_name()
    project_slug = project_name.replace("_", "-").lower()

    structure = prompt_structure()
    python_version = prompt_python_version()
    features = prompt_features()
    with_samples = prompt_samples() if structure == ProjectStructure.MONOREPO else False
    with_docs, docs_theme = prompt_docs()
    license_type = prompt_license()

    return ProjectConfig(
        project_name=project_name.replace("-", "_"),
        project_slug=project_slug,
        structure=structure,
        python_version=python_version,
        with_samples=with_samples,
        with_docker=features.get("docker", False),
        with_ci=features.get("ci", False),
        with_pypi=features.get("pypi", False),
        with_docs=with_docs,
        docs_theme=docs_theme or DocsTheme.MATERIAL,
        license_type=license_type,
    )
```

#### 2.4 `src/mpm/cli.py` - Typer Application
```python
"""MPM CLI - Modern Python Monorepo scaffolding tool."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.panel import Panel

from mpm import __version__
from mpm.config import DocsTheme, LicenseType, ProjectConfig, ProjectStructure, PythonVersion
from mpm.generators.project import generate_project
from mpm.prompts import gather_project_config

app = typer.Typer(
    name="mpm",
    help="Modern Python Monorepo CLI - Scaffold production-ready Python projects",
    add_completion=True,
)
console = Console()

# Subcommand for adding packages
add_app = typer.Typer(help="Add a new package to an existing project")
app.add_typer(add_app, name="add")


def version_callback(value: bool) -> None:
    if value:
        console.print(f"mpm version {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    project_name: Annotated[Optional[str], typer.Argument(help="Project name")] = None,
    monorepo: Annotated[bool, typer.Option("--monorepo", "-m", help="Create monorepo structure")] = False,
    single: Annotated[bool, typer.Option("--single", "-s", help="Create single package structure")] = False,
    python: Annotated[str, typer.Option("--python", "-p", help="Python version")] = "3.13",
    with_samples: Annotated[bool, typer.Option(help="Include sample packages")] = False,
    with_docker: Annotated[bool, typer.Option(help="Include Docker configuration")] = False,
    with_ci: Annotated[bool, typer.Option(help="Include GitHub Actions CI")] = False,
    with_pypi: Annotated[bool, typer.Option(help="Include PyPI publishing workflow")] = False,
    with_docs: Annotated[bool, typer.Option(help="Include MkDocs documentation")] = False,
    docs_theme: Annotated[str, typer.Option(help="Docs theme: material or shadcn")] = "material",
    license: Annotated[str, typer.Option("--license", "-l", help="License type")] = "MIT",
    no_git: Annotated[bool, typer.Option(help="Skip git initialization")] = False,
    yes: Annotated[bool, typer.Option("--yes", "-y", help="Accept defaults (non-interactive)")] = False,
    version: Annotated[bool, typer.Option("--version", "-v", callback=version_callback, is_eager=True)] = False,
) -> None:
    """Create a new Modern Python Monorepo project."""
    # If subcommand invoked, skip
    if ctx.invoked_subcommand is not None:
        return

    # Interactive mode or flags mode
    if yes or (monorepo or single):
        # Non-interactive: build config from flags
        structure = ProjectStructure.SINGLE if single else ProjectStructure.MONOREPO
        config = ProjectConfig(
            project_name=(project_name or "my_project").replace("-", "_"),
            project_slug=(project_name or "my-project").replace("_", "-").lower(),
            structure=structure,
            python_version=PythonVersion(python),
            with_samples=with_samples,
            with_docker=with_docker,
            with_ci=with_ci,
            with_pypi=with_pypi,
            with_docs=with_docs,
            docs_theme=DocsTheme(docs_theme),
            license_type=LicenseType(license.upper()) if license != "none" else LicenseType.NONE,
            init_git=not no_git,
        )
    else:
        # Interactive mode
        config = gather_project_config(project_name)
        config.init_git = not no_git

    # Generate project
    output_path = Path.cwd() / config.project_slug
    generate_project(config, output_path)

    # Success message
    console.print(Panel.fit(
        f"[green]✓[/green] Created [bold]{config.project_slug}[/bold]\n\n"
        f"Next steps:\n"
        f"  cd {config.project_slug}\n"
        f"  uv sync --all-packages\n"
        f"  poe check",
        title="Project Created",
    ))


@add_app.command("lib")
def add_lib(
    name: Annotated[str, typer.Argument(help="Library name")],
    description: Annotated[str, typer.Option("--description", "-d")] = "",
) -> None:
    """Add a new library package to libs/."""
    from mpm.generators.package import add_package
    add_package(name, "lib", description)


@add_app.command("app")
def add_app_cmd(
    name: Annotated[str, typer.Argument(help="Application name")],
    description: Annotated[str, typer.Option("--description", "-d")] = "",
    docker: Annotated[bool, typer.Option("--docker", help="Include Dockerfile")] = False,
) -> None:
    """Add a new application package to apps/."""
    from mpm.generators.package import add_package
    add_package(name, "app", description, with_docker=docker)


if __name__ == "__main__":
    app()
```

#### 2.5 `src/mpm/generators/renderer.py` - Template Rendering
```python
"""Jinja2 template renderer using importlib.resources."""

from importlib.resources import as_file, files
from pathlib import Path
from typing import Any

from jinja2 import BaseLoader, Environment, TemplateNotFound


class PackageTemplateLoader(BaseLoader):
    """Load templates from package resources."""

    def __init__(self, package: str = "mpm.templates"):
        self.package = package

    def get_source(self, environment: Environment, template: str) -> tuple[str, str, callable]:
        try:
            source = files(self.package).joinpath(template).read_text()
            return source, template, lambda: True
        except (FileNotFoundError, TypeError):
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

    def render(self, template_path: str, context: dict[str, Any]) -> str:
        """Render a template with the given context."""
        template = self.env.get_template(template_path)
        return template.render(**context)

    def render_to_file(self, template_path: str, output_path: Path, context: dict[str, Any]) -> None:
        """Render a template and write to output file."""
        content = self.render(template_path, context)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)

    def copy_static(self, src_path: str, dest_path: Path) -> None:
        """Copy a static (non-template) file."""
        import shutil
        ref = files("mpm.templates").joinpath(src_path)
        with as_file(ref) as src:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dest_path)
```

#### 2.6 `src/mpm/generators/project.py` - Main Generator
```python
"""Project generator - creates the full project structure."""

import subprocess
from pathlib import Path

from rich.console import Console

from mpm.config import ProjectConfig, ProjectStructure
from mpm.generators.renderer import TemplateRenderer

console = Console()


def generate_project(config: ProjectConfig, output_path: Path) -> None:
    """Generate a complete project from configuration."""
    renderer = TemplateRenderer()
    context = config.model_dump()

    console.print(f"[dim]Creating project at {output_path}...[/dim]")

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate base files (always)
    _generate_base_files(renderer, output_path, context)

    # Generate structure-specific files
    if config.structure == ProjectStructure.MONOREPO:
        _generate_monorepo_structure(renderer, output_path, context)
        if config.with_samples:
            _generate_sample_packages(renderer, output_path, context)
    else:
        _generate_single_package(renderer, output_path, context)

    # Generate optional features
    if config.with_docker:
        _generate_docker_files(renderer, output_path, context)

    if config.with_ci:
        _generate_ci_files(renderer, output_path, context, config.with_pypi)

    if config.with_docs:
        _generate_docs(renderer, output_path, context, config.docs_theme)

    # Initialize git
    if config.init_git:
        _init_git(output_path)

    console.print("[green]✓[/green] Project generated successfully")


def _generate_base_files(renderer: TemplateRenderer, output: Path, ctx: dict) -> None:
    """Generate base project files."""
    renderer.render_to_file("base/pyproject.toml.jinja", output / "pyproject.toml", ctx)
    renderer.render_to_file("base/README.md.jinja", output / "README.md", ctx)
    renderer.render_to_file("base/.python-version.jinja", output / ".python-version", ctx)
    renderer.copy_static("base/.gitignore", output / ".gitignore")

    if ctx.get("license_type") and ctx["license_type"] != "none":
        renderer.render_to_file("base/LICENSE.jinja", output / "LICENSE", ctx)


def _generate_monorepo_structure(renderer: TemplateRenderer, output: Path, ctx: dict) -> None:
    """Generate monorepo directory structure."""
    (output / "libs").mkdir(exist_ok=True)
    (output / "apps").mkdir(exist_ok=True)


def _generate_sample_packages(renderer: TemplateRenderer, output: Path, ctx: dict) -> None:
    """Generate sample greeter lib and printer app."""
    from mpm.generators.package import generate_lib_package, generate_app_package

    generate_lib_package(
        renderer, output,
        package_name="greeter",
        namespace=ctx["namespace"],
        ctx=ctx,
    )
    generate_app_package(
        renderer, output,
        package_name="printer",
        namespace=ctx["namespace"],
        ctx=ctx,
        with_docker=ctx.get("with_docker", False),
    )


def _generate_single_package(renderer: TemplateRenderer, output: Path, ctx: dict) -> None:
    """Generate single package structure."""
    src_dir = output / "src" / ctx["namespace"]
    src_dir.mkdir(parents=True, exist_ok=True)
    renderer.render_to_file("single/__init__.py.jinja", src_dir / "__init__.py", ctx)
    (src_dir / "py.typed").touch()


def _generate_docker_files(renderer: TemplateRenderer, output: Path, ctx: dict) -> None:
    """Generate Docker configuration files."""
    renderer.render_to_file("docker/docker-compose.yml.jinja", output / "docker-compose.yml", ctx)
    renderer.render_to_file("docker/docker-bake.hcl.jinja", output / "docker-bake.hcl", ctx)
    renderer.copy_static("docker/.dockerignore", output / ".dockerignore")


def _generate_ci_files(renderer: TemplateRenderer, output: Path, ctx: dict, with_pypi: bool) -> None:
    """Generate GitHub Actions workflows."""
    workflows = output / ".github" / "workflows"
    workflows.mkdir(parents=True, exist_ok=True)
    renderer.render_to_file("ci/pr.yml.jinja", workflows / "pr.yml", ctx)
    if with_pypi:
        renderer.render_to_file("ci/release.yml.jinja", workflows / "release.yml", ctx)


def _generate_docs(renderer: TemplateRenderer, output: Path, ctx: dict, theme: str) -> None:
    """Generate MkDocs documentation."""
    docs_dir = output / "docs"
    docs_dir.mkdir(exist_ok=True)
    theme_dir = f"docs/{theme}"
    renderer.render_to_file(f"{theme_dir}/mkdocs.yml.jinja", output / "mkdocs.yml", ctx)
    renderer.render_to_file(f"{theme_dir}/index.md.jinja", docs_dir / "index.md", ctx)


def _init_git(output: Path) -> None:
    """Initialize git repository."""
    try:
        subprocess.run(["git", "init"], cwd=output, capture_output=True, check=True)
        console.print("[green]✓[/green] Initialized git repository")
    except subprocess.CalledProcessError:
        console.print("[yellow]⚠[/yellow] Failed to initialize git repository")
```

### Phase 3: Template Files

Create Jinja2 templates in `src/mpm/templates/`. Key templates to create:

#### 3.1 `templates/base/pyproject.toml.jinja` (Monorepo Root)
```jinja
[project]
name = "{{ project_slug }}"
version = "0.1.0"
description = "{{ project_description }}"
readme = "README.md"
requires-python = ">={{ python_version }}"
dependencies = []

[dependency-groups]
dev = [
    "una>=0.7.0",
    "ruff>=0.8.0",
    "ty>=0.0.1a6",
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    "poethepoet>=0.31.0",
]
{% if with_docs %}
docs = [
    "mkdocs>=1.6.0",
    {% if docs_theme == "material" %}
    "mkdocs-material>=9.0.0",
    {% else %}
    "mkdocs-shadcn>=0.9.0",
    {% endif %}
    "mkdocstrings[python]>=0.27.0",
]
{% endif %}

[tool.uv]
package = false

[tool.uv.workspace]
members = ["apps/*", "libs/*"]

[tool.una]
namespace = "{{ namespace }}"
requires-python = ">={{ python_version }}"

[tool.ruff]
line-length = 120

[tool.ruff.lint]
select = ["A", "B", "E", "F", "I", "N", "UP", "W", "RUF", "T100"]

[tool.ruff.lint.isort]
known-first-party = ["{{ namespace }}"]

[tool.pytest.ini_options]
testpaths = ["apps", "libs"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "--doctest-modules -v"

[tool.poe.tasks]
fmt = "ruff format"
lint = "ruff check --fix"
check = "ty check"
test = "pytest"
cov = "pytest --cov=apps --cov=libs --cov-report=term-missing"
all = ["fmt", "lint", "check", "test"]
```

#### 3.2 `templates/monorepo/libs/__package__/pyproject.toml.jinja`
```jinja
[project]
name = "{{ package_name }}"
version = "0.1.0"
description = "{{ package_description }}"
authors = []
dependencies = []
requires-python = ">={{ python_version }}"
dynamic = ["una"]

[build-system]
requires = ["hatchling", "hatch-una"]
build-backend = "hatchling.build"

[tool.hatch.metadata]
allow-direct-references = true

[tool.uv]
dev-dependencies = []

[tool.uv.sources]

[tool.hatch.build.hooks.una-build]
[tool.hatch.metadata.hooks.una-meta]
```

### Phase 4: Comprehensive Testing Strategy

Testing is critical for the MPM CLI. You must write and run tests continuously during development to ensure all features work correctly. Use temporary directories to test CLI output in isolation.

#### 4.1 Test Directory Structure

```
mpm/
└── tests/
    ├── __init__.py
    ├── conftest.py              # Shared fixtures
    ├── test_cli.py              # CLI command tests
    ├── test_config.py           # Pydantic model tests
    ├── test_renderer.py         # Template rendering tests
    ├── test_generators.py       # Generator unit tests
    ├── test_integration.py      # Full CLI integration tests
    └── test_e2e.py              # End-to-end tests (generated projects work)
```

#### 4.2 Test Fixtures (`conftest.py`)

```python
"""Shared test fixtures for MPM CLI tests."""

import tempfile
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from mpm.cli import app


@pytest.fixture
def cli_runner() -> CliRunner:
    """Typer CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def run_mpm(cli_runner: CliRunner, temp_dir: Path):
    """Factory fixture to run MPM CLI in temp directory."""
    import os

    def _run_mpm(*args: str) -> tuple[int, str, Path]:
        """Run mpm with args, return (exit_code, output, project_path)."""
        original_dir = os.getcwd()
        os.chdir(temp_dir)
        try:
            result = cli_runner.invoke(app, list(args))
            # Find generated project directory
            dirs = [d for d in temp_dir.iterdir() if d.is_dir()]
            project_path = dirs[0] if dirs else temp_dir
            return result.exit_code, result.stdout, project_path
        finally:
            os.chdir(original_dir)

    return _run_mpm
```

#### 4.3 Unit Tests - CLI Commands (`test_cli.py`)

```python
"""Unit tests for CLI commands."""

from typer.testing import CliRunner

from mpm.cli import app


def test_version(cli_runner: CliRunner):
    """Test --version flag."""
    result = cli_runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "mpm version" in result.stdout


def test_help(cli_runner: CliRunner):
    """Test --help flag."""
    result = cli_runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Modern Python Monorepo" in result.stdout
    assert "--monorepo" in result.stdout
    assert "--single" in result.stdout


def test_add_help(cli_runner: CliRunner):
    """Test mpm add --help."""
    result = cli_runner.invoke(app, ["add", "--help"])
    assert result.exit_code == 0
    assert "lib" in result.stdout
    assert "app" in result.stdout


def test_mutually_exclusive_flags(cli_runner: CliRunner, temp_dir):
    """Test that --monorepo and --single are mutually exclusive."""
    import os
    os.chdir(temp_dir)
    result = cli_runner.invoke(app, ["test", "--monorepo", "--single", "-y"])
    # Should use the last flag or raise error - document expected behavior
    assert result.exit_code == 0  # or handle error case
```

#### 4.4 Unit Tests - Config Models (`test_config.py`)

```python
"""Unit tests for Pydantic configuration models."""

import pytest
from pydantic import ValidationError

from mpm.config import (
    DocsTheme,
    LicenseType,
    ProjectConfig,
    ProjectStructure,
    PythonVersion,
)


def test_project_config_defaults():
    """Test ProjectConfig with minimal required fields."""
    config = ProjectConfig(
        project_name="my_project",
        project_slug="my-project",
    )
    assert config.structure == ProjectStructure.MONOREPO
    assert config.python_version == PythonVersion.PY313
    assert config.license_type == LicenseType.MIT
    assert config.with_samples is False
    assert config.with_docker is False
    assert config.init_git is True


def test_project_config_namespace():
    """Test namespace property."""
    config = ProjectConfig(
        project_name="my_awesome_project",
        project_slug="my-awesome-project",
    )
    assert config.namespace == "my_awesome_project"


def test_project_config_all_options():
    """Test ProjectConfig with all options enabled."""
    config = ProjectConfig(
        project_name="full_project",
        project_slug="full-project",
        project_description="A full-featured project",
        structure=ProjectStructure.MONOREPO,
        python_version=PythonVersion.PY312,
        license_type=LicenseType.APACHE,
        with_samples=True,
        with_docker=True,
        with_ci=True,
        with_pypi=True,
        with_docs=True,
        docs_theme=DocsTheme.SHADCN,
        init_git=False,
    )
    assert config.with_samples is True
    assert config.docs_theme == DocsTheme.SHADCN


def test_invalid_python_version():
    """Test that invalid Python version raises error."""
    with pytest.raises(ValidationError):
        ProjectConfig(
            project_name="test",
            project_slug="test",
            python_version="2.7",  # Invalid
        )
```

#### 4.5 Unit Tests - Template Renderer (`test_renderer.py`)

```python
"""Unit tests for template rendering."""

import pytest

from mpm.generators.renderer import TemplateRenderer


def test_renderer_initialization():
    """Test TemplateRenderer initializes correctly."""
    renderer = TemplateRenderer()
    assert renderer.env is not None


def test_render_simple_template(temp_dir):
    """Test rendering a simple template."""
    renderer = TemplateRenderer()

    # This tests that templates are accessible from package resources
    context = {
        "project_slug": "test-project",
        "project_description": "A test project",
        "python_version": "3.13",
        "namespace": "test_project",
    }

    # Test rendering base pyproject.toml
    content = renderer.render("base/pyproject.toml.jinja", context)
    assert "test-project" in content
    assert "3.13" in content


def test_render_to_file(temp_dir):
    """Test rendering template directly to file."""
    renderer = TemplateRenderer()
    output_file = temp_dir / "pyproject.toml"

    context = {
        "project_slug": "my-app",
        "python_version": "3.13",
        "namespace": "my_app",
    }

    renderer.render_to_file("base/pyproject.toml.jinja", output_file, context)

    assert output_file.exists()
    content = output_file.read_text()
    assert "my-app" in content
```

#### 4.6 Integration Tests - CLI with Various Configurations (`test_integration.py`)

**CRITICAL**: These tests verify that the CLI produces correct output for all configuration combinations.

```python
"""Integration tests for MPM CLI - tests full CLI execution with various configs."""

import subprocess
from pathlib import Path

import pytest


class TestMonorepoGeneration:
    """Test monorepo project generation."""

    def test_basic_monorepo(self, run_mpm):
        """Test basic monorepo generation."""
        exit_code, output, project = run_mpm("test-project", "--monorepo", "-y")

        assert exit_code == 0
        assert project.exists()
        assert (project / "pyproject.toml").exists()
        assert (project / "libs").is_dir()
        assert (project / "apps").is_dir()
        assert (project / ".gitignore").exists()
        assert (project / ".python-version").exists()

    def test_monorepo_with_samples(self, run_mpm):
        """Test monorepo with sample packages."""
        exit_code, output, project = run_mpm(
            "sample-project", "--monorepo", "--with-samples", "-y"
        )

        assert exit_code == 0

        # Verify greeter lib exists
        greeter = project / "libs" / "greeter"
        assert greeter.is_dir()
        assert (greeter / "pyproject.toml").exists()

        # Verify printer app exists
        printer = project / "apps" / "printer"
        assert printer.is_dir()
        assert (printer / "pyproject.toml").exists()

        # Verify namespace structure
        assert (greeter / "sample_project" / "greeter" / "__init__.py").exists()
        assert (printer / "sample_project" / "printer" / "__init__.py").exists()

    def test_monorepo_with_docker(self, run_mpm):
        """Test monorepo with Docker configuration."""
        exit_code, output, project = run_mpm(
            "docker-project", "--monorepo", "--with-docker", "-y"
        )

        assert exit_code == 0
        assert (project / "docker-compose.yml").exists()
        assert (project / "docker-bake.hcl").exists()
        assert (project / ".dockerignore").exists()

    def test_monorepo_with_ci(self, run_mpm):
        """Test monorepo with GitHub Actions CI."""
        exit_code, output, project = run_mpm(
            "ci-project", "--monorepo", "--with-ci", "-y"
        )

        assert exit_code == 0
        workflows = project / ".github" / "workflows"
        assert workflows.is_dir()
        assert (workflows / "pr.yml").exists()

    def test_monorepo_with_pypi(self, run_mpm):
        """Test monorepo with PyPI publishing workflow."""
        exit_code, output, project = run_mpm(
            "pypi-project", "--monorepo", "--with-ci", "--with-pypi", "-y"
        )

        assert exit_code == 0
        workflows = project / ".github" / "workflows"
        assert (workflows / "pr.yml").exists()
        assert (workflows / "release.yml").exists()

    def test_monorepo_with_docs_material(self, run_mpm):
        """Test monorepo with MkDocs Material theme."""
        exit_code, output, project = run_mpm(
            "docs-project", "--monorepo", "--with-docs", "--docs-theme", "material", "-y"
        )

        assert exit_code == 0
        assert (project / "mkdocs.yml").exists()
        assert (project / "docs" / "index.md").exists()

        # Verify Material theme configured
        mkdocs_content = (project / "mkdocs.yml").read_text()
        assert "material" in mkdocs_content.lower()

    def test_monorepo_with_docs_shadcn(self, run_mpm):
        """Test monorepo with MkDocs shadcn theme."""
        exit_code, output, project = run_mpm(
            "shadcn-project", "--monorepo", "--with-docs", "--docs-theme", "shadcn", "-y"
        )

        assert exit_code == 0
        assert (project / "mkdocs.yml").exists()

        mkdocs_content = (project / "mkdocs.yml").read_text()
        assert "shadcn" in mkdocs_content.lower()

    def test_monorepo_full_features(self, run_mpm):
        """Test monorepo with all features enabled."""
        exit_code, output, project = run_mpm(
            "full-project",
            "--monorepo",
            "--with-samples",
            "--with-docker",
            "--with-ci",
            "--with-pypi",
            "--with-docs",
            "-y"
        )

        assert exit_code == 0

        # All features present
        assert (project / "libs" / "greeter").is_dir()
        assert (project / "apps" / "printer").is_dir()
        assert (project / "docker-compose.yml").exists()
        assert (project / ".github" / "workflows" / "pr.yml").exists()
        assert (project / ".github" / "workflows" / "release.yml").exists()
        assert (project / "mkdocs.yml").exists()


class TestSinglePackageGeneration:
    """Test single package project generation."""

    def test_basic_single_package(self, run_mpm):
        """Test basic single package generation."""
        exit_code, output, project = run_mpm("single-project", "--single", "-y")

        assert exit_code == 0
        assert project.exists()
        assert (project / "pyproject.toml").exists()
        assert (project / "src" / "single_project" / "__init__.py").exists()
        assert (project / "src" / "single_project" / "py.typed").exists()

        # Should NOT have monorepo structure
        assert not (project / "libs").exists()
        assert not (project / "apps").exists()

    def test_single_package_with_docker(self, run_mpm):
        """Test single package with Docker."""
        exit_code, output, project = run_mpm(
            "docker-single", "--single", "--with-docker", "-y"
        )

        assert exit_code == 0
        assert (project / "Dockerfile").exists()
        assert (project / "docker-compose.yml").exists()


class TestPythonVersions:
    """Test different Python version configurations."""

    @pytest.mark.parametrize("version", ["3.11", "3.12", "3.13"])
    def test_python_versions(self, run_mpm, version):
        """Test generation with different Python versions."""
        exit_code, output, project = run_mpm(
            f"py{version.replace('.', '')}-project",
            "--monorepo",
            "--python", version,
            "-y"
        )

        assert exit_code == 0

        pyproject = (project / "pyproject.toml").read_text()
        assert f">={version}" in pyproject

        python_version_file = (project / ".python-version").read_text()
        assert version in python_version_file


class TestLicenses:
    """Test different license configurations."""

    @pytest.mark.parametrize("license_type,expected", [
        ("MIT", "MIT License"),
        ("Apache-2.0", "Apache License"),
        ("GPL-3.0", "GNU GENERAL PUBLIC LICENSE"),
    ])
    def test_license_types(self, run_mpm, license_type, expected):
        """Test generation with different licenses."""
        exit_code, output, project = run_mpm(
            f"{license_type.lower()}-project",
            "--monorepo",
            "--license", license_type,
            "-y"
        )

        assert exit_code == 0
        assert (project / "LICENSE").exists()

        license_content = (project / "LICENSE").read_text()
        assert expected in license_content

    def test_no_license(self, run_mpm):
        """Test generation without license."""
        exit_code, output, project = run_mpm(
            "no-license-project",
            "--monorepo",
            "--license", "none",
            "-y"
        )

        assert exit_code == 0
        assert not (project / "LICENSE").exists()


class TestNoGit:
    """Test --no-git flag."""

    def test_no_git_initialization(self, run_mpm):
        """Test that --no-git skips git init."""
        exit_code, output, project = run_mpm(
            "no-git-project", "--monorepo", "--no-git", "-y"
        )

        assert exit_code == 0
        assert not (project / ".git").exists()


class TestGeneratedFileContents:
    """Test that generated file contents are correct."""

    def test_pyproject_toml_content(self, run_mpm):
        """Verify pyproject.toml has correct structure."""
        exit_code, output, project = run_mpm(
            "content-test", "--monorepo", "--with-samples", "-y"
        )

        assert exit_code == 0

        # Root pyproject.toml
        root_pyproject = (project / "pyproject.toml").read_text()
        assert "[tool.uv.workspace]" in root_pyproject
        assert "[tool.una]" in root_pyproject
        assert "[tool.ruff]" in root_pyproject
        assert "[tool.pytest.ini_options]" in root_pyproject
        assert "[tool.poe.tasks]" in root_pyproject

        # Lib pyproject.toml
        lib_pyproject = (project / "libs" / "greeter" / "pyproject.toml").read_text()
        assert 'dynamic = ["una"]' in lib_pyproject
        assert "hatchling" in lib_pyproject
        assert "hatch-una" in lib_pyproject
        assert "[tool.hatch.build.hooks.una-build]" in lib_pyproject

    def test_namespace_consistency(self, run_mpm):
        """Verify namespace is consistent across all files."""
        exit_code, output, project = run_mpm(
            "my-namespace-test", "--monorepo", "--with-samples", "-y"
        )

        assert exit_code == 0

        # Namespace should be "my_namespace_test" (underscores)
        expected_namespace = "my_namespace_test"

        # Check root pyproject.toml
        root_pyproject = (project / "pyproject.toml").read_text()
        assert f'namespace = "{expected_namespace}"' in root_pyproject

        # Check directory structure
        assert (project / "libs" / "greeter" / expected_namespace / "greeter").is_dir()
```

#### 4.7 End-to-End Tests - Generated Projects Actually Work (`test_e2e.py`)

**CRITICAL**: These tests verify that generated projects can be installed and used.

```python
"""End-to-end tests - verify generated projects actually work."""

import subprocess
import sys
from pathlib import Path

import pytest


class TestGeneratedProjectsWork:
    """Test that generated projects can be installed and used."""

    @pytest.mark.slow
    def test_monorepo_uv_sync(self, run_mpm):
        """Test that generated monorepo can run 'uv sync'."""
        exit_code, output, project = run_mpm(
            "e2e-sync-test", "--monorepo", "--with-samples", "-y"
        )

        assert exit_code == 0

        # Run uv sync in the generated project
        result = subprocess.run(
            ["uv", "sync", "--all-packages"],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"uv sync failed: {result.stderr}"
        assert (project / "uv.lock").exists()

    @pytest.mark.slow
    def test_monorepo_lint_passes(self, run_mpm):
        """Test that generated code passes linting."""
        exit_code, output, project = run_mpm(
            "e2e-lint-test", "--monorepo", "--with-samples", "-y"
        )

        assert exit_code == 0

        # Install dependencies first
        subprocess.run(["uv", "sync", "--all-packages"], cwd=project, check=True)

        # Run ruff check
        result = subprocess.run(
            ["uv", "run", "ruff", "check", "."],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Linting failed: {result.stdout}\n{result.stderr}"

    @pytest.mark.slow
    def test_monorepo_type_check_passes(self, run_mpm):
        """Test that generated code passes type checking."""
        exit_code, output, project = run_mpm(
            "e2e-typecheck-test", "--monorepo", "--with-samples", "-y"
        )

        assert exit_code == 0

        subprocess.run(["uv", "sync", "--all-packages"], cwd=project, check=True)

        result = subprocess.run(
            ["uv", "run", "ty", "check"],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Type check failed: {result.stdout}\n{result.stderr}"

    @pytest.mark.slow
    def test_monorepo_tests_pass(self, run_mpm):
        """Test that generated project tests pass."""
        exit_code, output, project = run_mpm(
            "e2e-test-test", "--monorepo", "--with-samples", "-y"
        )

        assert exit_code == 0

        subprocess.run(["uv", "sync", "--all-packages"], cwd=project, check=True)

        result = subprocess.run(
            ["uv", "run", "pytest"],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Tests failed: {result.stdout}\n{result.stderr}"

    @pytest.mark.slow
    def test_monorepo_poe_all(self, run_mpm):
        """Test that 'poe all' passes (fmt, lint, check, test)."""
        exit_code, output, project = run_mpm(
            "e2e-poe-test", "--monorepo", "--with-samples", "-y"
        )

        assert exit_code == 0

        subprocess.run(["uv", "sync", "--all-packages"], cwd=project, check=True)

        result = subprocess.run(
            ["uv", "run", "poe", "all"],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"poe all failed: {result.stdout}\n{result.stderr}"

    @pytest.mark.slow
    def test_single_package_works(self, run_mpm):
        """Test that single package project works."""
        exit_code, output, project = run_mpm(
            "e2e-single-test", "--single", "-y"
        )

        assert exit_code == 0

        result = subprocess.run(
            ["uv", "sync"],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"uv sync failed: {result.stderr}"

    @pytest.mark.slow
    def test_lib_can_be_built(self, run_mpm):
        """Test that a generated lib can be built into a wheel."""
        exit_code, output, project = run_mpm(
            "e2e-build-test", "--monorepo", "--with-samples", "-y"
        )

        assert exit_code == 0

        subprocess.run(["uv", "sync", "--all-packages"], cwd=project, check=True)

        greeter_dir = project / "libs" / "greeter"
        result = subprocess.run(
            ["uv", "build"],
            cwd=greeter_dir,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Build failed: {result.stderr}"
        assert (greeter_dir / "dist").is_dir()


class TestAddPackageCommand:
    """Test 'mpm add' command for adding packages to existing projects."""

    @pytest.mark.slow
    def test_add_lib_to_existing_project(self, run_mpm, temp_dir):
        """Test adding a library to existing project."""
        # First create a project
        exit_code, output, project = run_mpm("add-test", "--monorepo", "-y")
        assert exit_code == 0

        # Now add a library
        import os
        from typer.testing import CliRunner
        from mpm.cli import app

        runner = CliRunner()
        os.chdir(project)

        result = runner.invoke(app, ["add", "lib", "auth"])

        assert result.exit_code == 0
        assert (project / "libs" / "auth").is_dir()
        assert (project / "libs" / "auth" / "pyproject.toml").exists()

    @pytest.mark.slow
    def test_add_app_with_docker(self, run_mpm, temp_dir):
        """Test adding an app with Docker support."""
        exit_code, output, project = run_mpm("add-app-test", "--monorepo", "-y")
        assert exit_code == 0

        import os
        from typer.testing import CliRunner
        from mpm.cli import app

        runner = CliRunner()
        os.chdir(project)

        result = runner.invoke(app, ["add", "app", "api", "--docker"])

        assert result.exit_code == 0
        assert (project / "apps" / "api").is_dir()
        assert (project / "apps" / "api" / "Dockerfile").exists()
```

#### 4.8 Test Configuration (`pyproject.toml` additions)

Add to `mpm/pyproject.toml`:

```toml
[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow (run with --slow)",
]

[tool.coverage.run]
source = ["src/mpm"]
omit = ["*/tests/*"]
```

#### 4.9 Running Tests During Development

**IMPORTANT**: Run tests continuously as you implement features.

```bash
# From mpm directory
cd mpm

# Run all fast tests (skip slow E2E tests)
uv run pytest -m "not slow"

# Run specific test file
uv run pytest tests/test_cli.py -v

# Run specific test
uv run pytest tests/test_integration.py::TestMonorepoGeneration::test_basic_monorepo -v

# Run with coverage
uv run pytest --cov=mpm --cov-report=term-missing -m "not slow"

# Run ALL tests including slow E2E tests
uv run pytest --slow

# Run tests and stop on first failure
uv run pytest -x

# Run tests with output visible
uv run pytest -s
```

#### 4.10 Manual Testing Workflow

During development, manually test the CLI in a temporary directory:

```bash
# Create a temp directory for testing
TEMP_TEST_DIR=$(mktemp -d)
cd "$TEMP_TEST_DIR"

# Test basic monorepo creation
uv run --directory /path/to/mpm mpm test-monorepo --monorepo -y
ls -la test-monorepo/

# Verify generated project works
cd test-monorepo
uv sync --all-packages
uv run poe all  # Should pass: fmt, lint, check, test

# Test with all features
cd "$TEMP_TEST_DIR"
uv run --directory /path/to/mpm mpm full-test \
    --monorepo \
    --with-samples \
    --with-docker \
    --with-ci \
    --with-pypi \
    --with-docs \
    -y

# Inspect the generated structure
tree full-test/ -a -I '.git|__pycache__|.venv'

# Clean up
rm -rf "$TEMP_TEST_DIR"
```

#### 4.11 Test Matrix Coverage

Ensure tests cover this configuration matrix:

| Dimension | Values to Test |
|-----------|---------------|
| **Structure** | `monorepo`, `single` |
| **Python** | `3.11`, `3.12`, `3.13` |
| **Samples** | `with-samples`, without |
| **Docker** | `with-docker`, without |
| **CI** | `with-ci`, without |
| **PyPI** | `with-pypi`, without |
| **Docs** | `with-docs` (material), `with-docs` (shadcn), without |
| **License** | `MIT`, `Apache-2.0`, `GPL-3.0`, `none` |
| **Git** | default (init), `--no-git` |

**Minimum required test scenarios:**
1. Basic monorepo (no extras)
2. Monorepo with all features
3. Monorepo with samples only
4. Single package basic
5. Single package with Docker
6. Each Python version
7. Each license type
8. No git initialization

### Phase 5: Build and Verify

```bash
# From the mpm directory
cd mpm

# Run full test suite
uv run pytest -v

# Run including slow E2E tests
uv run pytest --slow -v

# Build the wheel
uv build

# Verify templates are included in wheel
unzip -l dist/modern_python_monorepo-*.whl | grep templates

# Test installed CLI works
pip install dist/modern_python_monorepo-*.whl
mpm --help
mpm --version

# Final verification: create and test a project
TEMP_TEST_DIR=$(mktemp -d)
cd "$TEMP_TEST_DIR"
mpm final-test --monorepo --with-samples -y
cd final-test
uv sync --all-packages
uv run poe all  # Must pass!
```

### Implementation Checklist

#### Phase 1: Project Setup
- [ ] Create `mpm/` directory structure
- [ ] Create `mpm/pyproject.toml` with uv_build backend
- [ ] Add `mpm` to workspace in root `pyproject.toml`
- [ ] Run `uv sync` to verify workspace setup

#### Phase 2: Core Implementation
- [ ] Implement `src/mpm/__init__.py` (version)
- [ ] Implement `src/mpm/config.py` (Pydantic models)
- [ ] Implement `src/mpm/prompts.py` (Questionary prompts)
- [ ] Implement `src/mpm/cli.py` (Typer app)
- [ ] Implement `src/mpm/generators/__init__.py`
- [ ] Implement `src/mpm/generators/renderer.py`
- [ ] Implement `src/mpm/generators/project.py`
- [ ] Implement `src/mpm/generators/package.py`
- [ ] Implement `src/mpm/utils.py`

#### Phase 3: Template Files
- [ ] Create `src/mpm/templates/__init__.py`
- [ ] Create `templates/base/` (pyproject.toml.jinja, README.md.jinja, .gitignore, LICENSE.jinja, .python-version.jinja)
- [ ] Create `templates/monorepo/` (libs/, apps/ structures)
- [ ] Create `templates/single/` (src/ structure)
- [ ] Create `templates/docker/` (Dockerfile.jinja, docker-compose.yml.jinja, docker-bake.hcl.jinja, .dockerignore)
- [ ] Create `templates/ci/` (pr.yml.jinja, release.yml.jinja)
- [ ] Create `templates/docs/material/` (mkdocs.yml.jinja, docs structure)
- [ ] Create `templates/docs/shadcn/` (mkdocs.yml.jinja, docs structure)
- [ ] Create `templates/tooling/` (.pre-commit-config.yaml)
- [ ] Create `templates/samples/greeter/` (lib sample)
- [ ] Create `templates/samples/printer/` (app sample)

#### Phase 4: Testing (Run continuously!)
- [ ] Create `tests/__init__.py`
- [ ] Create `tests/conftest.py` (fixtures)
- [ ] Write `tests/test_config.py` (unit tests for Pydantic models)
- [ ] Write `tests/test_renderer.py` (unit tests for template rendering)
- [ ] Write `tests/test_cli.py` (CLI command tests)
- [ ] Write `tests/test_integration.py` (CLI with various configurations)
  - [ ] Test basic monorepo generation
  - [ ] Test monorepo with samples
  - [ ] Test monorepo with Docker
  - [ ] Test monorepo with CI
  - [ ] Test monorepo with PyPI
  - [ ] Test monorepo with docs (Material)
  - [ ] Test monorepo with docs (shadcn)
  - [ ] Test monorepo with all features
  - [ ] Test single package generation
  - [ ] Test single package with Docker
  - [ ] Test all Python versions (3.11, 3.12, 3.13)
  - [ ] Test all license types (MIT, Apache, GPL, none)
  - [ ] Test --no-git flag
  - [ ] Test generated file contents
  - [ ] Test namespace consistency
- [ ] Write `tests/test_e2e.py` (end-to-end tests)
  - [ ] Test generated monorepo runs `uv sync`
  - [ ] Test generated code passes linting
  - [ ] Test generated code passes type checking
  - [ ] Test generated project tests pass
  - [ ] Test `poe all` passes
  - [ ] Test single package works
  - [ ] Test lib can be built into wheel
  - [ ] Test `mpm add lib` command
  - [ ] Test `mpm add app --docker` command
- [ ] Run fast tests: `uv run pytest -m "not slow"`
- [ ] Run full test suite: `uv run pytest --slow`

#### Phase 5: Build and Verify
- [ ] Build wheel: `uv build`
- [ ] Verify templates in wheel: `unzip -l dist/*.whl | grep templates`
- [ ] Install wheel: `pip install dist/*.whl`
- [ ] Test installed CLI: `mpm --help && mpm --version`
- [ ] Final E2E test: Create project, run `uv sync`, run `poe all`

#### Manual Testing Checkpoints
- [ ] After Phase 2: `uv run mpm --help` works
- [ ] After Phase 3: `uv run mpm test --monorepo -y` creates project structure
- [ ] After Phase 3: Generated project passes `uv sync && poe all`
- [ ] After Phase 4: All tests pass
- [ ] After Phase 5: Installed CLI works end-to-end

### Reference: Existing Repository Files

Use these existing files as reference for template content:

| File | Use As Template For |
|------|---------------------|
| `/pyproject.toml` | `templates/base/pyproject.toml.jinja` (monorepo root) |
| `/libs/greeter/pyproject.toml` | `templates/monorepo/libs/__package__/pyproject.toml.jinja` |
| `/apps/printer/pyproject.toml` | `templates/monorepo/apps/__package__/pyproject.toml.jinja` |
| `/libs/greeter/modern_python_monorepo/greeter/__init__.py` | `templates/samples/greeter/__init__.py.jinja` |
| `/.github/workflows/*.yml` | `templates/ci/*.yml.jinja` |
| `/docker-compose.yml` | `templates/docker/docker-compose.yml.jinja` |
| `/docker-bake.hcl` | `templates/docker/docker-bake.hcl.jinja` |
| `/mkdocs.yml` | `templates/docs/shadcn/mkdocs.yml.jinja` |
| `/.pre-commit-config.yaml` | `templates/tooling/.pre-commit-config.yaml` |
| `/.gitignore` | `templates/base/.gitignore` |

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
