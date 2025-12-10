# Commands

## Overview

The MPM CLI provides commands to create and manage Python monorepo projects.

## `mpm` (Default Command)

Creates a new MPM project interactively or with flags.

```bash
mpm [project-name] [options]
```

### Parameters

* `project-name` (optional): Name for your project directory

### Key Options

* `--yes, -y`: Use default configuration (skips prompts)
* `--monorepo, -m`: Create monorepo structure
* `--single, -s`: Create single package structure
* `--python, -p <version>`: Python version (`3.11`, `3.12`, `3.13`)
* `--with-samples`: Include sample packages (greeter lib, printer app)
* `--with-docker`: Include Docker configuration
* `--with-ci`: Include GitHub Actions CI workflow
* `--with-pypi`: Include PyPI publishing workflow
* `--with-docs`: Include MkDocs documentation
* `--docs-theme <theme>`: Docs theme (`material`, `shadcn`)
* `--license, -l <type>`: License (`MIT`, `Apache-2.0`, `GPL-3.0`, `none`)
* `--no-git`: Skip git initialization
* `--no-sync`: Skip running `uv sync` after generation

See the full reference in [Options](options.md).

### Examples

```bash
# Interactive mode - prompts for all options
mpm

# Quick setup with defaults
mpm my-project --yes

# Monorepo with samples and CI
mpm my-project --monorepo --with-samples --with-ci -y

# Single package project
mpm my-lib --single -y

# Full production setup
mpm my-api --monorepo --with-docker --with-ci --with-pypi --with-docs -y
```

## `new`

Creates a new project with an explicit name. Identical to the default command but requires a project name.

```bash
mpm new <project-name> [options]
```

### Parameters

* `project-name` (required): Name for your project directory

### Examples

```bash
# Create monorepo with name
mpm new my-project --monorepo -y

# Create single package
mpm new my-lib --single -y
```

## `add`

Adds packages or features to an existing MPM project.

```bash
mpm add [subcommand] [options]
```

When run without a subcommand, enters interactive mode to add a package.

### Subcommands

#### `add lib`

Adds a new library package to `libs/`.

```bash
mpm add lib <name> [options]
```

**Parameters:**

* `name` (required): Library name

**Options:**

* `--description, -d <text>`: Library description

**Example:**

```bash
mpm add lib auth
mpm add lib utils --description "Shared utilities"
```

#### `add app`

Adds a new application package to `apps/`.

```bash
mpm add app <name> [options]
```

**Parameters:**

* `name` (required): Application name

**Options:**

* `--description, -d <text>`: Application description
* `--docker`: Include Dockerfile for the application

**Example:**

```bash
mpm add app api
mpm add app worker --docker
mpm add app cli --description "Command-line interface"
```

#### `add docker`

Adds Docker configuration to an existing project.

```bash
mpm add docker
```

**What it creates:**

* `.dockerignore` - Always created
* For **single package** projects:
    * `Dockerfile`
    * `docker-compose.yml`
    * `docker-bake.hcl`
* For **monorepo** projects:
    * `docker-compose.yml` and `docker-bake.hcl` only if apps with Dockerfiles exist

**Example:**

```bash
cd my-project
mpm add docker
```

!!! note
    For monorepos, add apps with `mpm add app <name> --docker` first, then run `mpm add docker` to generate the compose files.

#### `add ci`

Adds GitHub Actions CI workflow to an existing project.

```bash
mpm add ci
```

**What it creates:**

* `.github/workflows/pr.yml` - Runs on pull requests with lint, type check, and tests

**Example:**

```bash
cd my-project
mpm add ci
```

#### `add pypi`

Adds PyPI publishing workflow to an existing project.

```bash
mpm add pypi
```

**What it creates:**

* `.github/workflows/release.yml` - Publishes to PyPI on GitHub releases

**Example:**

```bash
cd my-project
mpm add pypi
```

!!! warning
    If CI is not enabled, you'll see a warning. Consider adding CI first with `mpm add ci`.

#### `add docs`

Adds MkDocs documentation to an existing project.

```bash
mpm add docs [options]
```

**Options:**

* `--theme, -t <theme>`: Documentation theme (`material`, `shadcn`). Default: `material`

**What it creates:**

* `mkdocs.yml` - MkDocs configuration
* `docs/index.md` - Documentation home page
* Updates `pyproject.toml` with MkDocs dependencies and poe tasks

**Example:**

```bash
cd my-project
mpm add docs
mpm add docs --theme shadcn
```

### Interactive Mode

Running `mpm add` without a subcommand enters interactive mode:

```bash
cd my-project
mpm add
```

You'll be prompted to:

1. Choose package type (Library or Application)
2. Enter package name
3. Enter description (optional)
4. For apps: Include Docker support?

## Global Options

These options work with any command:

* `--help, -h`: Display help information
* `--version, -v`: Display CLI version

## Command Examples

### Create a Production-Ready Monorepo

```bash
mpm my-api \
  --monorepo \
  --with-samples \
  --with-docker \
  --with-ci \
  --with-pypi \
  --with-docs \
  --docs-theme material \
  -y
```

### Create Empty Monorepo, Add Features Later

```bash
# Create minimal monorepo
mpm my-project --monorepo -y

# Navigate to project
cd my-project

# Add features incrementally
mpm add docker
mpm add ci
mpm add pypi
mpm add docs --theme material
```

### Build a Microservices Monorepo

```bash
# Create monorepo
mpm platform --monorepo -y
cd platform

# Add shared libraries
mpm add lib common
mpm add lib auth
mpm add lib database

# Add services with Docker
mpm add app api --docker
mpm add app worker --docker
mpm add app scheduler --docker

# Add Docker orchestration
mpm add docker

# Add CI/CD
mpm add ci
mpm add pypi
```

### Create a Simple Library

```bash
# Single package for a standalone library
mpm my-lib --single -y
cd my-lib

# Add documentation
mpm add docs
```
