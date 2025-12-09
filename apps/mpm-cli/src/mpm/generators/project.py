"""Project generator - creates the full project structure."""

import subprocess
from datetime import datetime
from pathlib import Path

from rich.console import Console

from mpm.config import DocsTheme, ProjectConfig, ProjectStructure
from mpm.generators.renderer import TemplateRenderer

console = Console()


def generate_project(config: ProjectConfig, output_path: Path) -> None:
    """Generate a complete project from configuration."""
    renderer = TemplateRenderer()
    context = config.model_dump()
    # Add namespace to context (it's a property, not a field)
    context["namespace"] = config.namespace
    # Add current year for LICENSE
    context["current_year"] = datetime.now().year

    console.print(f"[dim]Creating project at {output_path}...[/dim]")

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate base files (always)
    _generate_base_files(renderer, output_path, context)

    # Generate structure-specific files
    if config.structure == ProjectStructure.MONOREPO:
        _generate_monorepo_structure(renderer, output_path, context)
        if config.with_samples:
            _generate_sample_packages(renderer, output_path, context)
    else:
        _generate_single_package(renderer, output_path, context)

    # Generate optional features
    if config.with_precommit:
        _generate_precommit(renderer, output_path, context)

    if config.with_docker:
        _generate_docker_files(renderer, output_path, context)

    if config.with_ci:
        _generate_ci_files(renderer, output_path, context, config.with_pypi)

    if config.with_docs:
        _generate_docs(renderer, output_path, context, config.docs_theme)

    # Generate VS Code configuration
    _generate_vscode_config(renderer, output_path, context)

    # Initialize git
    if config.init_git:
        _init_git(output_path)

    # Run uv sync to install dependencies
    if config.auto_sync:
        _run_uv_sync(output_path, config.structure)

    console.print("[green]\u2713[/green] Project generated successfully")


def _generate_base_files(renderer: TemplateRenderer, output: Path, ctx: dict) -> None:
    """Generate base project files."""
    renderer.render_to_file("base/pyproject.toml.jinja", output / "pyproject.toml", ctx)
    renderer.render_to_file("base/README.md.jinja", output / "README.md", ctx)
    renderer.render_to_file("base/.python-version.jinja", output / ".python-version", ctx)
    renderer.copy_static("base/.gitignore", output / ".gitignore")

    if ctx.get("license_type") and ctx["license_type"] != "none":
        renderer.render_to_file("base/LICENSE.jinja", output / "LICENSE", ctx)


def _generate_monorepo_structure(_renderer: TemplateRenderer, output: Path, _ctx: dict) -> None:
    """Generate monorepo directory structure."""
    (output / "libs").mkdir(exist_ok=True)
    (output / "apps").mkdir(exist_ok=True)


def _generate_sample_packages(renderer: TemplateRenderer, output: Path, ctx: dict) -> None:
    """Generate sample greeter lib and printer app."""
    from mpm.generators.package import generate_app_package, generate_lib_package

    generate_lib_package(
        renderer,
        output,
        package_name="greeter",
        namespace=ctx["namespace"],
        ctx=ctx,
        is_sample=True,
    )
    generate_app_package(
        renderer,
        output,
        package_name="printer",
        namespace=ctx["namespace"],
        ctx=ctx,
        with_docker=ctx.get("with_docker", False),
        is_sample=True,
    )


def _generate_single_package(renderer: TemplateRenderer, output: Path, ctx: dict) -> None:
    """Generate single package structure."""
    src_dir = output / "src" / ctx["namespace"]
    src_dir.mkdir(parents=True, exist_ok=True)
    renderer.render_to_file("single/__init__.py.jinja", src_dir / "__init__.py", ctx)
    (src_dir / "py.typed").touch()

    # Add tests directory for single package
    tests_dir = output / "tests"
    tests_dir.mkdir(exist_ok=True)
    renderer.render_to_file("single/test_import.py.jinja", tests_dir / "test_import.py", ctx)


def _generate_precommit(renderer: TemplateRenderer, output: Path, _ctx: dict) -> None:
    """Generate pre-commit configuration."""
    renderer.copy_static("tooling/.pre-commit-config.yaml", output / ".pre-commit-config.yaml")


