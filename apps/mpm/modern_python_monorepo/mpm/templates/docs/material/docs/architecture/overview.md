# Architecture Overview

## Monorepo Structure

```
project/
├── pyproject.toml          # Workspace root + tool config
├── uv.lock                 # Single lockfile
├── apps/                   # Runnable applications
│   └── <app>/
│       ├── pyproject.toml
│       └── <namespace>/<app>/
└── libs/                   # Reusable libraries
    └── <lib>/
        ├── pyproject.toml
        └── <namespace>/<lib>/
```

## Key Concepts

### Workspace

The root `pyproject.toml` defines the workspace:

```toml
[tool.uv.workspace]
members = ["apps/*", "libs/*"]
```

### Namespace Packages

All packages use a shared namespace to avoid import collisions:

```python
from <namespace>.<package> import something
```

### Internal Dependencies

Apps can depend on libs using workspace references:

```toml
[project]
dependencies = ["some-lib"]

[tool.uv.sources.some-lib]
workspace = true
```

## Dependency Flow

```
apps/printer → libs/greeter → cowsay-python (PyPI)
```

Libraries are reusable. Applications are runnable.
