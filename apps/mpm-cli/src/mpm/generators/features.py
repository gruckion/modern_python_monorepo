"""Feature generators for adding features to existing projects."""

from pathlib import Path

from rich.console import Console

from mpm.config import DocsTheme, MpmConfig, ProjectStructure
from mpm.generators.renderer import TemplateRenderer

console = Console()


def add_docker_feature(project_root: Path, config: MpmConfig) -> None:
    """Add Docker configuration to an existing project.

    For monorepo:
    - If apps with Dockerfiles exist, generates docker-compose.yml and docker-bake.hcl
    - Always generates .dockerignore

    For single package:
    - Generates Dockerfile, docker-compose.yml, docker-bake.hcl, and .dockerignore
    """
    renderer = TemplateRenderer()

    ctx = {
        "project_slug": config.project_slug,
        "namespace": config.project_name,
        "python_version": config.python_version,
        "structure": config.structure,
        "with_samples": config.with_samples,
        "github_owner": config.github_owner,
    }

    # Always generate .dockerignore
    renderer.copy_static("docker/.dockerignore", project_root / ".dockerignore")
    console.print("[dim]Created .dockerignore[/dim]")

    if config.structure == ProjectStructure.SINGLE:
        # Single package: generate Dockerfile at root
        renderer.render_to_file("docker/Dockerfile.jinja", project_root / "Dockerfile", ctx)
        renderer.render_to_file("docker/docker-compose.yml.jinja", project_root / "docker-compose.yml", ctx)
        renderer.render_to_file("docker/docker-bake.hcl.jinja", project_root / "docker-bake.hcl", ctx)
        console.print("[dim]Created Dockerfile, docker-compose.yml, docker-bake.hcl[/dim]")
    else:
        # Monorepo: check for existing apps with Dockerfiles
        apps_dir = project_root / "apps"
        apps_with_docker = []

        if apps_dir.exists():
            for app_dir in apps_dir.iterdir():
                if app_dir.is_dir() and (app_dir / "Dockerfile").exists():
                    apps_with_docker.append(app_dir.name)

        if apps_with_docker:
            # Generate docker-compose.yml and docker-bake.hcl referencing existing apps
            ctx["apps_with_docker"] = apps_with_docker
            # For samples, the app is 'printer'
            if config.with_samples or apps_with_docker:
                renderer.render_to_file("docker/docker-compose.yml.jinja", project_root / "docker-compose.yml", ctx)
                renderer.render_to_file("docker/docker-bake.hcl.jinja", project_root / "docker-bake.hcl", ctx)
                console.print(f"[dim]Created docker-compose.yml, docker-bake.hcl for apps: {apps_with_docker}[/dim]")
        else:
            console.print("[yellow]Note:[/yellow] No apps with Dockerfiles found.")
            console.print("[dim]Add apps with 'mpm add app <name> --docker' to generate docker-compose.yml[/dim]")


def add_ci_feature(project_root: Path, config: MpmConfig) -> None:
    """Add GitHub Actions CI to an existing project."""
    renderer = TemplateRenderer()

    ctx = {
        "structure": config.structure,
        "project_slug": config.project_slug,
        "namespace": config.project_name,
        "python_version": config.python_version,
    }

    workflows_dir = project_root / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    renderer.render_to_file("ci/pr.yml.jinja", workflows_dir / "pr.yml", ctx)
    console.print("[dim]Created .github/workflows/pr.yml[/dim]")


def add_pypi_feature(project_root: Path, config: MpmConfig) -> None:
    """Add PyPI publishing workflow to an existing project."""
    renderer = TemplateRenderer()

    ctx = {
        "structure": config.structure,
        "project_slug": config.project_slug,
        "namespace": config.project_name,
        "python_version": config.python_version,
        "with_samples": config.with_samples,
    }

    workflows_dir = project_root / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    renderer.render_to_file("ci/release.yml.jinja", workflows_dir / "release.yml", ctx)
    console.print("[dim]Created .github/workflows/release.yml[/dim]")


def add_docs_feature(project_root: Path, config: MpmConfig, theme: DocsTheme = DocsTheme.MATERIAL) -> None:
    """Add MkDocs documentation to an existing project.

    Args:
        project_root: Path to project root
        config: MpmConfig configuration
        theme: Documentation theme (material or shadcn)
    """
    import subprocess

    renderer = TemplateRenderer()

    ctx = {
        "project_slug": config.project_slug,
        "project_description": config.project_description,
        "github_owner": config.github_owner,
        "structure": config.structure,
        "namespace": config.project_name,
        "python_version": config.python_version,
    }

    # Update pyproject.toml with docs dependencies
    _update_pyproject_toml_for_docs(project_root, theme)
    console.print("[dim]Updated pyproject.toml with docs dependencies[/dim]")

    # Run uv sync to install dependencies
    console.print("[dim]Running uv sync to install dependencies...[/dim]")
    subprocess.run(["uv", "sync", "--quiet"], cwd=project_root, capture_output=True)

    # Generate mkdocs.yml using appropriate theme template
    theme_dir = f"docs/{theme.value}"
    renderer.render_to_file(f"{theme_dir}/mkdocs.yml.jinja", project_root / "mkdocs.yml", ctx)
    console.print("[dim]Created mkdocs.yml[/dim]")

    # Create docs/index.md
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)

    index_content = f"""# Welcome to {config.project_slug}

{config.project_description or "Documentation for " + config.project_slug}

## Getting Started

TODO: Add getting started guide.
"""
    (docs_dir / "index.md").write_text(index_content)
    console.print("[dim]Created docs/index.md[/dim]")


def _update_pyproject_toml_for_docs(project_root: Path, theme: DocsTheme) -> None:
    """Update pyproject.toml to add docs dependencies and poe tasks.

    This uses tomli_w to rewrite the TOML file, which means comments are lost.
    However, since mpm generates pyproject.toml, this is acceptable.
    """
    import tomllib

    import tomli_w

    pyproject_path = project_root / "pyproject.toml"

    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    # Add mkdocs dependencies to dependency-groups.dev
    dev_deps = pyproject.setdefault("dependency-groups", {}).setdefault("dev", [])

    # Define docs dependencies based on theme
    if theme == DocsTheme.MATERIAL:
        docs_deps = [
            "mkdocs>=1.6.0",
            "mkdocs-material>=9.5.0",
            "mkdocs-mermaid2-plugin>=1.1.0",
        ]
    else:  # shadcn
        docs_deps = [
            "mkdocs>=1.6.0",
            "mkdocs-terminal>=4.0.0",
            "mkdocs-mermaid2-plugin>=1.1.0",
        ]

    # Add dependencies that aren't already present
    for dep in docs_deps:
        dep_name = dep.split(">=")[0].split("[")[0]
        if not any(dep_name in existing for existing in dev_deps):
            dev_deps.append(dep)

    # Add poe docs tasks if poe.tasks exists
    if "tool" in pyproject and "poe" in pyproject["tool"] and "tasks" in pyproject["tool"]["poe"]:
        tasks = pyproject["tool"]["poe"]["tasks"]

        # Add docs tasks if they don't exist
        if "docs" not in tasks:
            tasks["docs"] = "mkdocs serve"
        if "docs-build" not in tasks:
            tasks["docs-build"] = "mkdocs build"

    # Write back
    with open(pyproject_path, "wb") as f:
        tomli_w.dump(pyproject, f)
