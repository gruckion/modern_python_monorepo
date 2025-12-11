# CLI Features Missing - Comparison Report

Generated project: `hello` (with all flags: `--monorepo --with-samples --with-docker --with-ci --with-pypi --with-docs`)

Reference project: `modern_python_monorepo` (this repository)

---

## File Structure Comparison

### Reference Project Tree (excluding mpm-cli and build artifacts)

```
.
├── .dockerignore
├── .github/workflows/
│   ├── pr.yml
│   └── release.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── .vscode/
│   ├── extensions.json
│   └── settings.json
├── apps/printer/
│   ├── Dockerfile
│   ├── modern_python_monorepo/printer/
│   │   ├── __init__.py
│   │   └── py.typed
│   ├── modern_python_monorepo/py.typed    <-- MISSING in generated
│   ├── pyproject.toml
│   └── tests/test_printer_import.py
├── docker-bake.hcl
├── docker-compose.yml
├── docs/
│   ├── api/
│   │   ├── greeter.md                      <-- MISSING
│   │   ├── index.md                        <-- MISSING
│   │   └── printer.md                      <-- MISSING
│   ├── architecture/
│   │   └── overview.md                     <-- MISSING
│   ├── contributing.md                     <-- MISSING
│   ├── development/
│   │   ├── commands.md                     <-- MISSING
│   │   ├── docker.md                       <-- MISSING
│   │   └── setup.md                        <-- MISSING
│   ├── getting-started.md
│   └── index.md
├── libs/greeter/
│   ├── modern_python_monorepo/greeter/
│   │   ├── __init__.py
│   │   └── py.typed
│   ├── modern_python_monorepo/py.typed    <-- MISSING in generated
│   ├── pyproject.toml
│   └── tests/test_greeter_import.py
├── LICENSE
├── mkdocs.yml
├── pyproject.toml
└── README.md
```

### Generated Project Tree

```
.
├── .dockerignore
├── .github/workflows/
│   ├── pr.yml
│   └── release.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── apps/printer/
│   ├── Dockerfile
│   ├── hello/printer/
│   │   ├── __init__.py
│   │   └── py.typed
│   ├── pyproject.toml
│   └── tests/test_printer_import.py
├── docker-bake.hcl
├── docker-compose.yml
├── docs/
│   ├── getting-started.md
│   └── index.md                           <-- Only 2 files
├── libs/greeter/
│   ├── hello/greeter/
│   │   ├── __init__.py
│   │   └── py.typed
│   ├── pyproject.toml
│   └── tests/test_greeter_import.py
├── LICENSE
├── mkdocs.yml
├── pyproject.toml
└── README.md
```

### Missing Files/Directories

1. `.vscode/` - VS Code configuration directory
   - `extensions.json`
   - `settings.json`
2. `docs/api/` - API reference documentation
   - `greeter.md`
   - `index.md`
   - `printer.md`
3. `docs/architecture/overview.md`
4. `docs/contributing.md`
5. `docs/development/` - Development guides
   - `commands.md`
   - `docker.md`
   - `setup.md`
6. `libs/greeter/<namespace>/py.typed` - Namespace-level py.typed marker
7. `apps/printer/<namespace>/py.typed` - Namespace-level py.typed marker

---

## 1. CRITICAL: `mpm add` Command - Python Version Bug

### Bug Description

When using `mpm add lib <name>` or `mpm add app <name>`, the generated `pyproject.toml` has an invalid `requires-python` value:

```toml
requires-python = ">="   # INVALID - missing version number!
```

This causes a TOML parse error:

```
Failed to parse version: Unexpected end of version specifier, expected version: >=
```

### Root Cause (`package.py:125-131`)

```python
ctx = {
    "package_name": name,
    "package_description": description or f"{name.capitalize()} package",
    "namespace": namespace,
    "python_version": "3.13",  # String, not PythonVersion enum!
    "with_docker": with_docker,
}
```

The template expects `python_version.value` (from `PythonVersion` enum), but receives a plain string.

### Template (`monorepo/libs/pyproject.toml.jinja:7`)

```jinja
requires-python = ">={{ python_version.value if python_version is defined else '3.13' }}"
```

When `python_version` is a string, `python_version.value` fails silently, resulting in empty string.

### Fix Required

1. Read Python version from `.python-version` file in project root
2. Pass `PythonVersion` enum OR fix template to handle both string and enum

### Missing Test

