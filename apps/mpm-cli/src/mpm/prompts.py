"""Questionary prompts for interactive mode."""

import questionary
from questionary import Choice

from mpm.config import (
    DocsTheme,
    LicenseType,
    ProjectConfig,
    ProjectStructure,
    PythonVersion,
)


def prompt_project_name() -> str:
    """Prompt for project name."""
    result = questionary.text(
        "Project name:",
        validate=lambda x: len(x) > 0 or "Project name is required",
    ).ask()
    if result is None:
        raise KeyboardInterrupt
    return result


def prompt_structure() -> ProjectStructure:
    """Prompt for project structure."""
    choice = questionary.select(
        "Project structure:",
        choices=[
            Choice("Monorepo (libs/ and apps/ workspaces)", ProjectStructure.MONOREPO),
            Choice("Single package", ProjectStructure.SINGLE),
        ],
    ).ask()
    if choice is None:
        raise KeyboardInterrupt
    return choice


def prompt_python_version() -> PythonVersion:
    """Prompt for Python version."""
    result = questionary.select(
        "Python version requirement:",
        choices=[
            Choice("3.11+", PythonVersion.PY311),
            Choice("3.12+", PythonVersion.PY312),
            Choice("3.13+", PythonVersion.PY313),
        ],
        default=PythonVersion.PY313,
    ).ask()
    if result is None:
        raise KeyboardInterrupt
    return result


def prompt_features() -> dict[str, bool]:
    """Prompt for features to include."""
    features = questionary.checkbox(
        "Select features to include:",
        choices=[
            Choice("Ruff (linting & formatting)", checked=True, value="ruff"),
            Choice("ty (type checking)", checked=True, value="ty"),
            Choice("pytest (testing)", checked=True, value="pytest"),
            Choice("poethepoet (task runner)", checked=True, value="poe"),
            Choice("Pre-commit hooks", checked=True, value="precommit"),
            Choice("GitHub Actions CI", checked=False, value="ci"),
            Choice("PyPI publishing workflow", checked=False, value="pypi"),
            Choice("Docker support", checked=False, value="docker"),
        ],
    ).ask()
    if features is None:
        raise KeyboardInterrupt
    return {f: f in features for f in ["ruff", "ty", "pytest", "poe", "precommit", "ci", "pypi", "docker"]}


def prompt_samples() -> bool:
    """Prompt for sample packages."""
    result = questionary.select(
        "Include sample packages?",
        choices=[
            Choice("Yes (greeter lib + printer app)", True),
            Choice("No (empty structure)", False),
        ],
    ).ask()
    if result is None:
        raise KeyboardInterrupt
    return result


def prompt_docs() -> tuple[bool, DocsTheme | None]:
    """Prompt for documentation setup."""
    choice = questionary.select(
        "Include documentation site (MkDocs)?",
        choices=[
            Choice("Yes - Material theme (recommended)", "material"),
            Choice("Yes - shadcn theme (modern UI)", "shadcn"),
            Choice("No", "none"),
        ],
    ).ask()
    if choice is None:
        raise KeyboardInterrupt
    if choice == "none":
        return False, None
    return True, DocsTheme(choice)


def prompt_license() -> LicenseType:
    """Prompt for license type."""
    result = questionary.select(
        "License:",
        choices=[
            Choice("MIT", LicenseType.MIT),
            Choice("Apache-2.0", LicenseType.APACHE),
            Choice("GPL-3.0", LicenseType.GPL),
            Choice("None", LicenseType.NONE),
        ],
    ).ask()
    if result is None:
        raise KeyboardInterrupt
    return result


def gather_project_config(name: str | None = None) -> ProjectConfig:
    """Gather all configuration via interactive prompts."""
    project_name = name or prompt_project_name()
    project_slug = project_name.replace("_", "-").lower()

    structure = prompt_structure()
    python_version = prompt_python_version()
    features = prompt_features()
    with_samples = prompt_samples() if structure == ProjectStructure.MONOREPO else False
    with_docs, docs_theme = prompt_docs()
    license_type = prompt_license()

    return ProjectConfig(
        project_name=project_name.replace("-", "_"),
        project_slug=project_slug,
        structure=structure,
        python_version=python_version,
        with_samples=with_samples,
        with_docker=features.get("docker", False),
        with_ci=features.get("ci", False),
        with_pypi=features.get("pypi", False),
        with_docs=with_docs,
        docs_theme=docs_theme or DocsTheme.MATERIAL,
        with_precommit=features.get("precommit", True),
        license_type=license_type,
    )
