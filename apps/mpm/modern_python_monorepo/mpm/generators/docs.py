"""Documentation generator for MPM CLI."""

from pathlib import Path

from rich.console import Console

from modern_python_monorepo.mpm.config import TemplateContext
from modern_python_monorepo.mpm.generators.renderer import get_renderer

console = Console()


def generate_docs(
    ctx: TemplateContext,
    output_dir: Path,
    theme: str = "material",
) -> None:
    """Generate MkDocs documentation.

    Args:
        ctx: Template context
        output_dir: Output directory for the project
        theme: MkDocs theme ("material" or "shadcn")
    """
    renderer = get_renderer()
    template_base = f"docs/{theme}"

    # Create docs directory
    docs_dir = output_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    (docs_dir / "development").mkdir(exist_ok=True)
    (docs_dir / "architecture").mkdir(exist_ok=True)
    (docs_dir / "api").mkdir(exist_ok=True)

    # mkdocs.yml
    renderer.render_to_file(
        f"{template_base}/mkdocs.yml.jinja",
        output_dir / "mkdocs.yml",
        ctx,
    )

    # Main documentation pages
    renderer.render_to_file(
        f"{template_base}/docs/index.md.jinja",
        docs_dir / "index.md",
        ctx,
    )
    renderer.render_to_file(
        f"{template_base}/docs/getting-started.md.jinja",
        docs_dir / "getting-started.md",
        ctx,
    )

    # Development docs
    renderer.render_to_file(
        f"{template_base}/docs/development/setup.md.jinja",
        docs_dir / "development" / "setup.md",
        ctx,
    )
    renderer.copy_static(
        f"{template_base}/docs/development/commands.md",
        docs_dir / "development" / "commands.md",
    )

    # Docker docs (if enabled)
    if ctx.with_docker:
        renderer.copy_static(
            f"{template_base}/docs/development/docker.md",
            docs_dir / "development" / "docker.md",
        )

    # Architecture docs
    renderer.copy_static(
        f"{template_base}/docs/architecture/overview.md",
        docs_dir / "architecture" / "overview.md",
    )

    # API docs
    renderer.render_to_file(
        f"{template_base}/docs/api/index.md.jinja",
        docs_dir / "api" / "index.md",
        ctx,
    )

    # Contributing
    renderer.copy_static(
        f"{template_base}/docs/contributing.md",
        docs_dir / "contributing.md",
    )

    console.print(f"[green]✓[/green] Generated MkDocs documentation ({theme} theme)")