def _generate_docker_files(renderer: TemplateRenderer, output: Path, ctx: dict) -> None:
    """Generate Docker configuration files."""
    structure = ctx.get("structure")
    is_monorepo = structure == ProjectStructure.MONOREPO or (
        hasattr(structure, "value") and structure.value == "monorepo"
    )
    has_samples = ctx.get("with_samples", False)

    # Always generate .dockerignore (useful even if user adds docker later)
    renderer.copy_static("docker/.dockerignore", output / ".dockerignore")

    # For single package mode, generate root Dockerfile and docker-compose/bake
    if not is_monorepo:
        renderer.render_to_file("docker/Dockerfile.jinja", output / "Dockerfile", ctx)
        renderer.render_to_file("docker/docker-compose.yml.jinja", output / "docker-compose.yml", ctx)
        renderer.render_to_file("docker/docker-bake.hcl.jinja", output / "docker-bake.hcl", ctx)
    # For monorepo WITH samples, generate docker-compose/bake (Dockerfile is in apps/printer)
    elif has_samples:
        renderer.render_to_file("docker/docker-compose.yml.jinja", output / "docker-compose.yml", ctx)
        renderer.render_to_file("docker/docker-bake.hcl.jinja", output / "docker-bake.hcl", ctx)
    # For monorepo WITHOUT samples, skip docker-compose/bake (no Dockerfiles exist yet)
    # User can add apps with `mpm add app <name> --docker` later


def _generate_ci_files(renderer: TemplateRenderer, output: Path, ctx: dict, with_pypi: bool) -> None:
    """Generate GitHub Actions workflows."""
    workflows = output / ".github" / "workflows"
    workflows.mkdir(parents=True, exist_ok=True)
    renderer.render_to_file("ci/pr.yml.jinja", workflows / "pr.yml", ctx)
    if with_pypi:
        renderer.render_to_file("ci/release.yml.jinja", workflows / "release.yml", ctx)


def _generate_docs(renderer: TemplateRenderer, output: Path, ctx: dict, theme: DocsTheme) -> None:
    """Generate MkDocs documentation.

    Uses `mkdocs new` to create the initial scaffold (docs/index.md),
    then replaces mkdocs.yml with our customized theme configuration.
    """
    theme_dir = f"docs/{theme.value}"

    # First, ensure dependencies are synced so mkdocs is available
    subprocess.run(
        ["uv", "sync", "--quiet"],
        cwd=output,
        capture_output=True,
    )

    # Use mkdocs new to create the docs/ directory and initial index.md
    # This ensures compatibility with MkDocs conventions
    result = subprocess.run(
        ["uv", "run", "mkdocs", "new", "."],
        cwd=output,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        console.print("[green]\u2713[/green] Initialized docs with mkdocs")
    else:
        console.print(f"[yellow]\u26a0[/yellow] mkdocs new failed: {result.stderr}")

    # Replace mkdocs.yml with our customized theme configuration
    # (mkdocs new creates a minimal one, we need our full config)
    renderer.render_to_file(f"{theme_dir}/mkdocs.yml.jinja", output / "mkdocs.yml", ctx)


def _generate_vscode_config(renderer: TemplateRenderer, output: Path, ctx: dict) -> None:
    """Generate VS Code configuration files."""
    vscode_dir = output / ".vscode"
    vscode_dir.mkdir(exist_ok=True)
    renderer.copy_static("vscode/extensions.json", vscode_dir / "extensions.json")
    renderer.render_to_file("vscode/settings.json.jinja", vscode_dir / "settings.json", ctx)


def _init_git(output: Path) -> None:
    """Initialize git repository."""
    try:
        subprocess.run(["git", "init"], cwd=output, capture_output=True, check=True)
        console.print("[green]\u2713[/green] Initialized git repository")
    except subprocess.CalledProcessError:
        console.print("[yellow]\u26a0[/yellow] Failed to initialize git repository")


def _run_uv_sync(output: Path, structure: ProjectStructure) -> None:
    """Run uv sync to install dependencies."""
    try:
        # For monorepos, use --all-packages to sync all workspace members
        if structure == ProjectStructure.MONOREPO:
            cmd = ["uv", "sync", "--all-packages"]
        else:
            cmd = ["uv", "sync"]

        console.print("[dim]Running uv sync...[/dim]")
        result = subprocess.run(cmd, cwd=output, capture_output=True, text=True)
        if result.returncode == 0:
            console.print("[green]\u2713[/green] Dependencies installed")
        else:
            console.print(f"[yellow]\u26a0[/yellow] uv sync failed: {result.stderr}")
    except FileNotFoundError:
        console.print("[yellow]\u26a0[/yellow] uv not found, skipping dependency installation")
