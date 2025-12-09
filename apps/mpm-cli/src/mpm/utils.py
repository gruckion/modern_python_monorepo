"""Utility functions for MPM CLI."""

import re
import tomllib
from pathlib import Path


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


def get_namespace_from_project(project_root: Path) -> str | None:
    """Get the namespace from a project's pyproject.toml."""
    pyproject = project_root / "pyproject.toml"
    if not pyproject.exists():
        return None

    try:
        with open(pyproject, "rb") as f:
            config = tomllib.load(f)
            return config.get("tool", {}).get("una", {}).get("namespace")
    except (tomllib.TOMLDecodeError, KeyError):
        return None
