"""MPM CLI - Modern Python Monorepo scaffolding tool."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from mpm import __version__
from mpm.config import DocsTheme, LicenseType, ProjectConfig, ProjectStructure, PythonVersion
from mpm.generators.project import generate_project
from mpm.prompts import gather_project_config

app = typer.Typer(
    name="mpm",
    help="Modern Python Monorepo CLI - Scaffold production-ready Python projects",
    add_completion=True,
    no_args_is_help=False,
)
console = Console()

# Subcommand for adding packages
add_app = typer.Typer(help="Add a new package to an existing project")
app.add_typer(add_app, name="add")


def version_callback(value: bool) -> None:
    if value:
        console.print(f"mpm version {__version__}")
        raise typer.Exit()


@app.command("new")
def new_project(
    project_name: Annotated[str, typer.Argument(help="Project name")],
    monorepo: Annotated[bool, typer.Option("--monorepo", "-m", help="Create monorepo structure")] = False,
    single: Annotated[bool, typer.Option("--single", "-s", help="Create single package structure")] = False,
    python: Annotated[str, typer.Option("--python", "-p", help="Python version")] = "3.13",
    with_samples: Annotated[bool, typer.Option(help="Include sample packages")] = False,
    with_docker: Annotated[bool, typer.Option(help="Include Docker configuration")] = False,
    with_ci: Annotated[bool, typer.Option(help="Include GitHub Actions CI")] = False,
    with_pypi: Annotated[bool, typer.Option(help="Include PyPI publishing workflow")] = False,
    with_docs: Annotated[bool, typer.Option(help="Include MkDocs documentation")] = False,
    docs_theme: Annotated[str, typer.Option(help="Docs theme: material or shadcn")] = "material",
    license_type: Annotated[str, typer.Option("--license", "-l", help="License type")] = "MIT",
    no_git: Annotated[bool, typer.Option(help="Skip git initialization")] = False,
    no_sync: Annotated[bool, typer.Option("--no-sync", help="Skip running uv sync after generation")] = False,
    yes: Annotated[bool, typer.Option("--yes", "-y", help="Accept defaults (non-interactive)")] = False,
) -> None:
    """Create a new Modern Python Monorepo project with a given name."""
    _create_project(
        project_name=project_name,
        monorepo=monorepo,
        single=single,
        python=python,
        with_samples=with_samples,
        with_docker=with_docker,
        with_ci=with_ci,
        with_pypi=with_pypi,
        with_docs=with_docs,
        docs_theme=docs_theme,
        license_type=license_type,
        no_git=no_git,
        no_sync=no_sync,
        yes=yes,
    )


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    monorepo: Annotated[bool, typer.Option("--monorepo", "-m", help="Create monorepo structure")] = False,
    single: Annotated[bool, typer.Option("--single", "-s", help="Create single package structure")] = False,
    python: Annotated[str, typer.Option("--python", "-p", help="Python version")] = "3.13",
    with_samples: Annotated[bool, typer.Option(help="Include sample packages")] = False,
    with_docker: Annotated[bool, typer.Option(help="Include Docker configuration")] = False,
    with_ci: Annotated[bool, typer.Option(help="Include GitHub Actions CI")] = False,
    with_pypi: Annotated[bool, typer.Option(help="Include PyPI publishing workflow")] = False,
    with_docs: Annotated[bool, typer.Option(help="Include MkDocs documentation")] = False,
    docs_theme: Annotated[str, typer.Option(help="Docs theme: material or shadcn")] = "material",
    license_type: Annotated[str, typer.Option("--license", "-l", help="License type")] = "MIT",
    no_git: Annotated[bool, typer.Option(help="Skip git initialization")] = False,
    no_sync: Annotated[bool, typer.Option("--no-sync", help="Skip running uv sync after generation")] = False,
    yes: Annotated[bool, typer.Option("--yes", "-y", help="Accept defaults (non-interactive)")] = False,
    version: Annotated[
        bool, typer.Option("--version", "-v", callback=version_callback, is_eager=True, help="Show version")
    ] = False,
) -> None:
    """Create a new Modern Python Monorepo project."""
    # If subcommand invoked, skip
    if ctx.invoked_subcommand is not None:
        return

    # If any structure option is specified, require interactive or use defaults
    if yes or monorepo or single:
        # Non-interactive: use default project name or prompt
        project_name = "my_project"
        _create_project(
            project_name=project_name,
            monorepo=monorepo,
            single=single,
            python=python,
            with_samples=with_samples,
            with_docker=with_docker,
            with_ci=with_ci,
            with_pypi=with_pypi,
            with_docs=with_docs,
            docs_theme=docs_theme,
            license_type=license_type,
            no_git=no_git,
            no_sync=no_sync,
            yes=yes,
        )
    else:
        # Fully interactive mode
        config = gather_project_config(None)
        config.init_git = not no_git
        config.auto_sync = not no_sync
        output_path = Path.cwd() / config.project_slug
        generate_project(config, output_path)
        _show_success(config.project_slug)


def _parse_license_type(license_str: str) -> LicenseType:
    """Parse license string to LicenseType enum."""
    license_lower = license_str.lower()
    if license_lower == "none":
        return LicenseType.NONE
    if license_lower == "mit":
        return LicenseType.MIT
    if license_lower in ("apache-2.0", "apache"):
        return LicenseType.APACHE
    if license_lower in ("gpl-3.0", "gpl"):
        return LicenseType.GPL
    # Fallback: try direct conversion
    return LicenseType(license_str)


def _create_project(
    project_name: str,
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
    no_sync: bool,
    yes: bool,
) -> None:
    """Internal function to create a project."""
    # Determine structure: --monorepo flag enables monorepo, otherwise single package
    # If both flags specified, monorepo takes precedence (common for monorepo workflows)
    if monorepo:
        structure = ProjectStructure.MONOREPO
    elif single:
        structure = ProjectStructure.SINGLE
    else:
        # Default: monorepo for this CLI tool since it's "Modern Python MONOREPO"
        structure = ProjectStructure.MONOREPO
    config = ProjectConfig(
        project_name=project_name.replace("-", "_"),
        project_slug=project_name.replace("_", "-").lower(),
        structure=structure,
        python_version=PythonVersion(python),
        with_samples=with_samples,
        with_docker=with_docker,
        with_ci=with_ci,
        with_pypi=with_pypi,
        with_docs=with_docs,
        docs_theme=DocsTheme(docs_theme),
        license_type=_parse_license_type(license_type),
        init_git=not no_git,
        auto_sync=not no_sync,
    )

    output_path = Path.cwd() / config.project_slug
    generate_project(config, output_path)
    _show_success(config.project_slug)


def _show_success(project_slug: str) -> None:
    """Show success message."""
    console.print(
        Panel.fit(
            f"[green]\u2713[/green] Created [bold]{project_slug}[/bold]\n\n"
            f"Next steps:\n"
            f"  cd {project_slug}\n"
            f"  uv sync --all-packages\n"
            f"  poe check",
            title="Project Created",
        )
    )


@add_app.callback(invoke_without_command=True)
def add_interactive(ctx: typer.Context) -> None:
    """Add a package interactively if no subcommand given."""
    if ctx.invoked_subcommand is None:
        # Interactive mode for add
        import questionary
        from questionary import Choice

        from mpm.generators.package import add_package
        from mpm.utils import find_project_root, get_namespace_from_project

        project_root = find_project_root()
        if not project_root:
            console.print("[red]Error:[/red] No mpm.toml found. This command requires an mpm-managed project.")
            console.print("[dim]Create a new project with 'mpm new <name>' first.[/dim]")
            raise typer.Exit(1)

        package_type = questionary.select(
            "Package type:",
            choices=[
                Choice("Library (libs/)", "lib"),
                Choice("Application (apps/)", "app"),
            ],
        ).ask()
        if package_type is None:
            raise typer.Abort()

        package_name = questionary.text(
            "Package name:",
            validate=lambda x: len(x) > 0 or "Package name is required",
        ).ask()
        if package_name is None:
            raise typer.Abort()

        description = questionary.text("Description (optional):").ask() or ""

        with_docker = False
        if package_type == "app":
            with_docker = (
                questionary.confirm(
                    "Include Docker support?",
                    default=False,
                ).ask()
                or False
            )

        namespace = get_namespace_from_project(project_root)
        if not namespace:
            console.print("[red]Error:[/red] Could not read namespace from mpm.toml.")
            raise typer.Exit(1)

        add_package(
            package_name,
            package_type,
            description,
            with_docker=with_docker,
            project_root=project_root,
            namespace=namespace,
        )


@add_app.command("lib")
def add_lib(
    name: Annotated[str, typer.Argument(help="Library name")],
    description: Annotated[str, typer.Option("--description", "-d", help="Library description")] = "",
) -> None:
    """Add a new library package to libs/."""
    from mpm.generators.package import add_package
    from mpm.utils import find_project_root, get_namespace_from_project

    project_root = find_project_root()
    if not project_root:
        console.print("[red]Error:[/red] No mpm.toml found. This command requires an mpm-managed project.")
        console.print("[dim]Create a new project with 'mpm new <name>' first.[/dim]")
        raise typer.Exit(1)

    namespace = get_namespace_from_project(project_root)
    if not namespace:
        console.print("[red]Error:[/red] Could not read namespace from mpm.toml.")
        raise typer.Exit(1)

    add_package(name, "lib", description, project_root=project_root, namespace=namespace)


@add_app.command("app")
def add_app_cmd(
    name: Annotated[str, typer.Argument(help="Application name")],
    description: Annotated[str, typer.Option("--description", "-d", help="App description")] = "",
    docker: Annotated[bool, typer.Option("--docker", help="Include Dockerfile")] = False,
) -> None:
    """Add a new application package to apps/."""
    from mpm.generators.package import add_package
    from mpm.utils import find_project_root, get_namespace_from_project

    project_root = find_project_root()
    if not project_root:
        console.print("[red]Error:[/red] No mpm.toml found. This command requires an mpm-managed project.")
        console.print("[dim]Create a new project with 'mpm new <name>' first.[/dim]")
        raise typer.Exit(1)

    namespace = get_namespace_from_project(project_root)
    if not namespace:
        console.print("[red]Error:[/red] Could not read namespace from mpm.toml.")
        raise typer.Exit(1)

    add_package(name, "app", description, with_docker=docker, project_root=project_root, namespace=namespace)


@add_app.command("docker")
def add_docker() -> None:
    """Add Docker configuration to an existing project."""
    from mpm.generators.features import add_docker_feature
    from mpm.utils import find_project_root, load_mpm_config, save_mpm_config

    project_root = find_project_root()
    if not project_root:
        console.print("[red]Error:[/red] No mpm.toml found. This command requires an mpm-managed project.")
        console.print("[dim]Create a new project with 'mpm new <name>' first.[/dim]")
        raise typer.Exit(1)

    mpm_config_path = project_root / "mpm.toml"
    mpm_config = load_mpm_config(mpm_config_path)

    if mpm_config.with_docker:
        console.print("[yellow]Docker is already enabled for this project.[/yellow]")
        return

    add_docker_feature(project_root, mpm_config)

    # Update mpm.toml
    mpm_config.with_docker = True
    save_mpm_config(mpm_config, mpm_config_path)

    console.print("[green]\u2713[/green] Added Docker configuration")


@add_app.command("ci")
def add_ci() -> None:
    """Add GitHub Actions CI to an existing project."""
    from mpm.generators.features import add_ci_feature
    from mpm.utils import find_project_root, load_mpm_config, save_mpm_config

    project_root = find_project_root()
    if not project_root:
        console.print("[red]Error:[/red] No mpm.toml found. This command requires an mpm-managed project.")
        console.print("[dim]Create a new project with 'mpm new <name>' first.[/dim]")
        raise typer.Exit(1)

    mpm_config_path = project_root / "mpm.toml"
    mpm_config = load_mpm_config(mpm_config_path)

    if mpm_config.with_ci:
        console.print("[yellow]CI is already enabled for this project.[/yellow]")
        return

    add_ci_feature(project_root, mpm_config)

    # Update mpm.toml
    mpm_config.with_ci = True
    save_mpm_config(mpm_config, mpm_config_path)

    console.print("[green]\u2713[/green] Added GitHub Actions CI")


@add_app.command("pypi")
def add_pypi() -> None:
    """Add PyPI publishing workflow to an existing project."""
    from mpm.generators.features import add_pypi_feature
    from mpm.utils import find_project_root, load_mpm_config, save_mpm_config

    project_root = find_project_root()
    if not project_root:
        console.print("[red]Error:[/red] No mpm.toml found. This command requires an mpm-managed project.")
        console.print("[dim]Create a new project with 'mpm new <name>' first.[/dim]")
        raise typer.Exit(1)

    mpm_config_path = project_root / "mpm.toml"
    mpm_config = load_mpm_config(mpm_config_path)

    if mpm_config.with_pypi:
        console.print("[yellow]PyPI publishing is already enabled for this project.[/yellow]")
        return

    if not mpm_config.with_ci:
        console.print("[yellow]Warning:[/yellow] CI is not enabled. Consider adding CI first with 'mpm add ci'.")

    add_pypi_feature(project_root, mpm_config)

    # Update mpm.toml
    mpm_config.with_pypi = True
    save_mpm_config(mpm_config, mpm_config_path)

    console.print("[green]\u2713[/green] Added PyPI publishing workflow")


@add_app.command("docs")
def add_docs(
    theme: Annotated[str, typer.Option("--theme", "-t", help="Docs theme: material or shadcn")] = "material",
) -> None:
    """Add MkDocs documentation to an existing project."""
    from mpm.config import DocsTheme
    from mpm.generators.features import add_docs_feature
    from mpm.utils import find_project_root, load_mpm_config, save_mpm_config

    project_root = find_project_root()
    if not project_root:
        console.print("[red]Error:[/red] No mpm.toml found. This command requires an mpm-managed project.")
        console.print("[dim]Create a new project with 'mpm new <name>' first.[/dim]")
        raise typer.Exit(1)

    mpm_config_path = project_root / "mpm.toml"
    mpm_config = load_mpm_config(mpm_config_path)

    if mpm_config.with_docs:
        console.print("[yellow]Docs are already enabled for this project.[/yellow]")
        return

    # Parse theme
    try:
        docs_theme = DocsTheme(theme)
    except ValueError:
        console.print(f"[red]Error:[/red] Invalid theme '{theme}'. Use 'material' or 'shadcn'.")
        raise typer.Exit(1) from None

    add_docs_feature(project_root, mpm_config, docs_theme)

    # Update mpm.toml
    mpm_config.with_docs = True
    mpm_config.docs_theme = docs_theme
    save_mpm_config(mpm_config, mpm_config_path)

    console.print("[green]\u2713[/green] Added MkDocs documentation")
    console.print("[dim]Run 'uv run poe docs' to start the docs server[/dim]")


if __name__ == "__main__":
    app()
