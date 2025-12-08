"""Project scaffold generator for MPM CLI."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

from rich.console import Console

from modern_python_monorepo.mpm.config import (
    ProjectConfig,
    ProjectStructure,
    TemplateContext,
)
from modern_python_monorepo.mpm.generators.ci import generate_ci
from modern_python_monorepo.mpm.generators.docker import generate_docker
from modern_python_monorepo.mpm.generators.docs import generate_docs
from modern_python_monorepo.mpm.generators.renderer import get_renderer

if TYPE_CHECKING:
    from modern_python_monorepo.mpm.generators.renderer import TemplateRenderer

console = Console()


def generate_project(config: ProjectConfig, output_dir: Path) -> None:
    """Generate a new project from configuration.

    Args:
        config: Project configuration
        output_dir: Output directory for the project
    """
    renderer = get_renderer()
    ctx = TemplateContext.from_project_config(config)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"[blue]Creating project:[/blue] {config.project_name}")

    # Generate base files
    _generate_base_files(renderer, ctx, output_dir, config)

    # Generate structure-specific files
    if config.structure == ProjectStructure.MONOREPO:
        _generate_monorepo_structure(renderer, ctx, output_dir, config)
    else:
        _generate_single_structure(renderer, ctx, output_dir)

    # Generate optional features
    if config.features.pre_commit:
        _generate_pre_commit(renderer, output_dir)

    if config.features.docker:
        generate_docker(ctx, output_dir)

    if config.features.github_actions:
        generate_ci(ctx, output_dir, include_pypi=config.features.pypi_publish)

    if config.features.docs:
        generate_docs(ctx, output_dir, theme=config.docs_theme.value)

    # Initialize git if requested
    if config.init_git:
        _init_git(output_dir)

    console.print(f"[green]✓[/green] Project created at: {output_dir}")


def _generate_base_files(
    renderer: TemplateRenderer,
    ctx: TemplateContext,
    output_dir: Path,
    config: ProjectConfig,
) -> None:
    """Generate base project files."""

    # pyproject.toml (use monorepo or single template)
    if config.structure == ProjectStructure.MONOREPO:
        renderer.render_to_file(
            "base/pyproject.toml.jinja",
            output_dir / "pyproject.toml",
            ctx,
        )
    else:
        renderer.render_to_file(
            "single/pyproject.toml.jinja",
            output_dir / "pyproject.toml",
            ctx,
        )

    # README.md
    renderer.render_to_file(
        "base/README.md.jinja",
        output_dir / "README.md",
        ctx,
    )

    # LICENSE
    if config.license_type.value != "none":
        renderer.render_to_file(
            "base/LICENSE.jinja",
            output_dir / "LICENSE",
            ctx,
        )

    # .gitignore
    renderer.copy_static("base/.gitignore", output_dir / ".gitignore")

    # .python-version
    renderer.render_to_file(
        "base/.python-version.jinja",
        output_dir / ".python-version",
        ctx,
    )

    console.print("[green]✓[/green] Generated base files")


def _generate_monorepo_structure(
    renderer: TemplateRenderer,
    ctx: TemplateContext,
    output_dir: Path,
    config: ProjectConfig,
) -> None:
    """Generate monorepo directory structure."""

    # Create apps/ and libs/ directories
    (output_dir / "apps").mkdir(exist_ok=True)
    (output_dir / "libs").mkdir(exist_ok=True)
    (output_dir / "apps" / ".gitkeep").touch()
    (output_dir / "libs" / ".gitkeep").touch()

    console.print("[green]✓[/green] Created monorepo structure")

    # Generate sample packages if requested
    if config.with_samples:
        _generate_sample_packages(renderer, ctx, output_dir)


def _generate_single_structure(
    renderer: TemplateRenderer,
    ctx: TemplateContext,
    output_dir: Path,
) -> None:
    """Generate single package directory structure."""

    # Create src directory with namespace
    src_dir = output_dir / "src" / ctx.namespace
    src_dir.mkdir(parents=True, exist_ok=True)

    # Generate source files
    renderer.render_to_file(
        "single/src/__namespace__/__init__.py.jinja",
        src_dir / "__init__.py",
        ctx,
    )
    renderer.copy_static(
        "single/src/__namespace__/py.typed",
        src_dir / "py.typed",
    )

    # Generate tests
    tests_dir = output_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    renderer.copy_static("single/tests/__init__.py", tests_dir / "__init__.py")
    renderer.render_to_file(
        "single/tests/test_import.py.jinja",
        tests_dir / "test_import.py",
        ctx,
    )

    console.print("[green]✓[/green] Created single package structure")


def _generate_sample_packages(
    renderer: TemplateRenderer,
    ctx: TemplateContext,
    output_dir: Path,
) -> None:
    """Generate sample greeter and printer packages."""

    # Generate greeter library
    greeter_dir = output_dir / "libs" / "greeter"
    greeter_pkg_dir = greeter_dir / ctx.namespace / "greeter"
    greeter_tests_dir = greeter_dir / "tests"

    greeter_pkg_dir.mkdir(parents=True, exist_ok=True)
    greeter_tests_dir.mkdir(parents=True, exist_ok=True)

    # Namespace __init__.py
    (greeter_dir / ctx.namespace / "__init__.py").write_text("# Namespace package\n")

    renderer.render_to_file(
        "samples/greeter/pyproject.toml.jinja",
        greeter_dir / "pyproject.toml",
        ctx,
    )
    renderer.render_to_file(
        "samples/greeter/__namespace__/greeter/__init__.py.jinja",
        greeter_pkg_dir / "__init__.py",
        ctx,
    )
    renderer.copy_static(
        "samples/greeter/__namespace__/greeter/py.typed",
        greeter_pkg_dir / "py.typed",
    )
    (greeter_tests_dir / "__init__.py").write_text("# Tests package\n")
    renderer.render_to_file(
        "samples/greeter/tests/test_greeter.py.jinja",
        greeter_tests_dir / "test_greeter.py",
        ctx,
    )

    console.print("[green]✓[/green] Created greeter library")

    # Generate printer application
    printer_dir = output_dir / "apps" / "printer"
    printer_pkg_dir = printer_dir / ctx.namespace / "printer"
    printer_tests_dir = printer_dir / "tests"

    printer_pkg_dir.mkdir(parents=True, exist_ok=True)
    printer_tests_dir.mkdir(parents=True, exist_ok=True)

    # Namespace __init__.py
    (printer_dir / ctx.namespace / "__init__.py").write_text("# Namespace package\n")

    renderer.render_to_file(
        "samples/printer/pyproject.toml.jinja",
        printer_dir / "pyproject.toml",
        ctx,
    )
    renderer.render_to_file(
        "samples/printer/__namespace__/printer/__init__.py.jinja",
        printer_pkg_dir / "__init__.py",
        ctx,
    )
    renderer.copy_static(
        "samples/printer/__namespace__/printer/py.typed",
        printer_pkg_dir / "py.typed",
    )
    (printer_tests_dir / "__init__.py").write_text("# Tests package\n")
    renderer.render_to_file(
        "samples/printer/tests/test_printer.py.jinja",
        printer_tests_dir / "test_printer.py",
        ctx,
    )

    # Generate Dockerfile for printer if Docker is enabled
    if ctx.with_docker:
        renderer.render_to_file(
            "samples/printer/Dockerfile.jinja",
            printer_dir / "Dockerfile",
            ctx,
        )

    console.print("[green]✓[/green] Created printer application")


def _generate_pre_commit(renderer: TemplateRenderer, output_dir: Path) -> None:
    """Generate pre-commit configuration."""

    renderer.copy_static(
        "tooling/.pre-commit-config.yaml",
        output_dir / ".pre-commit-config.yaml",
    )
    console.print("[green]✓[/green] Generated pre-commit configuration")


def _init_git(output_dir: Path) -> None:
    """Initialize git repository."""
    try:
        subprocess.run(
            ["git", "init"],
            cwd=output_dir,
            capture_output=True,
            check=True,
        )
        console.print("[green]✓[/green] Initialized git repository")
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("[yellow]![/yellow] Could not initialize git repository")
