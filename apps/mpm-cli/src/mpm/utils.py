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
