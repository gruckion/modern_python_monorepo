# Using the Interactive Prompts

## Overview

The CLI uses [questionary](https://questionary.readthedocs.io/) for interactive prompts. These prompts work in most terminals and are fully keyboard-driven.

## Core Keys

| Key | Action |
|-----|--------|
| Up/Down arrows | Navigate options |
| Enter | Confirm selection |
| Space | Toggle checkbox (multi-select) |
| Ctrl+C | Cancel and exit |

## Prompt Types

### Text Input

Used for entering free-form text like project names.

```
? Project name: █
```

- Type your answer and press **Enter**
- If validation fails, you'll see an error message; edit and press **Enter** again

**Where used:** Project name, package name, description

### Single Select

Choose one option from a list.

```
? Project structure: (Use arrow keys)
 ❯ Monorepo (libs/ and apps/ workspaces)
   Single package
```

- **Move** with Up/Down arrows
- **Enter** to confirm the highlighted option

**Where used:** Project structure, Python version, license type, documentation theme

### Checkbox (Multi-select)

Select multiple options from a list.

```
? Select features to include: (Press <space> to select, <enter> to confirm)
 ❯◉ Ruff (linting & formatting)
  ◉ ty (type checking)
  ◉ pytest (testing)
  ◉ poethepoet (task runner)
  ◉ Pre-commit hooks
  ◯ GitHub Actions CI
  ◯ PyPI publishing workflow
  ◯ Docker support
```

- **Move** with Up/Down arrows
- **Space** toggles the current item on (◉) or off (◯)
- **Enter** confirms your selection

**Where used:** Feature selection during project creation

### Confirm (Yes/No)

Binary choice prompts.

```
? Include sample packages?
 ❯ Yes (greeter lib + printer app)
   No (empty structure)
```

- **Move** with Up/Down arrows
- **Enter** to confirm

**Where used:** Sample packages, Docker support for apps

## Project Creation Flow

When you run `mpm` without flags, you'll go through these prompts:

### 1. Project Name

```
? Project name: my-awesome-project
```

Enter your project name. It will be converted to:

- **Slug** (URL-safe): `my-awesome-project`
- **Python identifier**: `my_awesome_project`

### 2. Project Structure

```
? Project structure:
 ❯ Monorepo (libs/ and apps/ workspaces)
   Single package
```

Choose between:

- **Monorepo**: Creates `libs/` and `apps/` workspace directories
- **Single package**: Creates a standalone Python package

### 3. Python Version

```
? Python version requirement:
   3.11+
   3.12+
 ❯ 3.13+
```

Sets the minimum Python version. Default is 3.13+.

### 4. Features

```
? Select features to include:
 ❯◉ Ruff (linting & formatting)
  ◉ ty (type checking)
  ◉ pytest (testing)
  ◉ poethepoet (task runner)
  ◉ Pre-commit hooks
  ◯ GitHub Actions CI
  ◯ PyPI publishing workflow
  ◯ Docker support
```

Core tools (Ruff, ty, pytest, poe, pre-commit) are selected by default. Optional features (CI, PyPI, Docker) are not.

### 5. Sample Packages (Monorepo only)

```
? Include sample packages?
 ❯ Yes (greeter lib + printer app)
   No (empty structure)
```

Only shown for monorepo projects. Creates example packages to demonstrate the structure.

### 6. Documentation

```
? Include documentation site (MkDocs)?
 ❯ Yes - Material theme (recommended)
   Yes - shadcn theme (modern UI)
   No
```

Choose whether to include MkDocs and which theme to use.

### 7. License

```
? License:
 ❯ MIT
   Apache-2.0
   GPL-3.0
   None
```

Select your project's license.

## Package Addition Flow

When you run `mpm add` without a subcommand:

### 1. Package Type

```
? Package type:
 ❯ Library (libs/)
   Application (apps/)
```

### 2. Package Name

```
? Package name: auth
```

### 3. Description

```
? Description (optional): Authentication utilities
```

### 4. Docker Support (Apps only)

```
? Include Docker support? (y/N)
```

Only shown when adding an application.

## When to Use Interactive Mode

**Use interactive mode when:**

- First-time users exploring options
- You're unsure of the exact flag names
- Complex configurations with many choices
- You want guidance through the setup process

**Use flags when:**

- CI/CD automation
- Reproducible project creation
- Scripts and tooling
- You know exactly what you want

## Skipping Prompts

### Skip All Prompts

Use `--yes` or `-y` to accept all defaults:

```bash
mpm my-project --yes
```

### Partial Interactive

Specify some options via flags, and only be prompted for the rest:

```bash
# Only prompted for features not specified
mpm my-project --monorepo --python 3.12
```

## Tips

### Cancel Safely

Press **Ctrl+C** at any prompt to cancel without creating files.

### Quick Navigation

In long lists, type the first letter of an option to jump to it (in some terminals).

### Default Selections

In checkbox prompts, items with ◉ are pre-selected. Press **Enter** to accept defaults without changing anything.

### Terminal Compatibility

If prompts don't render correctly:

- Ensure your terminal supports ANSI escape codes
- Try a different terminal emulator
- Use flag-based invocation instead: `mpm my-project --monorepo -y`
