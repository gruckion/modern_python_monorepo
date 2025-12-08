"""Package generator for adding new packages to existing projects."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from rich.console import Console

if TYPE_CHECKING:
    from modern_python_monorepo.mpm.generators.renderer import TemplateRenderer

from modern_python_monorepo.mpm.config import (
    PackageConfig,
    PackageType,
    TemplateContext,
)
from modern_python_monorepo.mpm.generators.renderer import get_renderer

console = Console()


def generate_package(
    config: PackageConfig,
    project_dir: Path,
    project_ctx: TemplateContext | None = None,
) -> None:
    """Generate a new package in an existing project.

    Args:
        config: Package configuration
        project_dir: Root directory of the project
        project_ctx: Optional existing project context
    """
    renderer = get_renderer()

    # Create package context
    if project_ctx is None:
        # Minimal context for package generation
        project_ctx = TemplateContext(
            project_name=project_dir.name,
            project_slug=project_dir.name.replace("_", "-"),
            namespace=config.namespace,
            python_version="3.13",
            python_requires=config.python_requires,
        )

    # Create package-specific context
    ctx = TemplateContext.from_package_config(config, project_ctx)

    # Determine output directory
    if config.package_type == PackageType.LIB:
        package_dir = project_dir / "libs" / config.package_name
        template_base = "monorepo/libs/__package__"
    else:
        package_dir = project_dir / "apps" / config.package_name
        template_base = "monorepo/apps/__package__"

    if package_dir.exists():
        console.print(f"[red]Error:[/red] Package directory already exists: {package_dir}")
        raise ValueError(f"Package directory already exists: {package_dir}")

    console.print(f"[blue]Creating {config.package_type.value}:[/blue] {config.package_name}")

    # Create package directory structure
    _generate_package_structure(renderer, ctx, package_dir, template_base)

    # Generate Dockerfile for apps if requested
    if config.package_type == PackageType.APP and config.with_docker:
        _generate_app_dockerfile(renderer, ctx, package_dir)

    console.print(f"[green]✓[/green] Created {config.package_type.value}: {config.package_name}")
    console.print("\n[dim]Run 'uv sync --all-packages' to update dependencies[/dim]")


def _generate_package_structure(
    renderer: TemplateRenderer,
    ctx: TemplateContext,
    package_dir: Path,
    template_base: str,
) -> None:
    """Generate the package directory structure."""

    # Create directories
    pkg_src_dir = package_dir / ctx.namespace / ctx.package_name
    tests_dir = package_dir / "tests"

    pkg_src_dir.mkdir(parents=True, exist_ok=True)
    tests_dir.mkdir(parents=True, exist_ok=True)

    # Namespace __init__.py
    (package_dir / ctx.namespace / "__init__.py").write_text("# Namespace package\n")

    # pyproject.toml
    renderer.render_to_file(
        f"{template_base}/pyproject.toml.jinja",
        package_dir / "pyproject.toml",
        ctx,
    )

    # Source files
    renderer.render_to_file(
        f"{template_base}/__namespace__/__package__/__init__.py.jinja",
        pkg_src_dir / "__init__.py",
        ctx,
    )
    renderer.copy_static(
        f"{template_base}/__namespace__/__package__/py.typed",
        pkg_src_dir / "py.typed",
    )

    # Test files
    (tests_dir / "__init__.py").write_text("# Tests package\n")
    renderer.render_to_file(
        f"{template_base}/tests/test_import.py.jinja",
        tests_dir / "test_import.py",
        ctx,
    )


def _generate_app_dockerfile(
    renderer: TemplateRenderer,
    ctx: TemplateContext,
    package_dir: Path,
) -> None:
    """Generate Dockerfile for an application."""

    renderer.render_to_file(
        "monorepo/apps/__package__/Dockerfile.jinja",
        package_dir / "Dockerfile",
        ctx,
    )
    console.print("[green]✓[/green] Generated Dockerfile")
