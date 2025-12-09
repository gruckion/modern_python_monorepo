# MPM CLI Technology Choices

This document outlines the opinionated technology choices made for the Modern Python Monorepo (MPM) CLI scaffolding tool and justifies each selection over its alternatives.

## Technology Stack Overview

| Category | Chosen | Alternatives |
|----------|--------|--------------|
| Package/Dependency Manager | **uv** | pip, poetry, pdm, pipenv, pyenv |
| Linting & Formatting | **Ruff** | black, isort, flake8, pylint, autopep8, yapf |
| Pre-commit Hooks | **prek** | pre-commit |
| Testing | **pytest** | unittest, nose, nose2 |
| Documentation | **MkDocs** | Sphinx, pdoc, pydoc |
| Type Checking | **ty** | mypy, pyright, pytype, pyre |
| Project Configuration | **pyproject.toml** | requirements.txt, setup.py, setup.cfg |
| Docker Builds | **docker-bake** | docker-compose build, docker build, kaniko |
| Task Runner | **Poe the Poet** | Makefile, invoke, tox, nox, just |
| Build Backend | **hatchling/uv build** | flit, setuptools, pdm-backend |
| Monorepo Tool | **una** | pants, bazel, nx |

---

## 1. Package Manager: uv

**Chosen:** uv (Astral)

### Alternatives:
- pip + venv
- poetry
- pdm
- pipenv
- pyenv (Python version management)

### Justification:

**Performance (10-100x faster)**: uv is written in Rust by Astral (the same team behind Ruff). Benchmarks consistently show 10-100x speed improvements over pip for dependency resolution and installation. This is achieved through Rust's memory safety and zero-cost abstractions, parallel downloads/installations, aggressive caching, and an efficient dependency resolution algorithm. For monorepos with dozens of packages, this speed difference is critical for CI/CD pipelines and developer productivity.

**All-in-One Tool**: uv replaces the fragmented Python tooling ecosystem:
- `pip` → `uv pip` / `uv sync`
- `venv/virtualenv` → `uv venv` (automatic)
- `pip-tools` → `uv.lock` (native lockfile)
- `pyenv` → `uv python install` (Python version management)

This consolidation reduces cognitive overhead and eliminates version mismatches between tools.

**Native Monorepo Support**: uv provides first-class workspace features:
- `[tool.uv.workspace]` for defining workspace members
- `uv sync --all-packages` for atomic workspace synchronization
- Unified `uv.lock` across all workspace members
- `uv build --package X` for selective package building
- `[tool.uv.sources]` for workspace dependency linking

**Why Not Alternatives**:
- **pip**: Slow resolution, no lockfile, needs 4+ additional tools for equivalent functionality
- **Poetry**: Python-based (slower), poor monorepo support, hybrid config format causes friction
- **PDM**: PEP 582 focus (now rejected PEP), smaller community, Python-based
- **Pipenv**: Notoriously slow, irregular updates, non-standard Pipfile format
- **pyenv**: Only handles Python versions; uv includes this functionality

**Ecosystem Coherence**: uv is part of the Astral suite (uv, Ruff, ty), providing a unified, high-performance toolchain vision for modern Python development.

---

## 2. Linting & Formatting: Ruff

**Chosen:** Ruff (Astral)

### Alternatives:
- black (formatting)
- isort (import sorting)
- flake8 (linting)
- pylint (linting)
- autopep8 (formatting)
- yapf (formatting)
- pyflakes (linting)
- pycodestyle (linting)

### Justification:

**Performance (10-100x faster)**: Ruff is written in Rust and processes code 10-100x faster than Python-based linters. On large codebases where black+isort+flake8 might take 30+ seconds, Ruff completes in under 1 second. This enables real-time IDE linting, instant pre-commit hooks, and faster CI pipelines.

**One Tool Replaces Many**: Ruff consolidates the fragmented Python linting ecosystem:
- `black` → `ruff format` (black-compatible)
- `isort` → Ruff I rules (import sorting)
- `flake8` + 50+ plugins → Ruff's 800+ built-in rules
- `pyupgrade` → Ruff UP rules (syntax modernization)
- `autoflake` → Ruff F rules (unused imports)
- `pycodestyle` → Ruff E/W rules
- `pep8-naming` → Ruff N rules

**Single Configuration**: One `[tool.ruff]` section in pyproject.toml replaces:
- `.flake8`
- `.isort.cfg`
- `[tool.black]`
- Multiple plugin configs

**Auto-fix Capability**: Most issues are auto-fixable via `ruff check --fix`, dramatically improving developer experience compared to manual fixes.

