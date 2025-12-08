"""CI/CD configuration generator for MPM CLI."""

from pathlib import Path

from rich.console import Console

from modern_python_monorepo.mpm.config import TemplateContext
from modern_python_monorepo.mpm.generators.renderer import get_renderer

console = Console()


def generate_ci(
    ctx: TemplateContext,
    output_dir: Path,
    include_pypi: bool = False,
) -> None:
    """Generate GitHub Actions CI/CD configuration.

    Args:
        ctx: Template context
        output_dir: Output directory for the project
        include_pypi: Whether to include PyPI publishing workflow
    """
    renderer = get_renderer()

    # Create workflows directory
    workflows_dir = output_dir / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    # PR workflow
    renderer.render_to_file(
        "ci/.github/workflows/pr.yml.jinja",
        workflows_dir / "pr.yml",
        ctx,
    )

    # Release workflow (if PyPI publishing enabled)
    if include_pypi:
        renderer.render_to_file(
            "ci/.github/workflows/release.yml.jinja",
            workflows_dir / "release.yml",
            ctx,
        )

    console.print("[green]✓[/green] Generated GitHub Actions workflows")
