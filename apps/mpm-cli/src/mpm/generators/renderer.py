"""Jinja2 template renderer using importlib.resources."""

import shutil
from importlib.resources import as_file, files
from pathlib import Path
from typing import Any

from jinja2 import BaseLoader, Environment, TemplateNotFound


class PackageTemplateLoader(BaseLoader):
    """Load templates from package resources."""

    def __init__(self, package: str = "mpm.templates"):
        self.package = package

    def get_source(self, environment: Environment, template: str) -> tuple[str, str, Any]:
        try:
            resource = files(self.package).joinpath(template)
            source = resource.read_text()
            return source, template, lambda: True
        except (FileNotFoundError, TypeError, AttributeError) as err:
            raise TemplateNotFound(template) from err


class TemplateRenderer:
    """Render Jinja2 templates from package resources."""

    def __init__(self) -> None:
        self.env = Environment(
            loader=PackageTemplateLoader(),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_path: str, context: dict[str, Any]) -> str:
        """Render a template with the given context."""
        template = self.env.get_template(template_path)
        return template.render(**context)

    def render_to_file(self, template_path: str, output_path: Path, context: dict[str, Any]) -> None:
        """Render a template and write to output file."""
        content = self.render(template_path, context)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)

    def copy_static(self, src_path: str, dest_path: Path) -> None:
        """Copy a static (non-template) file."""
        ref = files("mpm.templates").joinpath(src_path)
        with as_file(ref) as src:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dest_path)
