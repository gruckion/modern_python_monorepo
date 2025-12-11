# MPM Configuration File & Feature Commands Implementation Plan

This document outlines the complete implementation plan for adding `mpm.toml` configuration file support and `mpm add` feature commands (docker, ci, pypi, docs) to the mpm-cli tool.

---

## Table of Contents

1. [Checklist](#checklist)
2. [Background & Motivation](#background--motivation)
3. [Research Summary](#research-summary)
4. [Root Detection Analysis](#root-detection-analysis)
5. [mpm.toml Schema Design](#mpmtoml-schema-design)
6. [Implementation Phases](#implementation-phases)
7. [File Changes](#file-changes)
8. [Testing Strategy](#testing-strategy)
9. [Edge Cases](#edge-cases)
10. [Verification Criteria](#verification-criteria)

---

## Checklist

### Phase 1: Core mpm.toml Infrastructure
- [x] Add `tomli-w>=1.0.0` dependency to `apps/mpm-cli/pyproject.toml`
- [x] Create `MpmConfig` Pydantic model in `config.py`
  - [x] Add `version` field (CLI version)
  - [x] Add `created_at` field (ISO timestamp)
  - [x] Add all project config fields
  - [x] Implement `from_project_config()` class method
  - [x] Implement `from_toml()` class method
  - [x] Implement `to_toml_dict()` method
- [x] Create `templates/base/mpm.toml.jinja` template
- [x] Update `utils.py`:
  - [x] Add `find_mpm_config()` function
  - [x] Update `find_project_root()` to check mpm.toml first, then `[tool.uv.workspace]`
  - [x] Add `load_mpm_config()` function
  - [x] Add `save_mpm_config()` function
- [x] Update `generators/project.py`:
  - [x] Generate mpm.toml in `_generate_base_files()`
- [x] Write tests:
  - [x] `test_config.py`: Test MpmConfig model
  - [x] `test_utils.py`: Test find/load/save functions
  - [x] `test_integration.py`: Test mpm.toml generation
- [x] Run tests and verify passing

### Phase 2: Enhance Existing Commands
- [x] Update `generators/package.py`:
  - [x] Read mpm.toml for context when adding packages
  - [x] Use mpm.toml values for python_version, namespace, etc.
- [x] Update `cli.py`:
  - [x] Update `add_lib()` to read mpm.toml context
  - [x] Update `add_app_cmd()` to read mpm.toml context
  - [x] Update `add_interactive()` to read mpm.toml context
- [x] Write tests:
  - [x] Test `mpm add lib` reads from mpm.toml
  - [x] Test `mpm add app` reads from mpm.toml
  - [x] Test backward compat: works without mpm.toml
- [x] Run tests and verify passing

### Phase 3: Add Docker Feature Command
- [x] Implement `mpm add docker` command in `cli.py`:
  - [x] Create `add_docker()` function
  - [x] Handle monorepo vs single package
  - [x] Handle monorepo with/without existing apps
- [x] Create `generators/features.py` module:
  - [x] Implement `add_docker_feature()` function
  - [x] Generate .dockerignore
  - [x] Generate Dockerfile (single package)
  - [x] Generate docker-compose.yml (when applicable)
  - [x] Generate docker-bake.hcl (when applicable)
- [x] Update mpm.toml after adding docker
- [x] Write tests:
  - [x] `test_cli.py`: Test `mpm add docker --help`
  - [x] `test_add_features.py`: Test docker file generation
  - [x] `test_integration.py`: Test docker files created correctly
  - [x] `test_e2e.py`: Test docker build works
- [x] Run tests and verify passing

### Phase 4: Add CI Feature Command
- [x] Implement `mpm add ci` command in `cli.py`:
  - [x] Create `add_ci()` function
- [x] Add to `generators/features.py`:
  - [x] Implement `add_ci_feature()` function
  - [x] Generate .github/workflows/pr.yml
- [x] Update mpm.toml after adding CI
- [x] Write tests:
  - [x] `test_cli.py`: Test `mpm add ci --help`
  - [x] `test_add_features.py`: Test CI workflow generation
  - [x] `test_integration.py`: Test workflow created correctly
  - [x] Verify YAML is valid
- [x] Run tests and verify passing

### Phase 5: Add PyPI Feature Command
- [x] Implement `mpm add pypi` command in `cli.py`:
  - [x] Create `add_pypi()` function
  - [x] Warn if CI not enabled
- [x] Add to `generators/features.py`:
  - [x] Implement `add_pypi_feature()` function
  - [x] Generate .github/workflows/release.yml
- [x] Update mpm.toml after adding PyPI
- [x] Write tests:
  - [x] `test_cli.py`: Test `mpm add pypi --help`
  - [x] `test_add_features.py`: Test release workflow generation
  - [x] `test_integration.py`: Test workflow created correctly
  - [x] Verify YAML is valid
- [x] Run tests and verify passing

### Phase 6: Add Docs Feature Command
- [x] Implement `mpm add docs` command in `cli.py`:
  - [x] Create `add_docs()` function
  - [x] Add `--theme` option (material/shadcn)
  - [x] Prompt for theme if not specified
- [x] Add to `generators/features.py`:
  - [x] Implement `add_docs_feature()` function
  - [x] Generate mkdocs.yml
  - [x] Create docs/index.md
- [x] Add to `utils.py`:
  - [x] Implement `update_pyproject_toml_for_docs()` function
  - [x] Add mkdocs dependencies to [dependency-groups.dev]
  - [x] Add poe tasks for docs
- [x] Update mpm.toml after adding docs
- [x] Run `uv sync` to install dependencies
- [x] Write tests:
  - [x] `test_cli.py`: Test `mpm add docs --help`
  - [x] `test_add_features.py`: Test docs generation
  - [x] `test_integration.py`: Test mkdocs.yml created correctly
  - [x] `test_e2e.py`: Test `mkdocs build` works
- [x] Run tests and verify passing

### Phase 7: Final Integration & E2E Testing
- [x] Write comprehensive E2E tests:
  - [x] Create project, add all features one by one
  - [x] Verify `uv sync --all-packages` works after each add
  - [x] Verify `uv run ruff check` passes
  - [x] Verify `uv run pytest` passes
- [x] Test backward compatibility:
  - [x] Old project without mpm.toml still works
  - [x] `mpm add lib/app` works on old projects
- [x] Test idempotency:
  - [x] Running `mpm add docker` twice doesn't break anything
- [x] Run full test suite
- [x] Manual testing with real project creation

### Documentation
- [x] Update README.md with new commands
- [x] Add examples for each `mpm add` command
- [x] Document mpm.toml schema

---

## Background & Motivation

### Current State
- mpm-cli generates Python monorepo projects with various optional features
- Features like `--with-docker`, `--with-ci`, `--with-pypi`, `--with-docs` are only available at project creation time
- Documentation claims users can "add these manually later" but there's no CLI support
- Project root detection uses `[tool.una]` in pyproject.toml, which is Una's config, not mpm's

### Goals
1. Create `mpm.toml` configuration file that stores all user choices
2. Enable `mpm add <feature>` commands to add features after project creation
3. Improve project root detection using mpm.toml
4. Maintain backward compatibility with existing projects

### Inspiration
Better T Stack uses `bts.jsonc` for similar purposes - storing scaffolding choices to enable the `bts add` command to understand existing configuration.

---

## Research Summary

### Better T Stack's bts.jsonc
- **Purpose**: Stores technology choices made during scaffolding
- **Location**: Project root (alongside package.json)
- **Format**: JSONC (JSON with comments)
- **Key Use Case**: Enables `bts add` to understand existing config
- **Philosophy**: "Keep it if you plan to use `bts add`"

### Current mpm-cli Architecture
- **Config Model**: `ProjectConfig` Pydantic model in `config.py`
- **Template System**: Jinja2 templates in `src/mpm/templates/`
- **CLI Framework**: Typer
- **Project Detection**: `find_project_root()` in `utils.py` checks for `[tool.una]`
- **Existing Commands**: `mpm new`, `mpm add lib`, `mpm add app`

---

## Root Detection Analysis

### Current Detection Method
```python
# utils.py:32-49
def find_project_root(start_path: Path | None = None) -> Path | None:
    """Find the project root by looking for pyproject.toml with workspace config."""
    path = start_path or Path.cwd()
    while path != path.parent:
        pyproject = path / "pyproject.toml"
        if pyproject.exists():
            try:
                with open(pyproject, "rb") as f:
                    config = tomllib.load(f)
                    # Check for una namespace config (indicating monorepo root)
                    if "tool" in config and "una" in config["tool"]:
                        return path
            except (tomllib.TOMLDecodeError, KeyError):
                pass
        path = path.parent
    return None
```

**Problem**: Uses `[tool.una]` which is Una's build config, not mpm's project marker.

### pyproject.toml Comparison

**Root pyproject.toml (workspace root):**
```toml
[tool.uv]
package = false

[tool.uv.workspace]
members = ["apps/*", "libs/*"]

[tool.una]
namespace = "my_project"
requires-python = ">=3.13"

[dependency-groups]
dev = [...]

[tool.poe.tasks]
...
```

**Package pyproject.toml (libs/apps):**
```toml
[project]
dynamic = ["una"]  # For hatch-una

[build-system]
requires = ["hatchling", "hatch-una"]
build-backend = "hatchling.build"

[tool.hatch.build.hooks.una-build]
[tool.hatch.metadata.hooks.una-meta]
```

### Key Distinguishing Markers

| Marker | Root | Package |
|--------|------|---------|
| `[tool.uv.workspace]` | ✅ | ❌ |
| `[tool.uv] package = false` | ✅ | ❌ |
| `[tool.una]` | ✅ | ❌ |
| `[dependency-groups]` | ✅ | ❌ |
| `dynamic = ["una"]` | ❌ | ✅ |
| `[tool.hatch.build.hooks.una-build]` | ❌ | ✅ |
| `[build-system] requires hatch-una` | ❌ | ✅ |

### Proposed Detection Strategy

```python
def find_project_root(start_path: Path | None = None) -> Path | None:
    """Find the project root by looking for mpm.toml or workspace config."""
    path = start_path or Path.cwd()

    while path != path.parent:
        # First priority: mpm.toml (mpm-managed project)
        if (path / "mpm.toml").exists():
            return path

        # Second priority: [tool.uv.workspace] (uv workspace root)
        pyproject = path / "pyproject.toml"
        if pyproject.exists():
            try:
                with open(pyproject, "rb") as f:
                    config = tomllib.load(f)
                    if "tool" in config and "uv" in config["tool"]:
                        if "workspace" in config["tool"]["uv"]:
                            return path
            except (tomllib.TOMLDecodeError, KeyError):
                pass

        path = path.parent

    return None
```

**Benefits:**
1. mpm.toml is authoritative for mpm-managed projects
2. Falls back to uv workspace config for backward compatibility
3. Works for both monorepo and single-package projects
4. Doesn't depend on Una-specific config

---

## mpm.toml Schema Design

### Format Choice: TOML (not JSONC)

| Factor | TOML | JSONC |
|--------|------|-------|
| Python ecosystem convention | ✅ pyproject.toml, setup.cfg | ❌ |
| Stdlib support | ✅ tomllib (3.11+) | ❌ |
| Native comments | ✅ | ✅ |
| Human readability | ✅ Cleaner syntax | ⚠️ Verbose |
| Consistency | ✅ Matches pyproject.toml | ❌ |

### Schema

```toml
# mpm.toml - Modern Python Monorepo Configuration
# This file stores your project scaffolding choices.
# Keep it to enable `mpm add` commands to understand your setup.
# Generated by mpm v0.1.0

[mpm]
version = "0.1.0"                    # CLI version that created project
created_at = "2024-12-09T10:30:00"   # ISO 8601 timestamp

[project]
name = "my_project"                  # Python identifier (underscores)
slug = "my-project"                  # URL-safe slug (hyphens)
description = "A modern Python project"

[generation]
structure = "monorepo"               # monorepo | single
python_version = "3.13"              # 3.11 | 3.12 | 3.13
license = "MIT"                      # MIT | Apache-2.0 | GPL-3.0 | none

[features]
samples = false                      # Include sample packages
docker = false                       # Docker configuration
ci = false                           # GitHub Actions CI
pypi = false                         # PyPI publishing workflow
docs = false                         # MkDocs documentation
docs_theme = "material"              # material | shadcn
precommit = true                     # Pre-commit hooks

[metadata]
author_name = ""
author_email = ""
github_owner = ""
github_repo = ""
```

### Template: `templates/base/mpm.toml.jinja`

```toml
# mpm.toml - Modern Python Monorepo Configuration
# This file stores your project scaffolding choices.
# Keep it to enable `mpm add` commands to understand your setup.
# Generated by mpm v{{ mpm_version }}

[mpm]
version = "{{ mpm_version }}"
created_at = "{{ created_at }}"

[project]
name = "{{ project_name }}"
slug = "{{ project_slug }}"
description = "{{ project_description }}"

[generation]
structure = "{{ structure.value }}"
python_version = "{{ python_version.value }}"
license = "{{ license_type.value }}"

[features]
samples = {{ with_samples | lower }}
docker = {{ with_docker | lower }}
ci = {{ with_ci | lower }}
pypi = {{ with_pypi | lower }}
docs = {{ with_docs | lower }}
docs_theme = "{{ docs_theme.value }}"
precommit = {{ with_precommit | lower }}

[metadata]
author_name = "{{ author_name }}"
author_email = "{{ author_email }}"
github_owner = "{{ github_owner }}"
github_repo = "{{ github_repo }}"
```

---

## Implementation Phases

### Phase 1: Core mpm.toml Infrastructure

**Goal**: Lay the foundation for mpm.toml support.

#### 1.1 Add Dependency

**File**: `apps/mpm-cli/pyproject.toml`

```toml
dependencies = [
    "typer>=0.12.0",
    "questionary>=2.1.0",
    "rich>=13.0.0",
    "jinja2>=3.1.0",
    "pydantic>=2.0.0",
    "tomli-w>=1.0.0",  # ADD: For writing TOML files
]
```

#### 1.2 Create MpmConfig Model

**File**: `apps/mpm-cli/src/mpm/config.py`

```python
from datetime import datetime

class MpmConfig(BaseModel):
    """Configuration stored in mpm.toml at project root."""

    # MPM metadata
    version: str = Field(default="0.1.0", description="CLI version that created project")
    created_at: datetime = Field(default_factory=datetime.now)

    # Project info
    project_name: str = Field(..., description="Python identifier name")
    project_slug: str = Field(..., description="URL-safe slug")
    project_description: str = Field(default="")

    # Generation settings
    structure: ProjectStructure = Field(default=ProjectStructure.MONOREPO)
    python_version: PythonVersion = Field(default=PythonVersion.PY313)
    license_type: LicenseType = Field(default=LicenseType.MIT)

    # Features
    with_samples: bool = Field(default=False)
    with_docker: bool = Field(default=False)
    with_ci: bool = Field(default=False)
    with_pypi: bool = Field(default=False)
    with_docs: bool = Field(default=False)
    docs_theme: DocsTheme = Field(default=DocsTheme.MATERIAL)
    with_precommit: bool = Field(default=True)

    # Metadata
    author_name: str = Field(default="")
    author_email: str = Field(default="")
    github_owner: str = Field(default="")
    github_repo: str = Field(default="")

    @classmethod
    def from_project_config(cls, config: ProjectConfig, version: str = "0.1.0") -> "MpmConfig":
        """Create MpmConfig from ProjectConfig."""
        return cls(
            version=version,
            created_at=datetime.now(),
            project_name=config.project_name,
            project_slug=config.project_slug,
            project_description=config.project_description,
            structure=config.structure,
            python_version=config.python_version,
            license_type=config.license_type,
            with_samples=config.with_samples,
            with_docker=config.with_docker,
            with_ci=config.with_ci,
            with_pypi=config.with_pypi,
            with_docs=config.with_docs,
            docs_theme=config.docs_theme,
            with_precommit=config.with_precommit,
            author_name=config.author_name,
            author_email=config.author_email,
            github_owner=config.github_owner,
            github_repo=config.github_repo,
        )

    @classmethod
    def from_toml(cls, path: Path) -> "MpmConfig":
        """Load MpmConfig from mpm.toml file."""
        import tomllib

        with open(path, "rb") as f:
            data = tomllib.load(f)

        # Flatten nested structure
        return cls(
            version=data.get("mpm", {}).get("version", "0.1.0"),
            created_at=datetime.fromisoformat(data.get("mpm", {}).get("created_at", datetime.now().isoformat())),
            project_name=data.get("project", {}).get("name", ""),
            project_slug=data.get("project", {}).get("slug", ""),
            project_description=data.get("project", {}).get("description", ""),
            structure=ProjectStructure(data.get("generation", {}).get("structure", "monorepo")),
            python_version=PythonVersion(data.get("generation", {}).get("python_version", "3.13")),
            license_type=LicenseType(data.get("generation", {}).get("license", "MIT")),
            with_samples=data.get("features", {}).get("samples", False),
            with_docker=data.get("features", {}).get("docker", False),
            with_ci=data.get("features", {}).get("ci", False),
            with_pypi=data.get("features", {}).get("pypi", False),
            with_docs=data.get("features", {}).get("docs", False),
            docs_theme=DocsTheme(data.get("features", {}).get("docs_theme", "material")),
            with_precommit=data.get("features", {}).get("precommit", True),
            author_name=data.get("metadata", {}).get("author_name", ""),
            author_email=data.get("metadata", {}).get("author_email", ""),
            github_owner=data.get("metadata", {}).get("github_owner", ""),
            github_repo=data.get("metadata", {}).get("github_repo", ""),
        )

    def to_toml_dict(self) -> dict:
        """Convert to TOML-friendly nested dict structure."""
        return {
            "mpm": {
                "version": self.version,
                "created_at": self.created_at.isoformat(),
            },
            "project": {
                "name": self.project_name,
                "slug": self.project_slug,
                "description": self.project_description,
            },
            "generation": {
                "structure": self.structure.value,
                "python_version": self.python_version.value,
                "license": self.license_type.value,
            },
            "features": {
                "samples": self.with_samples,
                "docker": self.with_docker,
                "ci": self.with_ci,
                "pypi": self.with_pypi,
                "docs": self.with_docs,
                "docs_theme": self.docs_theme.value,
                "precommit": self.with_precommit,
            },
            "metadata": {
                "author_name": self.author_name,
                "author_email": self.author_email,
                "github_owner": self.github_owner,
                "github_repo": self.github_repo,
            },
        }
```

#### 1.3 Update Utils

**File**: `apps/mpm-cli/src/mpm/utils.py`

```python
import tomli_w

def find_mpm_config(start_path: Path | None = None) -> Path | None:
    """Find mpm.toml by walking up directory tree."""
    path = start_path or Path.cwd()

    while path != path.parent:
        mpm_toml = path / "mpm.toml"
        if mpm_toml.exists():
            return mpm_toml
        path = path.parent

    return None


def find_project_root(start_path: Path | None = None) -> Path | None:
    """Find the project root by looking for mpm.toml or workspace config."""
    path = start_path or Path.cwd()

    while path != path.parent:
        # First priority: mpm.toml (mpm-managed project)
        if (path / "mpm.toml").exists():
            return path

        # Second priority: [tool.uv.workspace] (uv workspace root)
        pyproject = path / "pyproject.toml"
        if pyproject.exists():
            try:
                with open(pyproject, "rb") as f:
                    config = tomllib.load(f)
                    if "tool" in config and "uv" in config["tool"]:
                        if "workspace" in config["tool"]["uv"]:
                            return path
            except (tomllib.TOMLDecodeError, KeyError):
                pass

        path = path.parent

    return None


def load_mpm_config(path: Path) -> "MpmConfig":
    """Load and parse mpm.toml file into MpmConfig."""
    from mpm.config import MpmConfig
    return MpmConfig.from_toml(path)


def save_mpm_config(config: "MpmConfig", path: Path) -> None:
    """Write MpmConfig to mpm.toml file."""
    # Generate header comment
    header = """# mpm.toml - Modern Python Monorepo Configuration
# This file stores your project scaffolding choices.
# Keep it to enable `mpm add` commands to understand your setup.

"""

    toml_dict = config.to_toml_dict()
    toml_content = tomli_w.dumps(toml_dict)

    path.write_text(header + toml_content)
```

#### 1.4 Update Project Generator

**File**: `apps/mpm-cli/src/mpm/generators/project.py`

```python
def _generate_base_files(renderer: TemplateRenderer, output: Path, ctx: dict) -> None:
    """Generate base project files."""
    from mpm import __version__

    # Add mpm version and timestamp to context
    ctx["mpm_version"] = __version__
    ctx["created_at"] = datetime.now().isoformat()

    # Generate mpm.toml FIRST (stores configuration)
    renderer.render_to_file("base/mpm.toml.jinja", output / "mpm.toml", ctx)

    # ... rest of existing base files generation
    renderer.render_to_file("base/pyproject.toml.jinja", output / "pyproject.toml", ctx)
    # ...
```

### Phase 2: Enhance Existing Commands

**Goal**: Make existing `mpm add lib/app` commands use mpm.toml for context.

#### 2.1 Update Package Generator

**File**: `apps/mpm-cli/src/mpm/generators/package.py`

Update `add_package()` to read from mpm.toml:

```python
def add_package(
    name: str,
    package_type: str,
    description: str = "",
    with_docker: bool = False,
    project_root: Path | None = None,
    namespace: str | None = None,  # Make optional, read from mpm.toml
) -> None:
    """Add a new package to an existing project."""
    from mpm.config import MpmConfig, PythonVersion
    from mpm.utils import find_mpm_config, load_mpm_config

    renderer = TemplateRenderer()
    root = project_root or Path.cwd()

    # Try to load mpm.toml for context
    mpm_config_path = find_mpm_config(root)
    mpm_config: MpmConfig | None = None

    if mpm_config_path:
        mpm_config = load_mpm_config(mpm_config_path)
        namespace = namespace or mpm_config.project_name
        python_version = mpm_config.python_version
    else:
        # Fallback: Read from .python-version and pyproject.toml
        namespace = namespace or get_namespace_from_project(root) or "my_project"
        python_version = _read_python_version_from_file(root)

    ctx = {
        "package_name": name,
        "package_description": description or f"{name.capitalize()} package",
        "namespace": namespace,
        "python_version": python_version,
        "with_docker": with_docker,
    }

    if package_type == "lib":
        generate_lib_package(renderer, root, name, namespace, ctx)
    else:
        generate_app_package(renderer, root, name, namespace, ctx, with_docker=with_docker)

    console.print("\n[dim]Run 'uv sync --all-packages' to update dependencies[/dim]")
```

### Phase 3: Add Docker Feature Command

**Goal**: Implement `mpm add docker` command.

#### 3.1 CLI Command

**File**: `apps/mpm-cli/src/mpm/cli.py`

```python
@add_app.command("docker")
def add_docker() -> None:
    """Add Docker configuration to an existing project."""
    from mpm.generators.features import add_docker_feature
    from mpm.utils import find_mpm_config, find_project_root, load_mpm_config, save_mpm_config

    project_root = find_project_root()
    if not project_root:
        console.print("[red]Error:[/red] Not in an mpm project. Run from a project root.")
        raise typer.Exit(1)

    mpm_config_path = find_mpm_config(project_root)
    if not mpm_config_path:
        console.print("[yellow]Warning:[/yellow] No mpm.toml found. Creating one from project structure.")
        # Create mpm.toml from existing project (implementation needed)
        raise typer.Exit(1)

    mpm_config = load_mpm_config(mpm_config_path)

    if mpm_config.with_docker:
        console.print("[yellow]Docker is already enabled for this project.[/yellow]")
        return

    add_docker_feature(project_root, mpm_config)

    # Update mpm.toml
    mpm_config.with_docker = True
    save_mpm_config(mpm_config, mpm_config_path)

    console.print("[green]✓[/green] Added Docker configuration")
```

#### 3.2 Feature Generator

**File**: `apps/mpm-cli/src/mpm/generators/features.py` (NEW)

```python
"""Feature generators for adding features to existing projects."""

from pathlib import Path

from rich.console import Console

from mpm.config import MpmConfig, ProjectStructure
from mpm.generators.renderer import TemplateRenderer

console = Console()


def add_docker_feature(project_root: Path, config: MpmConfig) -> None:
    """Add Docker configuration to an existing project."""
    renderer = TemplateRenderer()

    ctx = {
        "project_slug": config.project_slug,
        "namespace": config.project_name,
        "python_version": config.python_version,
        "structure": config.structure,
        "with_samples": config.with_samples,
        "github_owner": config.github_owner,
    }

    # Always generate .dockerignore
    renderer.copy_static("docker/.dockerignore", project_root / ".dockerignore")
    console.print("[dim]Created .dockerignore[/dim]")

    if config.structure == ProjectStructure.SINGLE:
        # Single package: generate Dockerfile at root
        renderer.render_to_file("docker/Dockerfile.jinja", project_root / "Dockerfile", ctx)
        renderer.render_to_file("docker/docker-compose.yml.jinja", project_root / "docker-compose.yml", ctx)
        renderer.render_to_file("docker/docker-bake.hcl.jinja", project_root / "docker-bake.hcl", ctx)
        console.print("[dim]Created Dockerfile, docker-compose.yml, docker-bake.hcl[/dim]")
    else:
        # Monorepo: check for existing apps with Dockerfiles
        apps_dir = project_root / "apps"
        apps_with_docker = []

        if apps_dir.exists():
            for app_dir in apps_dir.iterdir():
                if app_dir.is_dir() and (app_dir / "Dockerfile").exists():
                    apps_with_docker.append(app_dir.name)

        if apps_with_docker:
            # Generate docker-compose.yml and docker-bake.hcl referencing existing apps
            ctx["apps_with_docker"] = apps_with_docker
            renderer.render_to_file("docker/docker-compose.yml.jinja", project_root / "docker-compose.yml", ctx)
            renderer.render_to_file("docker/docker-bake.hcl.jinja", project_root / "docker-bake.hcl", ctx)
            console.print(f"[dim]Created docker-compose.yml, docker-bake.hcl for apps: {apps_with_docker}[/dim]")
        else:
            console.print("[yellow]Note:[/yellow] No apps with Dockerfiles found.")
            console.print("[dim]Add apps with 'mpm add app <name> --docker' to generate docker-compose.yml[/dim]")


def add_ci_feature(project_root: Path, config: MpmConfig) -> None:
    """Add GitHub Actions CI to an existing project."""
    renderer = TemplateRenderer()

    ctx = {
        "structure": config.structure,
    }

    workflows_dir = project_root / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    renderer.render_to_file("ci/pr.yml.jinja", workflows_dir / "pr.yml", ctx)
    console.print("[dim]Created .github/workflows/pr.yml[/dim]")


def add_pypi_feature(project_root: Path, config: MpmConfig) -> None:
    """Add PyPI publishing workflow to an existing project."""
    renderer = TemplateRenderer()

    ctx = {
        "structure": config.structure,
        "with_samples": config.with_samples,
    }

    workflows_dir = project_root / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    renderer.render_to_file("ci/release.yml.jinja", workflows_dir / "release.yml", ctx)
    console.print("[dim]Created .github/workflows/release.yml[/dim]")


def add_docs_feature(project_root: Path, config: MpmConfig, theme: str = "material") -> None:
    """Add MkDocs documentation to an existing project."""
    import subprocess

    from mpm.config import DocsTheme
    from mpm.utils import update_pyproject_toml_for_docs

    renderer = TemplateRenderer()
    docs_theme = DocsTheme(theme)

    ctx = {
        "project_slug": config.project_slug,
        "project_description": config.project_description,
        "github_owner": config.github_owner,
    }

    # Update pyproject.toml with docs dependencies and poe tasks
    update_pyproject_toml_for_docs(project_root, docs_theme)
    console.print("[dim]Updated pyproject.toml with docs dependencies[/dim]")

    # Run uv sync to install dependencies
    console.print("[dim]Running uv sync to install dependencies...[/dim]")
    subprocess.run(["uv", "sync", "--quiet"], cwd=project_root, capture_output=True)

    # Generate mkdocs.yml
    theme_dir = f"docs/{docs_theme.value}"
    renderer.render_to_file(f"{theme_dir}/mkdocs.yml.jinja", project_root / "mkdocs.yml", ctx)
    console.print("[dim]Created mkdocs.yml[/dim]")

    # Create docs/index.md
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)

    index_content = f"""# Welcome to {config.project_slug}

{config.project_description or "Documentation for " + config.project_slug}

## Getting Started

TODO: Add getting started guide.
"""
    (docs_dir / "index.md").write_text(index_content)
    console.print("[dim]Created docs/index.md[/dim]")
```

### Phase 4-6: Add CI, PyPI, Docs Commands

Similar pattern to Docker command. See CLI command structure in Phase 3.

---

## File Changes

### New Files

| File | Purpose |
|------|---------|
| `templates/base/mpm.toml.jinja` | Jinja2 template for mpm.toml |
| `generators/features.py` | Feature generators for add commands |
| `tests/test_utils.py` | Tests for utility functions |
| `tests/test_mpm_toml.py` | Tests for mpm.toml functionality |
| `tests/test_add_features.py` | Tests for mpm add commands |

### Modified Files

| File | Changes |
|------|---------|
| `pyproject.toml` | Add tomli-w dependency |
| `config.py` | Add MpmConfig model |
| `utils.py` | Add find/load/save functions, update find_project_root() |
| `cli.py` | Add docker, ci, pypi, docs subcommands |
| `generators/project.py` | Generate mpm.toml in _generate_base_files() |
| `generators/package.py` | Read mpm.toml for context |
| `tests/test_cli.py` | Add help tests for new commands |
| `tests/test_config.py` | Add MpmConfig tests |
| `tests/test_integration.py` | Add feature generation tests |
| `tests/test_e2e.py` | Add E2E tests for features |

---

## Testing Strategy

### Unit Tests

**test_config.py (extend):**
```python
def test_mpm_config_defaults() -> None:
    """Test MpmConfig with minimal required fields."""

def test_mpm_config_from_project_config() -> None:
    """Test creating MpmConfig from ProjectConfig."""

def test_mpm_config_from_toml() -> None:
    """Test loading MpmConfig from TOML file."""

def test_mpm_config_to_toml_dict() -> None:
    """Test converting MpmConfig to TOML dict."""

def test_mpm_config_round_trip() -> None:
    """Test round-trip serialization."""
```

**test_utils.py (new):**
```python
def test_find_mpm_config_exists() -> None:
    """Test finding mpm.toml when it exists."""

def test_find_mpm_config_not_exists() -> None:
    """Test finding mpm.toml when it doesn't exist."""

def test_find_project_root_with_mpm_toml() -> None:
    """Test project root detection via mpm.toml."""

def test_find_project_root_with_workspace() -> None:
    """Test project root detection via [tool.uv.workspace]."""

def test_find_project_root_prefers_mpm_toml() -> None:
    """Test that mpm.toml takes precedence."""

def test_load_mpm_config() -> None:
    """Test loading mpm.toml."""

def test_save_mpm_config() -> None:
    """Test saving mpm.toml."""
```

### CLI Tests

**test_cli.py (extend):**
```python
def test_add_docker_help(cli_runner: CliRunner) -> None:
    """Test mpm add docker --help."""

def test_add_ci_help(cli_runner: CliRunner) -> None:
    """Test mpm add ci --help."""

def test_add_pypi_help(cli_runner: CliRunner) -> None:
    """Test mpm add pypi --help."""

def test_add_docs_help(cli_runner: CliRunner) -> None:
    """Test mpm add docs --help."""
```

### Integration Tests

**test_integration.py (extend):**
```python
class TestMpmTomlGeneration:
    """Test mpm.toml generation."""

    def test_mpm_toml_generated(self, run_mpm: Any) -> None:
        """Test that mpm.toml is generated."""

    def test_mpm_toml_content(self, run_mpm: Any) -> None:
        """Test mpm.toml content matches config."""

class TestAddFeatureCommands:
    """Test mpm add feature commands."""

    def test_add_docker_to_monorepo(self, run_mpm: Any) -> None:
        """Test adding docker to monorepo."""

    def test_add_ci_to_project(self, run_mpm: Any) -> None:
        """Test adding CI to project."""

    def test_add_pypi_to_project(self, run_mpm: Any) -> None:
        """Test adding PyPI workflow."""

    def test_add_docs_to_project(self, run_mpm: Any) -> None:
        """Test adding docs to project."""
```

### E2E Tests

**test_e2e.py (extend):**
```python
class TestAddFeaturesE2E:
    """E2E tests for mpm add feature commands."""

    @pytest.mark.slow
    def test_add_docker_then_build(self, run_mpm: Any) -> None:
        """Test adding docker and building."""

    @pytest.mark.slow
    def test_add_docs_then_build(self, run_mpm: Any) -> None:
        """Test adding docs and running mkdocs build."""

    @pytest.mark.slow
    def test_add_all_features_sequentially(self, run_mpm: Any) -> None:
        """Test adding all features one by one."""

class TestBackwardCompatibility:
    """Test backward compatibility with old projects."""

    @pytest.mark.slow
    def test_add_lib_without_mpm_toml(self, run_mpm: Any) -> None:
        """Test adding lib to project without mpm.toml."""
```

---

## Edge Cases

| Edge Case | Handling |
|-----------|----------|
| Project without mpm.toml | Fall back to [tool.uv.workspace] detection |
| Single package project | Different docker file locations |
| Monorepo without apps | Docker add warns, only creates .dockerignore |
| Feature already enabled | Idempotent - warn and skip |
| Missing pyproject.toml | Error with helpful message |
| Corrupted mpm.toml | Error with helpful message |
| Running from subdirectory | find_project_root() walks up |
| pypi without ci | Warn but allow |

---

## Verification Criteria

### After Each Phase

1. All existing tests still pass
2. New tests pass
3. `uv sync --all-packages` works on generated projects
4. `uv run ruff check .` passes on generated code
5. `uv run pytest` passes on generated projects

### Final Verification

1. Create new project: `mpm new test-project --monorepo -y`
2. Verify mpm.toml created with correct content
3. Add features one by one:
   ```bash
   cd test-project
   mpm add docker
   mpm add ci
   mpm add pypi
   mpm add docs --theme material
   ```
4. Verify each feature works:
   - Docker: `docker compose build` (if apps exist)
   - CI: YAML is valid
   - PyPI: YAML is valid
   - Docs: `uv run mkdocs build`
5. Verify `uv sync --all-packages` still works
6. Verify `uv run poe all` passes

---

## Notes

### Why TOML over JSONC

1. Python ecosystem convention (pyproject.toml)
2. Native stdlib support (tomllib in 3.11+)
3. Cleaner syntax for configuration
4. Consistent with existing project files

### pyproject.toml Modification Strategy

For `mpm add docs`, we need to modify pyproject.toml to add dependencies and poe tasks. Options:

1. **String manipulation** - Fragile but preserves comments
2. **tomli-w** - Clean but loses comments
3. **Hybrid** - Use tomli-w, regenerate from template

**Chosen approach**: Use tomli-w. Comments in generated pyproject.toml are not critical since it's template-based. Add note in mpm.toml about modifications.

### Backward Compatibility

Projects created before mpm.toml was implemented will continue to work:
- `find_project_root()` falls back to [tool.uv.workspace] check
- `mpm add lib/app` works with or without mpm.toml
- New features require mpm.toml (can be generated from existing project)