**Why Not Alternatives**:
- **black**: Formatting only, no linting. `ruff format` is black-compatible but faster
- **isort**: Import sorting only; Ruff includes these rules natively
- **flake8**: Python-based (slow), requires plugin ecosystem, separate config
- **pylint**: Extremely slow, complex configuration, high false-positive rate
- **autopep8/yapf**: Legacy formatters; black/ruff format are the modern standard

**IDE Integration**: The VSCode Ruff extension provides format-on-save, real-time diagnostics, and code actions - all faster than legacy Python tooling.

---

## 3. Pre-commit Hooks: prek

**Chosen:** prek

### Alternatives:
- pre-commit (Python-based)
- husky (Node.js)
- lefthook (Go)
- overcommit (Ruby)

### Justification:

**Rust-Native Performance**: prek is a Rust-based pre-commit alternative that executes hooks faster than Python-based pre-commit. For commit-time hooks where developer patience is limited, this speed matters.

**Built-in Hooks (Offline-Capable)**: prek includes Rust-native implementations of common hooks:
- `trailing-whitespace`
- `end-of-file-fixer`
- `check-yaml`
- `check-toml`
- `check-added-large-files`
- `check-merge-conflict`
- `detect-private-key`

These run without downloading external tools, enabling offline development and faster first-run setup.

**Config Compatibility**: prek uses the same `.pre-commit-config.yaml` format as pre-commit, enabling easy migration between tools if needed.

**Ruff Integration**: The `ruff-pre-commit` hooks work seamlessly with prek, combining Rust-based linting with Rust-based hook execution.

**Why Not Alternatives**:
- **pre-commit**: Python-based (slower), requires Python environment, downloads tools on first run
- **husky**: Node.js-based, introduces JavaScript dependency to Python project
- **lefthook**: Go-based alternative, less ecosystem support for Python tools
- **overcommit**: Ruby-based, introduces Ruby dependency

**Ecosystem Coherence**: prek complements the Rust-first philosophy (uv, ruff, ty) while maintaining compatibility with the pre-commit ecosystem.

---

## 4. Testing: pytest

**Chosen:** pytest

### Alternatives:
- unittest (stdlib)
- nose/nose2
- doctest (stdlib)
- hypothesis (property-based)

### Justification:

**Industry Standard**: pytest has 90%+ adoption in modern Python projects. It has effectively won the Python testing framework competition.

**Simple, Expressive Syntax**: Plain `assert` statements instead of verbose `self.assertEqual()`:
```python
# pytest
assert result == expected

# unittest
self.assertEqual(result, expected)
```

**Powerful Fixture System**: Composable, dependency-injected fixtures replace complex setUp/tearDown:
```python
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()
```

**Rich Plugin Ecosystem**:
- `pytest-cov`: Coverage reporting
- `pytest-xdist`: Parallel test execution
- `pytest-asyncio`: Async test support
- `pytest-mock`: Enhanced mocking

**Monorepo Friendly**: `testpaths = ["apps", "libs"]` discovers tests across workspace.

**Why Not Alternatives**:
- **unittest**: Verbose xUnit style, no fixtures, limited assertions
- **nose/nose2**: Effectively deprecated, unmaintained
- **doctest**: Good for documentation examples, not for comprehensive testing

---

## 5. Documentation: MkDocs

**Chosen:** MkDocs (with Material or Shadcn theme)

### Alternatives:
- Sphinx
- pdoc
- pydoc (stdlib)
- mkdocstrings
- Docusaurus

### Justification:

**Markdown-First**: MkDocs uses Markdown, which is more widely known than Sphinx's reStructuredText. Lower barrier to entry for contributors.

**Beautiful Themes**: MkDocs Material provides a polished, modern UI out-of-the-box:
- Dark/light mode toggle
- Search with highlighting
- Mobile-responsive
- Code block copy buttons
- Mermaid diagram support

MPM also supports mkdocs-shadcn for an alternative modern aesthetic.

**Simple Configuration**: A single `mkdocs.yml` file vs Sphinx's complex `conf.py`:
```yaml
site_name: My Project
theme:
  name: material
plugins:
  - search
  - mkdocstrings
```

**Live Reload**: Fast development server with instant reload on file changes.

**API Documentation**: mkdocstrings generates API docs from Python docstrings, supporting Google, NumPy, and Sphinx docstring styles.

**Why Not Alternatives**:
- **Sphinx**: reStructuredText learning curve, dated default themes, complex configuration
- **pdoc**: Limited customization, no theme ecosystem
- **pydoc**: Stdlib but very basic, no modern features
- **Docusaurus**: React-based, overkill for Python projects

