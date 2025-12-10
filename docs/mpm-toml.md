# mpm.toml Configuration

## Overview

When you create a project with `mpm`, it generates an `mpm.toml` file at the project root. This file stores your project configuration and enables `mpm add` feature commands to work correctly.

## What is mpm.toml?

`mpm.toml` serves two purposes:

1. **Project Marker**: Identifies the directory as an MPM-managed project root
2. **Configuration Store**: Remembers your scaffolding choices so `mpm add` commands can maintain consistency

## Schema

```toml
[mpm]
version = "0.1.0"                    # CLI version that created the project
created_at = "2024-01-15T10:30:00"   # ISO 8601 timestamp

[project]
name = "my_project"                  # Python identifier (underscores)
slug = "my-project"                  # URL-safe slug (hyphens)
description = ""                     # Project description

[generation]
structure = "monorepo"               # monorepo | single
python_version = "3.13"              # 3.11 | 3.12 | 3.13
license = "MIT"                      # MIT | Apache-2.0 | GPL-3.0 | none

[features]
samples = false                      # Include sample packages
docker = false                       # Docker configuration enabled
ci = false                           # GitHub Actions CI enabled
pypi = false                         # PyPI publishing enabled
docs = false                         # MkDocs documentation enabled
docs_theme = "material"              # material | shadcn
precommit = true                     # Pre-commit hooks enabled

[metadata]
author_name = ""                     # Author name
author_email = ""                    # Author email
github_owner = ""                    # GitHub username/org
github_repo = ""                     # GitHub repository name
```

## How It Works

### Project Creation

When you run `mpm new my-project --monorepo --with-ci -y`, the generated `mpm.toml` captures these choices:

```toml
[generation]
structure = "monorepo"

[features]
ci = true
```

### Adding Packages

When you run `mpm add lib auth`, the command reads `mpm.toml` to determine:

- **Namespace**: Uses `project.name` for the Python import namespace
- **Python Version**: Uses `generation.python_version` for `requires-python`

This ensures new packages match your project's configuration.

### Adding Features

When you run `mpm add docker`, the command:

1. Reads current configuration from `mpm.toml`
2. Generates appropriate files based on `generation.structure`
3. Updates `features.docker = true` in `mpm.toml`

Running the same command again will see `docker = true` and skip with a warning.

## Example

After creating a project and adding features:

```bash
mpm new my-api --monorepo --python 3.12 -y
cd my-api
mpm add ci
mpm add docker
mpm add docs --theme shadcn
```

Your `mpm.toml` will look like:

```toml
[mpm]
version = "0.1.0"
created_at = "2024-12-09T14:30:00"

[project]
name = "my_api"
slug = "my-api"
description = ""

[generation]
structure = "monorepo"
python_version = "3.12"
license = "MIT"

[features]
samples = false
docker = true
ci = true
pypi = false
docs = true
docs_theme = "shadcn"
precommit = true

[metadata]
author_name = ""
author_email = ""
github_owner = ""
github_repo = ""
```

## Manual Editing

You can safely edit `mpm.toml` manually. Common reasons to edit:

- **Update metadata**: Add author info, GitHub details
- **Change description**: Update project description
- **Correct settings**: Fix any values that don't match your setup

Changes are reflected in subsequent `mpm add` commands.

!!! warning
    Don't change `generation.structure` after creating the project. The file structure won't be modified to match.

## Feature Command Requirements

| Command | Requires mpm.toml |
|---------|-------------------|
| `mpm add lib` | No (backward compatible) |
| `mpm add app` | No (backward compatible) |
| `mpm add docker` | **Yes** |
| `mpm add ci` | **Yes** |
| `mpm add pypi` | **Yes** |
| `mpm add docs` | **Yes** |

## Backward Compatibility

Projects created before `mpm.toml` was introduced still work:

- **`mpm add lib/app`**: Falls back to reading namespace from `[tool.una]` in `pyproject.toml`
- **Feature commands**: Require `mpm.toml` - create one manually or regenerate the project

### Creating mpm.toml for Old Projects

If you have an existing project without `mpm.toml`, create one manually:

```toml
[mpm]
version = "0.1.0"
created_at = "2024-01-01T00:00:00"

[project]
name = "your_project_name"
slug = "your-project-name"
description = ""

[generation]
structure = "monorepo"
python_version = "3.13"
license = "MIT"

[features]
samples = false
docker = false
ci = false
pypi = false
docs = false
docs_theme = "material"
precommit = true

[metadata]
author_name = ""
author_email = ""
github_owner = ""
github_repo = ""
```

Adjust values to match your existing setup, then `mpm add` feature commands will work.

## Why TOML?

MPM uses TOML (not JSON or YAML) because:

- **Python convention**: Matches `pyproject.toml`
- **Native support**: Python 3.11+ includes `tomllib` in stdlib
- **Clean syntax**: More readable than JSON for configuration
- **Comments**: Supports inline documentation
