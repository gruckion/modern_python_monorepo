"""Jinja2 template renderer for MPM CLI."""

import shutil
from collections.abc import Callable
from importlib.resources import as_file, files
from pathlib import Path
from typing import Any

from jinja2 import BaseLoader, Environment, TemplateNotFound

from modern_python_monorepo.mpm.config import TemplateContext


class PackageTemplateLoader(BaseLoader):
    """Load templates from package resources."""

    def __init__(self, package: str = "modern_python_monorepo.mpm.templates"):
        self.package = package

    def get_source(
        self,
        environment: Environment,
        template: str,
    ) -> tuple[str, str | None, Callable[[], bool] | None]:
        """Load template source from package resources."""
        try:
            source = files(self.package).joinpath(template).read_text()
            return source, template, lambda: True
        except (FileNotFoundError, TypeError) as e:
            raise TemplateNotFound(template) from e


class TemplateRenderer:
    """Render Jinja2 templates from package resources."""

    def __init__(self):
        self.env = Environment(
            loader=PackageTemplateLoader(),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        # Add custom filters
        self.env.filters["to_python_name"] = self._to_python_name

    @staticmethod
    def _to_python_name(value: str) -> str:
        """Convert string to valid Python identifier."""
        return value.replace("-", "_").lower()

    def render(self, template_path: str, context: dict[str, Any] | TemplateContext) -> str:
        """Render a template with the given context.

        Args:
            template_path: Path to template relative to templates/ directory
            context: Template context (dict or TemplateContext)

        Returns:
            Rendered template content
        """
        template = self.env.get_template(template_path)
        if isinstance(context, TemplateContext):
            context = context.model_dump()
        return template.render(**context)

    def render_to_file(
        self,
        template_path: str,
        output_path: Path,
        context: dict[str, Any] | TemplateContext,
    ) -> None:
        """Render a template and write to output file.

        Args:
            template_path: Path to template relative to templates/ directory
            output_path: Destination file path
            context: Template context
        """
        content = self.render(template_path, context)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)

    def copy_static(self, src_path: str, dest_path: Path) -> None:
        """Copy a static (non-template) file.

        Args:
            src_path: Source path relative to templates/ directory
            dest_path: Destination file path
        """
        ref = files("modern_python_monorepo.mpm.templates").joinpath(src_path)
        with as_file(ref) as src:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dest_path)

    def copy_directory(
        self,
        src_dir: str,
        dest_dir: Path,
        context: dict[str, Any] | TemplateContext,
        exclude_patterns: list[str] | None = None,
    ) -> None:
        """Copy a directory, rendering any .jinja templates.

        Args:
            src_dir: Source directory relative to templates/
            dest_dir: Destination directory
            context: Template context for rendering
            exclude_patterns: Glob patterns to exclude
        """
        if isinstance(context, TemplateContext):
            context = context.model_dump()

        exclude_patterns = exclude_patterns or []
        templates_base = files("modern_python_monorepo.mpm.templates")
        src_ref = templates_base.joinpath(src_dir)

        with as_file(src_ref) as src_path:
            if not src_path.is_dir():
                return

            for item in src_path.rglob("*"):
                if item.is_dir():
                    continue

                # Check exclusions
                rel_path = item.relative_to(src_path)
                if any(rel_path.match(pattern) for pattern in exclude_patterns):
                    continue

                # Calculate destination path
                dest_file = dest_dir / self._transform_path(rel_path, context)

                if item.suffix == ".jinja":
                    # Render template
                    template_rel = f"{src_dir}/{rel_path}"
                    dest_file = dest_file.with_suffix("")  # Remove .jinja
                    self.render_to_file(template_rel, dest_file, context)
                else:
                    # Copy static file
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(item, dest_file)

    def _transform_path(self, path: Path, context: dict[str, Any]) -> Path:
        """Transform path placeholders to actual values.

        Replaces:
            __package__ -> context["package_name"]
            __namespace__ -> context["namespace"]
        """
        parts = []
        for part in path.parts:
            if part == "__package__":
                parts.append(context.get("package_name", part))
            elif part == "__namespace__":
                parts.append(context.get("namespace", part))
            else:
                parts.append(part)
        return Path(*parts) if parts else path


# Singleton instance for convenience
_renderer: TemplateRenderer | None = None


def get_renderer() -> TemplateRenderer:
    """Get the singleton template renderer instance."""
    global _renderer
    if _renderer is None:
        _renderer = TemplateRenderer()
    return _renderer