---

## 6. Type Checking: ty

**Chosen:** ty (Astral)

### Alternatives:
- mypy
- pyright
- pytype (Google)
- pyre (Meta)

### Justification:

**Rust Performance**: ty is Astral's new Rust-based type checker, offering 10-100x speed improvements over Python-based mypy. For large codebases, this means type checking in seconds instead of minutes.

**Astral Ecosystem**: ty is part of the unified Astral toolchain (uv, ruff, ty), providing consistent configuration and behavior. The team's track record with Ruff's rapid adoption suggests ty will mature quickly.

**Auto-Configuration**: ty automatically infers Python version from `project.requires-python` in pyproject.toml, reducing configuration boilerplate.

**Forward-Looking Choice**: While ty is still in alpha (as of 2025), MPM is designed for modern projects. Early adoption positions projects for the future of Python type checking.

**Why Not Alternatives**:
- **mypy**: Established but Python-based (slow), complex configuration
- **pyright**: Fast (TypeScript-based), powers Pylance, but separate from Astral ecosystem
- **pytype**: Google's type checker, less community adoption
- **pyre**: Meta's type checker, primarily for internal use

**Fallback Strategy**: Projects can switch to mypy/pyright if ty's alpha status causes issues, as the type annotation syntax is standardized.

---

## 7. Project Configuration: pyproject.toml

**Chosen:** pyproject.toml (PEP 517/518/621)

### Alternatives:
- requirements.txt + setup.py
- setup.cfg + setup.py
- Pipfile (pipenv)

### Justification:

**Modern Python Standard**: pyproject.toml is standardized by PEP 517 (build system), PEP 518 (build requirements), and PEP 621 (project metadata). All modern Python tools support it.

**Single Source of Truth**: One file for:
- Project metadata (`[project]`)
- Dependencies (`dependencies`, `[dependency-groups]`)
- Build configuration (`[build-system]`)
- Tool settings (`[tool.ruff]`, `[tool.pytest]`, `[tool.poe]`, etc.)

**Unified Configuration**: Before pyproject.toml, projects needed:
- `setup.py` or `setup.cfg` for packaging
- `requirements.txt` for dependencies
- `.flake8` for linting
- `.isort.cfg` for imports
- `pytest.ini` for testing

Now everything lives in one file.

**Dependency Groups**: Modern `[dependency-groups]` (PEP 735) replaces confusing extras:
```toml
[dependency-groups]
dev = ["pytest", "ruff", "ty"]
docs = ["mkdocs", "mkdocs-material"]
```

**Why Not Alternatives**:
- **requirements.txt**: No metadata, no dependency resolution, multiple files needed
- **setup.py**: Executable code (security risk), legacy format
- **setup.cfg**: Transitional format, superseded by pyproject.toml
- **Pipfile**: Non-standard, pipenv-specific

---

## 8. Docker Builds: docker-bake

**Chosen:** docker buildx bake (with HCL)

### Alternatives:
- docker build
- docker-compose build
- kaniko
- buildah

### Justification:

**Parallel Multi-Target Builds**: docker-bake builds multiple targets concurrently. In a monorepo with 5 apps, this can reduce build time by 80%.

**Multi-Platform Support**: Build for linux/amd64 and linux/arm64 in a single command:
```hcl
target "app" {
  platforms = ["linux/amd64", "linux/arm64"]
}
```

**Declarative HCL Configuration**: Clear, version-controlled build definitions:
```hcl
target "app" {
  context    = "."
  dockerfile = "Dockerfile"
  tags       = ["${REGISTRY}/app:${TAG}"]
  cache-from = ["type=gha"]
  cache-to   = ["type=gha,mode=max"]
}
```

**Target Inheritance**: DRY configuration via `inherits`:
```hcl
target "app-dev" {
  inherits = ["app"]
  target   = "builder"
}
```

**GitHub Actions Cache Integration**: Native support for GHA cache backend, dramatically speeding CI builds.

**Variable Substitution**: Dynamic tags, registry URLs, and Python versions via variables.

**Why Not Alternatives**:
- **docker build**: Single target, no parallelism, manual multi-platform handling
- **docker-compose build**: Sequential builds, limited caching control
- **kaniko**: For daemonless builds in CI, but more complex setup
- **buildah**: Good for rootless builds, but less ecosystem integration

---

## 9. Task Runner: Poe the Poet

**Chosen:** Poe the Poet (poethepoet)

### Alternatives:
- Makefile
- invoke
- tox
- nox
- just
- taskfile

### Justification:

