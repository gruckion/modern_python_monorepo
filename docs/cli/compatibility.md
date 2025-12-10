# Compatibility Rules

## Overview

The CLI validates option combinations to ensure generated projects work correctly. This page documents the key compatibility rules and restrictions.

## Project Structure

### Monorepo vs Single Package

| Option | `--monorepo` | `--single` |
|--------|--------------|------------|
| Workspace directories | `libs/`, `apps/` | None |
| `[tool.uv.workspace]` | Yes | No |
| Sample packages | Supported | Not applicable |
| Package addition | `mpm add lib/app` | Not supported |

### Flag Precedence

If both `--monorepo` and `--single` are specified, `--monorepo` takes precedence:

```bash
# Results in monorepo structure
mpm my-project --monorepo --single -y
```

### Default Structure

When neither flag is specified:

- **Interactive mode**: Prompts for selection
- **With `--yes`**: Defaults to `monorepo`

## Sample Packages

### Monorepo Only

The `--with-samples` flag only works with monorepo projects:

```bash
# ✅ Valid - monorepo with samples
mpm my-project --monorepo --with-samples -y

# ⚠️ Ignored - single package ignores --with-samples
mpm my-project --single --with-samples -y
```

### What Samples Include

| Package | Type | Description |
|---------|------|-------------|
| `libs/greeter` | Library | Simple greeting function |
| `apps/printer` | Application | CLI that uses the greeter library |

## Docker Configuration

### Monorepo Docker

Docker configuration in monorepos depends on whether apps exist:

| Scenario | Files Created |
|----------|---------------|
| No apps | `.dockerignore` only |
| Apps without Dockerfiles | `.dockerignore` only |
| Apps with Dockerfiles | `.dockerignore`, `docker-compose.yml`, `docker-bake.hcl` |

**With `--with-samples --with-docker`:**

```bash
mpm my-project --monorepo --with-samples --with-docker -y
```

Creates:

- `.dockerignore`
- `apps/printer/Dockerfile`
- `docker-compose.yml`
- `docker-bake.hcl`

**Without samples:**

```bash
mpm my-project --monorepo --with-docker -y
```

Creates:

- `.dockerignore` only

!!! tip
    Add apps with Docker support using `mpm add app <name> --docker`, then run `mpm add docker` to generate the orchestration files.

### Single Package Docker

Single package projects get full Docker configuration:

```bash
mpm my-lib --single --with-docker -y
```

Creates:

- `.dockerignore`
- `Dockerfile`
- `docker-compose.yml`
- `docker-bake.hcl`

### Adding Docker Later

When using `mpm add docker`:

| Project Type | Existing Apps with Dockerfiles | Result |
|--------------|-------------------------------|--------|
| Monorepo | None | `.dockerignore` only |
| Monorepo | One or more | Full Docker setup |
| Single | N/A | Full Docker setup |

## CI/CD Features

### PyPI Without CI

Adding PyPI publishing without CI works but shows a warning:

```bash
mpm my-project --with-pypi -y
# Warning: CI is not enabled. Consider adding CI first with 'mpm add ci'.
```

The release workflow will still be created, but you may want CI for pull request checks.

### Recommended Setup

For a complete CI/CD pipeline:

```bash
# At project creation
mpm my-project --monorepo --with-ci --with-pypi -y

# Or incrementally
mpm my-project --monorepo -y
cd my-project
mpm add ci
mpm add pypi
```

## Feature Commands

### mpm.toml Requirements

Feature addition commands require an `mpm.toml` configuration file:

| Command | Requires mpm.toml | Notes |
|---------|-------------------|-------|
| `mpm add lib` | No | Backward compatible |
| `mpm add app` | No | Backward compatible |
| `mpm add docker` | **Yes** | Updates `features.docker` |
| `mpm add ci` | **Yes** | Updates `features.ci` |
| `mpm add pypi` | **Yes** | Updates `features.pypi` |
| `mpm add docs` | **Yes** | Updates `features.docs` |

**Error when mpm.toml is missing:**

```
Error: No mpm.toml found. This command requires an mpm-managed project.
Create a new project with 'mpm new <name>' or add mpm.toml manually.
```

### Idempotency

Feature commands are idempotent - running them twice is safe:

```bash
mpm add docker  # Creates Docker files
mpm add docker  # "Docker is already enabled for this project."
```

## Package Addition

### Monorepo Only

Package addition only works in monorepo projects:

```bash
# ✅ Valid - in a monorepo
cd my-monorepo
mpm add lib auth
mpm add app api

# ❌ Error - in a single package project
cd my-single-package
mpm add lib utils
# Error: Not in a monorepo project.
```

### Backward Compatibility

`mpm add lib/app` works with projects created before `mpm.toml` was introduced:

| Configuration Source | Priority |
|---------------------|----------|
| `mpm.toml` | First (preferred) |
| `[tool.una]` in `pyproject.toml` | Fallback |

**What it reads:**

- **Namespace**: Python import namespace (e.g., `my_project`)
- **Python version**: For `requires-python` in new packages

## Documentation

### Theme Compatibility

Both themes work with all project types:

| Theme | Description | Works with |
|-------|-------------|------------|
| `material` | Material for MkDocs | Monorepo, Single |
| `shadcn` | Modern shadcn-inspired | Monorepo, Single |

### Dependencies Added

When docs are enabled, these are added to `pyproject.toml`:

```toml
[dependency-groups]
dev = [
    # ... existing deps
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",  # or mkdocs-shadcn for shadcn theme
]
```

## Common Error Messages

### "Not in an mpm project"

**Cause:** Running a command outside a project directory.

**Fix:** Navigate to your project root:

```bash
cd my-project
mpm add lib auth
```

### "No mpm.toml found"

**Cause:** Running a feature command in a project without `mpm.toml`.

**Fix:** Either:

1. Create a new project with `mpm new`
2. Manually create `mpm.toml` (see [mpm.toml documentation](../mpm-toml.md#creating-mpmtoml-for-old-projects))

### "Not in a monorepo project"

**Cause:** Running `mpm add lib/app` in a single package project.

**Fix:** Package addition is only for monorepos. For single packages, add code directly to `src/`.

### "Feature is already enabled"

**Cause:** Running a feature command for a feature that's already active.

**Result:** No action taken, just a warning. This is safe and expected behavior.

## Validation Order

The CLI validates compatibility in this order:

1. **Project detection**: Find project root via `mpm.toml` or `[tool.uv.workspace]`
2. **Structure validation**: Ensure command is valid for project type
3. **Configuration check**: Verify `mpm.toml` exists (for feature commands)
4. **Feature state**: Check if feature is already enabled
5. **Execution**: Generate files and update configuration

Understanding these rules helps you create valid configurations and troubleshoot issues when the CLI reports errors.
