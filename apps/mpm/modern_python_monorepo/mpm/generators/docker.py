"""Docker configuration generator for MPM CLI."""

from pathlib import Path

from rich.console import Console

from modern_python_monorepo.mpm.config import TemplateContext
from modern_python_monorepo.mpm.generators.renderer import get_renderer

console = Console()


def generate_docker(ctx: TemplateContext, output_dir: Path) -> None:
    """Generate Docker configuration files.

    Args:
        ctx: Template context
        output_dir: Output directory for the project
    """
    renderer = get_renderer()

    # docker-compose.yml
    renderer.render_to_file(
        "docker/docker-compose.yml.jinja",
        output_dir / "docker-compose.yml",
        ctx,
    )

    # docker-bake.hcl
    renderer.render_to_file(
        "docker/docker-bake.hcl.jinja",
        output_dir / "docker-bake.hcl",
        ctx,
    )

    # .dockerignore
    renderer.copy_static(
        "docker/.dockerignore",
        output_dir / ".dockerignore",
    )

    console.print("[green]✓[/green] Generated Docker configuration")