No unit test exists for the `mpm add` command verifying Python version handling.

---

## 2. Root `pyproject.toml` Issues

### Missing in Generated

- **`mkdocs-mermaid2-plugin>=1.0.0`** in docs dependency group
- **Comment** `# target-version auto-inferred from project.requires-python` for ruff
- **Comment** `# ty - Type Checking (python-version auto-inferred from project.requires-python)` section header
- **prek hooks tasks** in `[tool.poe.tasks]`:

  ```toml
  hooks = "prek install"
  "hooks:run" = "prek run --all-files"
  ```

### Differences

- Generated uses `mkdocs-material>=9.0.0` but reference uses `mkdocs-shadcn>=0.9.0` (correct based on theme, but material deps may need adjustment)

---

## 3. README.md Issues

### Generated README Problems

- **MD012 violation**: Multiple consecutive blank lines (lines 2-4 have empty lines after title)
- **MD040 violation**: Fenced code blocks without language specified (project structure block ~line 46)
- **Missing badges**: No CI badge, codecov badge, license badge
- **Missing content sections**:
  - No TL;DR summary table
  - No Technology Stack table
  - No Git Hooks (prek) section
  - No detailed Docker section with multi-platform builds
  - No CI/CD explanation
  - No Publishing to PyPI section
  - No Adding New Packages guide
  - No CLI Commands section
- **Much shorter**: Generated is ~84 lines vs reference ~352 lines
- **Generic placeholder content**: Uses `your-username` instead of dynamic values

---

## 4. Documentation (`docs/`) Issues

### Missing Files in Generated (8 files)

- `docs/api/index.md`
- `docs/api/greeter.md`
- `docs/api/printer.md`
- `docs/architecture/overview.md`
- `docs/development/setup.md`
- `docs/development/commands.md`
- `docs/development/docker.md`
- `docs/contributing.md`

### Generated Has Only (2 files)

- `docs/index.md` (minimal placeholder content)
- `docs/getting-started.md` (minimal placeholder content)

### Content Quality Issues

- Generated `index.md` is ~47 lines vs reference ~63 lines
- Generated docs are placeholder-like, lacking real substance
- No badges, no comprehensive feature lists

---

## 5. `mkdocs.yml` Issues

### Missing in Generated (when using material theme)

- `edit_uri: edit/main/docs/`
- `mermaid2` plugin
- More comprehensive `mkdocstrings` options:
  - `show_root_full_path: false`
  - `show_symbol_type_heading: true`
  - `show_symbol_type_toc: true`
  - `docstring_style: google`
  - `members_order: source`
  - `show_signature_annotations: true`
- Additional markdown extensions:
  - `pymdownx.inlinehilite`
  - `pymdownx.snippets`
  - `footnotes`
  - `codehilite`
  - Mermaid custom fence configuration
- Full navigation structure with nested sections

### Navigation Structure Comparison

**Generated nav:**

```yaml
nav:
  - Home: index.md
  - Getting Started: getting-started.md
```

**Reference nav:**

```yaml
nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - Development:
      - Setup: development/setup.md
      - Commands: development/commands.md
      - Docker: development/docker.md
  - Architecture: architecture/overview.md
  - API Reference:
      - Overview: api/index.md
      - greeter: api/greeter.md
      - printer: api/printer.md
  - Contributing: contributing.md
```

---

## 6. Sample Package Issues (`libs/greeter`, `apps/printer`)

### Printer `__init__.py` - BUG: Invalid Import

**Generated uses:**

```python
from hello.greeter import greet  # WRONG - cannot be resolved!
```

**Should be:**

```python
from hello import greeter  # Correct namespace import pattern
```

The import `hello.greeter` cannot be resolved because:

- The namespace package is `hello`
- The subpackage is `greeter`
- Correct import: `from hello import greeter` then use `greeter.greet()`

### Missing py.typed at Namespace Level

Reference has `modern_python_monorepo/py.typed` in both libs and apps packages.
Generated is missing this namespace-level py.typed marker.

### Package pyproject.toml

- Generated adds description (good): `"Sample greeting library using cowsay"`
- Minor: Reference has helpful comment: `# needed for hatch-una metadata hook to work`

---

## 7. CI Workflow Issues (`.github/workflows/pr.yml`)

### YAML Syntax Error (Line 24)

```yaml
- name: Set up Python ${{ matrix.python-version }}        run: uv python install ${{ matrix.python-version }}
```

