"""Code generation modules for MPM CLI."""

from modern_python_monorepo.mpm.generators.ci import generate_ci
from modern_python_monorepo.mpm.generators.docker import generate_docker
from modern_python_monorepo.mpm.generators.docs import generate_docs
from modern_python_monorepo.mpm.generators.package import generate_package
from modern_python_monorepo.mpm.generators.project import generate_project
from modern_python_monorepo.mpm.generators.renderer import TemplateRenderer

__all__ = [
    "TemplateRenderer",
    "generate_ci",
    "generate_docker",
    "generate_docs",
    "generate_package",
    "generate_project",
]
