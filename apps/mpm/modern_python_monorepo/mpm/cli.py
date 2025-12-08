"""MPM CLI - Modern Python Monorepo scaffolding tool."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from modern_python_monorepo.mpm import __version__
from modern_python_monorepo.mpm.config import (
    DocsTheme,
    FeatureSet,
    LicenseType,
    PackageConfig,
    PackageType,
    ProjectConfig,
    ProjectStructure,
    PythonVersion,
    detect_project_config,
)
from modern_python_monorepo.mpm.generators import generate_package, generate_project
from modern_python_monorepo.mpm.prompts import prompt_package_config, prompt_project_config

console = Console()
app = typer.Typer(
    name="mpm",
    help="Modern Python Monorepo CLI - Scaffold production-ready Python projects",
    add_completion=True,
    no_args_is_help=False,
    rich_markup_mode="rich",
    invoke_without_command=True,
)


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        console.print(f"mpm version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    version: Annotated[
        bool | None,
        typer.Option("--version", "-v", callback=version_callback, is_eager=True, help="Show version and exit"),
    ] = None,
) -> None:
    """Modern Python Monorepo CLI - Scaffold production-ready Python projects.

    Examples:

        # Interactive mode
        mpm new

        # Create project with name
        mpm new my-project

        # Create monorepo with all defaults
        mpm new my-project --monorepo --yes

        # Add packages
        mpm add-lib auth
        mpm add-app api --docker
    """
    # If no command was invoked, run interactive project creation
    if ctx.invoked_subcommand is None:
        _create_project_interactive(
            None, False, False, "3.13", False, False, False, False, False, "material", "MIT", False, False
        )


def _create_project_interactive(
    project_name: str | None,
    monorepo: bool,
    single: bool,
    python: str,
    with_samples: bool,
    with_docker: bool,
    with_ci: bool,
    with_pypi: bool,
    with_docs: bool,
    docs_theme: str,
    license_type: str,
    no_git: bool,
    yes: bool,
) -> None:
    """Create a project with the given configuration."""
    # Show welcome banner
    console.print(
        Panel(
            "[bold blue]Modern Python Monorepo[/bold blue]\n[dim]Scaffold production-ready Python projects[/dim]",
            border_style="blue",
        )
    )

    try:
        # Determine if we have enough info for non-interactive mode
        has_structure = monorepo or single
        use_interactive = not (yes or (project_name and has_structure))

        if use_interactive:
            # Interactive mode
            config = prompt_project_config(name=project_name, use_defaults=yes)
        else:
            # Non-interactive mode with CLI flags
            # Determine structure
            if single:
                structure = ProjectStructure.SINGLE
            else:
                structure = ProjectStructure.MONOREPO

            # Determine Python version
            py_version = PythonVersion.PY313
            if python == "3.11":
                py_version = PythonVersion.PY311
            elif python == "3.12":
                py_version = PythonVersion.PY312

            # Determine license
            license_map = {
                "MIT": LicenseType.MIT,
                "Apache-2.0": LicenseType.APACHE,
                "GPL-3.0": LicenseType.GPL,
                "none": LicenseType.NONE,
            }
            selected_license = license_map.get(license_type, LicenseType.MIT)

            # Determine docs theme
            selected_theme = DocsTheme.SHADCN if docs_theme == "shadcn" else DocsTheme.MATERIAL

            # Build feature set
            features = FeatureSet(
                docker=with_docker,
                github_actions=with_ci,
                pypi_publish=with_pypi,
                docs=with_docs,
            )

            config = ProjectConfig(
                project_name=project_name or "my_project",
                structure=structure,
                python_version=py_version,
                features=features,
                with_samples=with_samples,
                docs_theme=selected_theme,
                license_type=selected_license,
                init_git=not no_git,
            )

        # Generate project
        output_dir = Path.cwd() / config.project_slug
        generate_project(config, output_dir)

        # Print next steps
        console.print()
        console.print("[bold green]Next steps:[/bold green]")
        console.print(f"  cd {config.project_slug}")
        console.print("  uv sync --all-packages")
        if config.features.pre_commit:
            console.print("  uv run poe hooks")
        console.print("  uv run poe all")

    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
        raise typer.Exit(1) from None


@app.command("new")
def create_project(
    project_name: Annotated[
        str | None,
        typer.Argument(help="Project name"),
    ] = None,
    monorepo: Annotated[
        bool,
        typer.Option("--monorepo", "-m", help="Create monorepo structure (libs/ + apps/)"),
    ] = False,
    single: Annotated[
        bool,
        typer.Option("--single", "-s", help="Create single package structure"),
    ] = False,
    python: Annotated[
        str,
        typer.Option("--python", "-p", help="Python version requirement"),
    ] = "3.13",
    with_samples: Annotated[
        bool,
        typer.Option("--with-samples", help="Include sample greeter lib and printer app"),
    ] = False,
    with_docker: Annotated[
        bool,
        typer.Option("--with-docker", help="Include Docker configuration"),
    ] = False,
    with_ci: Annotated[
        bool,
        typer.Option("--with-ci", help="Include GitHub Actions CI workflow"),
    ] = False,
    with_pypi: Annotated[
        bool,
        typer.Option("--with-pypi", help="Include PyPI publishing workflow"),
    ] = False,
    with_docs: Annotated[
        bool,
        typer.Option("--with-docs", help="Include MkDocs documentation"),
    ] = False,
    docs_theme: Annotated[
        str,
        typer.Option("--docs-theme", help="MkDocs theme: material or shadcn"),
    ] = "material",
    license_type: Annotated[
        str,
        typer.Option("--license", "-l", help="License: MIT, Apache-2.0, GPL-3.0, none"),
    ] = "MIT",
    no_git: Annotated[
        bool,
        typer.Option("--no-git", help="Skip git repository initialization"),
    ] = False,
    yes: Annotated[
        bool,
        typer.Option("--yes", "-y", help="Accept all defaults (non-interactive mode)"),
    ] = False,
) -> None:
    """Create a new Modern Python Monorepo project.

    If no arguments are provided, runs in interactive mode.
    """
    _create_project_interactive(
        project_name,
        monorepo,
        single,
        python,
        with_samples,
        with_docker,
        with_ci,
        with_pypi,
        with_docs,
        docs_theme,
        license_type,
        no_git,
        yes,
    )


@app.command("add")
def add_interactive() -> None:
    """Add a new package to an existing project (interactive).

    Must be run from within a project directory containing a pyproject.toml
    with workspace configuration.
    """
    # Check if we're in a project
    project_config = detect_project_config(Path.cwd())
    if project_config is None:
        console.print("[red]Error:[/red] Not in a Modern Python Monorepo project")
        console.print("[dim]Run from a directory with pyproject.toml containing workspace config[/dim]")
        raise typer.Exit(1)

    # Interactive mode
    try:
        pkg_config = prompt_package_config(
            namespace=project_config.namespace,
            python_requires=project_config.python_requires,
        )
        generate_package(pkg_config, Path.cwd())
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
        raise typer.Exit(1) from None


@app.command("add-lib")
def add_lib(
    name: Annotated[str, typer.Argument(help="Library name")],
    description: Annotated[
        str,
        typer.Option("--description", "-d", help="Library description"),
    ] = "",
) -> None:
    """Add a new library package to libs/."""
    _add_package(name, PackageType.LIB, description, with_docker=False)


@app.command("add-app")
def add_app_cmd(
    name: Annotated[str, typer.Argument(help="Application name")],
    description: Annotated[
        str,
        typer.Option("--description", "-d", help="Application description"),
    ] = "",
    docker: Annotated[
        bool,
        typer.Option("--docker", help="Include Dockerfile"),
    ] = False,
) -> None:
    """Add a new application package to apps/."""
    _add_package(name, PackageType.APP, description, with_docker=docker)


def _add_package(
    name: str,
    package_type: PackageType,
    description: str,
    with_docker: bool,
) -> None:
    """Add a package to the project."""
    # Check if we're in a project
    project_config = detect_project_config(Path.cwd())
    if project_config is None:
        console.print("[red]Error:[/red] Not in a Modern Python Monorepo project")
        console.print("[dim]Run from a directory with pyproject.toml containing workspace config[/dim]")
        raise typer.Exit(1)

    try:
        pkg_config = PackageConfig(
            package_name=name,
            package_type=package_type,
            description=description,
            with_docker=with_docker,
            namespace=project_config.namespace,
            python_requires=project_config.python_requires,
        )
        generate_package(pkg_config, Path.cwd())
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from None
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
        raise typer.Exit(1) from None


if __name__ == "__main__":
    app()