Missing newline between step name and `run` command!

### Missing in Generated

- `pull_request.types` specification: `[opened, reopened, synchronize]`
- Pinned uv version: `version: "0.5.14"` (generated uses `"latest"`)
- `--all-extras` flag in sync command
- **Lockfile check step**: Ensures `uv.lock` is up to date
- **prek hooks step**: Uses `j178/prek-action@v1`
- Uses `poe cov` vs raw pytest command
- Newer codecov action version: `v5` vs `v4`

### Generated Has Issues

- Uses Python version matrix (different approach)
- YAML syntax error makes workflow invalid

---

## 8. Release Workflow Issues (`.github/workflows/release.yml`)

### Missing in Generated

- **Per-package release tags**: `greeter-v*.*.*`, `printer-v*.*.*`
- **`workflow_dispatch`**: Manual release trigger with inputs
- **TestPyPI support**: Separate job for TestPyPI publishing
- **Package selection logic**: Determine which packages to build based on tag
- **Per-package build steps**: Build greeter and printer separately
- **`verbose: true`** on publish steps
- Newer action versions

### Generated Uses

- Simple `uv build` (not `uv build --package <name>`)
- Single publish job without TestPyPI option
- No manual workflow dispatch

---

## 9. Docker Issues

### `docker-compose.yml` Missing

- BuildKit cache configuration (`cache_from`, `cache_to`)
- `image` tag definitions
- Development service (`printer-dev`) with:
  - Builder stage target
  - Volume mounts for live development
  - `develop.watch` configuration for hot reload
- Generated still uses deprecated `version: "3.8"` key

### `docker-bake.hcl` Issues

- Missing variables: `TAG`, `REGISTRY`, `PYTHON_VERSION`
- Missing `printer-dev` target for development builds
- Missing `ci` target with GitHub Actions cache integration
- Using generic local cache instead of `type=gha` for CI

### `Dockerfile` Issues (apps/printer)

- Generated uses `ghcr.io/astral-sh/uv:python3.13-bookworm-slim` as base vs `python:${PYTHON_VERSION}-slim-bookworm`
- Generated doesn't pin uv version (reference pins `0.5.14`)
- Missing `UV_PYTHON_DOWNLOADS=never` env var
- Generated copies entire `libs/` and `apps/` directories vs selective copying
- Missing BuildKit cache mounts: `--mount=type=cache,target=/root/.cache/uv`
- Missing two-phase dependency installation (deps first, then workspace)
- Generated uses `apt-get install git` (unnecessary)
- Generated uses different user creation syntax
- Generated health check imports wrong module
- Generated CMD runs wrong module path: `python -m hello.printer`

---

## 10. `.gitignore` Issues

### Generated is Bloated (153 lines vs 19 lines)

- Generated includes many unnecessary patterns (Django, Flask, Scrapy, Sphinx, etc.)
- Reference is minimal and focused

### Potentially Problematic

- Generated ignores `.python-version` which is typically committed
- Generated includes lots of IDE-specific patterns that may be unnecessary

---

## 11. `.pre-commit-config.yaml` Issues

### Missing in Generated

- Header comment explaining prek usage
- `--config=pyproject.toml` args for ruff hooks
- `check-toml` hook
- `--maxkb=1000` args for `check-added-large-files`
- Uses `pre-commit/pre-commit-hooks` repo instead of `builtin` hooks (prek builtin hooks are faster)

---

## 12. LICENSE Issues

### Missing

- Current year in copyright (generated has placeholder)
- Actual project name/author in copyright
- Generated has `Copyright (c) Your Name` placeholder
- Reference has `Copyright (c) 2025 GPT Architecture Contributors`
- Reference has markdown header (`# MIT License`)

---

## 13. Missing VS Code Configuration

### Missing `.vscode/` directory

- `extensions.json` - Recommended extensions
- `settings.json` - Project-specific settings

---

## 14. Missing Tests

### Tests that should exist but don't

1. **License content test**: Verify correct license text is generated for each type (MIT, Apache-2.0, GPL-3.0)

2. **`mpm add` command tests** ✅ **ADDED**:
   - `test_add_lib_sets_python_version` - Tests that `mpm add lib` correctly reads from `.python-version`
   - `test_add_app_sets_python_version` - Tests that `mpm add app` correctly reads from `.python-version`
   - Both tests verify `requires-python` is not just `">="` (the bug)