**pyproject.toml Native**: Tasks defined directly in `[tool.poe.tasks]`, no separate file:
```toml
[tool.poe.tasks]
fmt = "ruff format"
lint = "ruff check --fix"
check = "ty check"
test = "pytest"
all = ["fmt", "lint", "check", "test"]
```

**Task Composition**: Combine tasks into sequences:
```toml
all = ["fmt", "lint", "check", "test"]
```

**Cross-Platform**: Works on Windows, macOS, and Linux without requiring make or shell-specific syntax.

**uv Integration**: Seamlessly works with `uv run poe <task>`, leveraging uv's fast execution.

**CI/Dev Parity**: Same commands work locally and in CI:
```bash
uv run poe test      # local
uv run poe ci:lint   # CI (stricter)
```

**Why Not Alternatives**:
- **Makefile**: Unix-only, requires make installation, shell syntax quirks
- **invoke**: Requires separate tasks.py file, Python function syntax
- **tox/nox**: Testing-focused, overkill for simple task running
- **just**: Rust-based but requires justfile, not in pyproject.toml
- **taskfile**: YAML-based, separate file

---

## 10. Build Backend: hatchling

**Chosen:** hatchling (with uv build)

### Alternatives:
- setuptools
- flit
- pdm-backend
- maturin (Rust extensions)

### Justification:

**Modern, Fast Build Backend**: hatchling is Hatch's PEP 517-compliant build backend, designed for modern Python packaging.

**Plugin System**: Extensible via plugins:
- `hatch-una`: Inlines internal monorepo dependencies into wheels
- `hatch-vcs`: Version from git tags
- `hatch-fancy-pypi-readme`: Dynamic README generation

**Monorepo Wheel Building**: With `hatch-una`, internal dependencies are properly bundled:
```toml
[build-system]
requires = ["hatchling", "hatch-una"]
build-backend = "hatchling.build"

[tool.hatch.build.hooks.una-build]
[tool.hatch.metadata.hooks.una-meta]
```

**src Layout Support**: Native understanding of `src/package` structure without configuration.

**Minimal Configuration**: Sensible defaults reduce boilerplate compared to setuptools.

**uv build Integration**: `uv build` uses whatever backend is specified in pyproject.toml, so hatchling works seamlessly.

**Why Not Alternatives**:
- **setuptools**: Legacy, complex, backward-compatibility baggage, verbose config
- **flit**: Simple but limited (no build hooks, no plugins for monorepo support)
- **pdm-backend**: PDM-specific, less ecosystem adoption
- **maturin**: For Rust extensions, not pure Python

---

## 11. Monorepo Tool: una

**Chosen:** una

### Alternatives:
- pants
- bazel
- nx
- lerna (Node.js)
- turborepo (Node.js)

### Justification:

**Lightweight Python Monorepo Solution**: una is designed specifically for Python monorepos using uv workspaces, without the complexity of enterprise build systems.

**uv Workspace Integration**: Works seamlessly with uv's native workspace support:
```toml
[tool.uv.workspace]
members = ["apps/*", "libs/*"]

[tool.una]
namespace = "myorg"
```

**hatch-una for Wheel Building**: The `hatch-una` plugin properly inlines internal dependencies when building wheels, solving Python's monorepo packaging challenge.

**Namespace Package Support**: Enables shared namespaces across packages:
```
myorg.app1  (apps/app1)
myorg.app2  (apps/app2)
myorg.lib1  (libs/lib1)
```

**Simple Mental Model**: Uses standard Python packaging (pyproject.toml, src layout) rather than inventing new concepts.

**Right-Sized Solution**: For small-to-medium monorepos (2-20 packages), una provides the benefits without the overhead.

**Why Not Alternatives**:
- **pants**: Powerful but massive complexity, steep learning curve, overkill for most Python projects
- **bazel**: Google's build system, extremely complex, primarily for huge codebases
- **nx**: JavaScript/TypeScript focused, poor Python support
- **lerna/turborepo**: Node.js ecosystem, not designed for Python

**When to Consider Alternatives**: If your monorepo grows to 50+ packages with complex interdependencies, enterprise tools like pants may become worthwhile. For most projects, una's simplicity is the right choice.

---

## Summary

The MPM CLI chooses tools based on:

1. **Performance**: Rust-based tools (uv, ruff, prek, ty) for maximum speed
2. **Modern Standards**: PEP compliance, pyproject.toml-first
3. **Developer Experience**: Single-tool philosophy, minimal configuration
4. **Ecosystem Coherence**: Astral suite (uv, ruff, ty) for unified experience
5. **Production Readiness**: Proven tools with active maintenance
