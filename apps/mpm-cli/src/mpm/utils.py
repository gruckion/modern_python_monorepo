"""Utility functions for MPM CLI."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import TYPE_CHECKING

import tomli_w

if TYPE_CHECKING:
    from mpm.config import MpmConfig


def to_snake_case(name: str) -> str:
    """Convert a string to snake_case."""
    # Replace hyphens with underscores
    name = name.replace("-", "_")
    # Convert camelCase to snake_case
    name = re.sub(r"([a-z])([A-Z])", r"\1_\2", name)
    return name.lower()


def to_kebab_case(name: str) -> str:
    """Convert a string to kebab-case."""
    # Replace underscores with hyphens
    name = name.replace("_", "-")
    # Convert camelCase to kebab-case
    name = re.sub(r"([a-z])([A-Z])", r"\1-\2", name)
    return name.lower()


def is_valid_python_identifier(name: str) -> bool:
    """Check if a name is a valid Python identifier."""
    snake = to_snake_case(name)
    return snake.isidentifier()


# Python reserved keywords that cannot be used as project/package names
PYTHON_KEYWORDS = frozenset(
    {
        "False",
        "None",
        "True",
        "and",
        "as",
        "assert",
        "async",
        "await",
        "break",
        "class",
        "continue",
        "def",
        "del",
        "elif",
        "else",
        "except",
        "finally",
        "for",
        "from",
        "global",
        "if",
        "import",
        "in",
        "is",
        "lambda",
        "nonlocal",
        "not",
        "or",
        "pass",
        "raise",
        "return",
        "try",
        "while",
        "with",
        "yield",
    }
)

# Names that would conflict with Python internals
RESERVED_NAMES = frozenset(
    {
        "__init__",
        "__main__",
        "__pycache__",
        "__all__",
        "__builtins__",
        "__doc__",
        "__file__",
        "__name__",
        "__package__",
        "__spec__",
        "test",
        "tests",
        "src",
        "lib",
        "libs",
        "app",
        "apps",
        "dist",
        "build",
    }
)


def validate_project_name(name: str) -> tuple[bool, str]:
    """Validate a project or package name.

    Returns:
        A tuple of (is_valid, error_message).
        If valid, error_message is empty.
    """
    if not name:
        return False, "Name cannot be empty"

    if len(name) > 100:
        return False, "Name is too long (max 100 characters)"

    # Check for path traversal attempts
    if ".." in name or "/" in name or "\\" in name:
        return False, "Name cannot contain path separators or '..'"

    # Check for spaces
    if " " in name:
        return False, "Name cannot contain spaces (use hyphens or underscores)"

    # Check for special characters (only allow alphanumeric, hyphens, underscores)
    # Allow underscore at start to catch dunder names like __init__ in reserved names check
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*$", name):
        return False, "Name must start with a letter and contain only letters, numbers, hyphens, or underscores"

    # Convert to snake_case for Python identifier check
    snake_name = to_snake_case(name)

    # Check if it's a valid Python identifier
    if not snake_name.isidentifier():
        return False, f"'{snake_name}' is not a valid Python identifier"

    # Check for Python keywords
    if snake_name in PYTHON_KEYWORDS or snake_name.lower() in {k.lower() for k in PYTHON_KEYWORDS}:
        return False, f"'{name}' is a Python reserved keyword"

    # Check for reserved names
    if snake_name in RESERVED_NAMES or snake_name.lower() in {n.lower() for n in RESERVED_NAMES}:
        return False, f"'{name}' is a reserved name that may cause conflicts"

    return True, ""


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
    """Find the project root by looking for mpm.toml.

    All mpm-managed projects have an mpm.toml file at the root.
    """
    path = start_path or Path.cwd()

    while path != path.parent:
        if (path / "mpm.toml").exists():
            return path
        path = path.parent

    return None


def get_namespace_from_project(project_root: Path) -> str | None:
    """Get the namespace from a project's mpm.toml."""
    mpm_toml = project_root / "mpm.toml"
    if not mpm_toml.exists():
        return None

    try:
        with open(mpm_toml, "rb") as f:
            config = tomllib.load(f)
            return config.get("project", {}).get("name")
    except (tomllib.TOMLDecodeError, KeyError):
        return None


def load_mpm_config(path: Path) -> MpmConfig:
    """Load and parse mpm.toml file into MpmConfig."""
    from mpm.config import MpmConfig

    return MpmConfig.from_toml(path)


def save_mpm_config(config: MpmConfig, path: Path) -> None:
    """Write MpmConfig to mpm.toml file."""
    # Generate header comment
    header = """# mpm.toml - Modern Python Monorepo Configuration
# This file stores your project scaffolding choices.
# Keep it to enable `mpm add` commands to understand your setup.

"""

    toml_dict = config.to_toml_dict()
    toml_content = tomli_w.dumps(toml_dict)

    path.write_text(header + toml_content)