3. **Markdown lint tests**: Verify generated README.md passes MD012, MD040

---

## 15. `.dockerignore` Issues

### Generated is Bloated (66 lines vs 20 lines)

The generated `.dockerignore` includes many unnecessary patterns:

**Reference (focused):**
```
.venv
__pycache__
.git
.gitignore
.vscode
.idea
.pytest_cache
.ruff_cache
.mypy_cache
dist
*.egg-info
```

**Generated includes unnecessary:**
- Full Python packaging patterns (eggs, wheels, sdist, etc.)
- Django/Flask/Scrapy patterns (not relevant)
- IDE-specific patterns (.idea, .vscode already covered)
- Build/dist patterns duplicated multiple ways

---

## Summary of Critical Issues (Priority Order)

### P0 - Breaking Bugs

1. **`mpm add` Python version bug**: `requires-python = ">="` is invalid TOML
2. **CI workflow YAML syntax error**: Line 24 has malformed YAML
3. **Printer import bug**: `from hello.greeter import greet` should be `from hello import greeter`

### P1 - Missing Core Features

4. **Documentation almost empty**: Missing 8 doc files, no API reference, no architecture docs
5. **Release workflow too simplistic**: No per-package releases, no TestPyPI, no manual trigger
6. **Missing prek hooks task**: No `poe hooks` or `poe hooks:run` commands
7. **Missing namespace-level py.typed**: Type checking won't work properly

### P2 - Quality Issues

8. **README markdown lint errors**: MD012 (multiple blank lines), MD040 (missing language on code blocks)
9. **Docker files outdated**: Missing BuildKit optimizations, dev targets, proper caching
10. **Bloated .gitignore**: 153 lines vs reference's focused 19 lines
11. **Missing VS Code config**: No `.vscode/` directory

### P3 - Nice to Have

12. **No license content test**: Can't verify correct license is generated
13. **Missing mkdocs plugins**: No mermaid2 plugin, incomplete mkdocstrings config
14. **Missing `mpm add` tests**: ✅ Tests have been added (see section 14)

---

## Appendix A: Detailed Diffs

### A.1 Root `pyproject.toml` Diff

```diff
--- reference/pyproject.toml
+++ generated/pyproject.toml

# Missing dependencies in [project.optional-dependencies.dev]:
-    # MPM CLI dependencies
-    "typer>=0.12.0",
-    "questionary>=2.1.0",
-    "rich>=13.0.0",
-    "jinja2>=3.1.0",
-    "pydantic>=2.0.0",

# Different docs dependencies:
-    "mkdocs-shadcn>=0.9.0",
+    "mkdocs-material>=9.0.0",
-    "mkdocs-mermaid2-plugin>=1.0.0",

# Missing ruff comment:
-# target-version auto-inferred from project.requires-python

# Missing ty section header:
-# ty - Type Checking (python-version auto-inferred from project.requires-python)

# Missing poe tasks:
-hooks = "prek install"
-"hooks:run" = "prek run --all-files"
```

### A.2 `mkdocs.yml` Key Differences

```diff
--- reference/mkdocs.yml
+++ generated/mkdocs.yml

# Theme difference (reference uses shadcn, generated uses material):
-theme:
-  name: shadcn
-  show_title: true
-  show_stargazers: true
+theme:
+  name: material
+  palette: [...]  # Full material palette config

# Missing edit_uri:
-edit_uri: edit/main/docs/

# Missing mermaid2 plugin:
-  - mermaid2

# Missing mkdocstrings options:
-            show_root_full_path: false
-            show_symbol_type_heading: true
-            show_symbol_type_toc: true
-            docstring_style: google
-            members_order: source
-            show_signature_annotations: true

# Missing markdown extensions:
-  - pymdownx.inlinehilite
-  - pymdownx.snippets
-  - footnotes
-  - codehilite
-  - custom mermaid fence config

# Truncated nav (generated only has 2 items):
-nav:
-  - Development:
-      - Setup: development/setup.md
-      - Commands: development/commands.md
-      - Docker: development/docker.md
-  - Architecture: architecture/overview.md
-  - API Reference:
-      - Overview: api/index.md
-      - greeter: api/greeter.md
-      - printer: api/printer.md
-  - Contributing: contributing.md
```

### A.3 `.github/workflows/pr.yml` Key Differences

```diff
--- reference/pr.yml
+++ generated/pr.yml

# Missing pull_request types:
-  pull_request:
-    types: [opened, reopened, synchronize]
+  pull_request:
+    branches: [main]

# Different uv setup:
-        uses: astral-sh/setup-uv@v5
-          version: "0.5.14"
+        uses: astral-sh/setup-uv@v4
+          version: "latest"

# YAML SYNTAX ERROR on line 24:
+      - name: Set up Python ${{ matrix.python-version }}        run: uv python install ${{ matrix.python-version }}
# ^ Missing newline between name and run!

# Missing lockfile check step:
-      - name: Check lockfile is up to date
-        run: |
-          uv sync --all-packages --all-extras --dev
-          if [[ -n $(git diff --stat uv.lock) ]]; then
-            echo "uv.lock is out of date..."
-            exit 1
-          fi

# Missing prek action:
-      - name: Run prek hooks
-        uses: j178/prek-action@v1
-        with:
-          extra-args: "--all-files"

# Different test command:
-        run: uv run poe cov
+        run: uv run pytest --cov --cov-report=xml

# Different codecov action version:
-        uses: codecov/codecov-action@v5
+        uses: codecov/codecov-action@v4
```

### A.4 `apps/printer/Dockerfile` Key Differences

```diff
--- reference/Dockerfile
+++ generated/Dockerfile

# Different base image approach:
-ARG PYTHON_VERSION=3.13
-FROM python:${PYTHON_VERSION}-slim-bookworm AS builder
-COPY --from=ghcr.io/astral-sh/uv:0.5.14 /uv /uvx /bin/
+FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# Missing UV environment vars:
-ENV UV_COMPILE_BYTECODE=1 \
-    UV_LINK_MODE=copy \
-    UV_PYTHON_DOWNLOADS=never

# Generated installs git (unnecessary):
+RUN apt-get update && apt-get install -y --no-install-recommends \
+    git \
+    && rm -rf /var/lib/apt/lists/*

# Different copy strategy:
-COPY libs/greeter/pyproject.toml libs/greeter/pyproject.toml
-COPY apps/printer/pyproject.toml apps/printer/pyproject.toml
+COPY libs/ libs/
+COPY apps/ apps/

# Missing cache mounts:
-RUN --mount=type=cache,target=/root/.cache/uv \
-    uv sync --frozen --no-install-workspace --no-dev
+RUN uv sync --frozen --no-dev --all-packages

# Different user creation:
-RUN useradd --create-home --shell /bin/bash app
-USER app
+RUN groupadd --gid 1000 appgroup && \
+    useradd --uid 1000 --gid 1000 --create-home appuser
+USER appuser

# Wrong health check:
-    CMD python -c "from modern_python_monorepo.printer import run" || exit 1
+    CMD python -c "print('healthy')" || exit 1

# Different CMD:
-CMD ["python", "-c", "from modern_python_monorepo.printer import run; run()"]
+CMD ["python", "-m", "hello.printer"]
```

### A.5 `apps/printer/__init__.py` Bug

```diff
--- reference/printer/__init__.py
+++ generated/printer/__init__.py

# Reference imports namespace package correctly:
-from modern_python_monorepo import greeter
-
-def run() -> None:
-    print(greeter.greet())

# Generated has invalid import:
+from hello.greeter import greet  # BUG: This import cannot be resolved!
+
+def run() -> None:
+    message = greet("Hello from the printer app!")  # Also wrong signature
+    print(message)
```

### A.6 `.pre-commit-config.yaml` Differences

```diff
--- reference/.pre-commit-config.yaml
+++ generated/.pre-commit-config.yaml

# Missing header comment:
-# prek hooks configuration (Rust-based pre-commit alternative)
-# Install: uv run poe hooks (or: prek install)
-# Run manually: uv run poe hooks:run (or: prek run --all-files)

# Missing ruff args:
-        args: [--fix, --config=pyproject.toml]
+        args: [--fix]
-        args: [--config=pyproject.toml]

# Uses pre-commit repo instead of builtin:
-  - repo: builtin
+  - repo: https://github.com/pre-commit/pre-commit-hooks
+    rev: v5.0.0

# Missing check-toml and maxkb arg:
-      - id: check-toml
-        args: [--maxkb=1000]
```

### A.7 `LICENSE` Differences

```diff
--- reference/LICENSE
+++ generated/LICENSE

-# MIT License
+MIT License

-Copyright (c) 2025 GPT Architecture Contributors
+Copyright (c) Your Name
```
