"""Interactive prompts for MPM CLI using questionary."""

import questionary
from questionary import Choice

from modern_python_monorepo.mpm.config import (
    DocsTheme,
    FeatureSet,
    LicenseType,
    PackageConfig,
    PackageType,
    ProjectConfig,
    ProjectStructure,
    PythonVersion,
)


def prompt_project_name(default: str = "") -> str:
    """Prompt for project name.

    Args:
        default: Default project name

    Returns:
        Validated project name
    """
    name = questionary.text(
        "Project name:",
        default=default,
        validate=lambda x: len(x) > 0 or "Project name cannot be empty",
    ).ask()

    if name is None:
        raise KeyboardInterrupt

    return name


def prompt_project_structure() -> ProjectStructure:
    """Prompt for project structure type.

    Returns:
        Selected project structure
    """
    result = questionary.select(
        "Project structure:",
        choices=[
            Choice("Monorepo (libs/ and apps/ workspaces)", ProjectStructure.MONOREPO),
            Choice("Single package", ProjectStructure.SINGLE),
        ],
    ).ask()

    if result is None:
        raise KeyboardInterrupt

    return result


def prompt_python_version() -> PythonVersion:
    """Prompt for Python version.

    Returns:
        Selected Python version
    """
    result = questionary.select(
        "Python version requirement:",
        choices=[
            Choice("3.13+", PythonVersion.PY313),
            Choice("3.12+", PythonVersion.PY312),
            Choice("3.11+", PythonVersion.PY311),
        ],
    ).ask()

    if result is None:
        raise KeyboardInterrupt

    return result


def prompt_features() -> FeatureSet:
    """Prompt for features to include.

    Returns:
        Feature set configuration
    """
    choices = [
        Choice("Ruff (linting & formatting)", value="ruff", checked=True),
        Choice("ty (type checking)", value="ty", checked=True),
        Choice("pytest (testing)", value="pytest", checked=True),
        Choice("poethepoet (task runner)", value="poethepoet", checked=True),
        Choice("Pre-commit hooks (prek)", value="pre_commit", checked=True),
        Choice("GitHub Actions CI", value="github_actions", checked=False),
        Choice("PyPI publishing workflow", value="pypi_publish", checked=False),
        Choice("Docker support", value="docker", checked=False),
    ]

    selected = questionary.checkbox(
        "Select features to include:",
        choices=choices,
    ).ask()

    if selected is None:
        raise KeyboardInterrupt

    return FeatureSet(
        ruff="ruff" in selected,
        ty="ty" in selected,
        pytest="pytest" in selected,
        poethepoet="poethepoet" in selected,
        pre_commit="pre_commit" in selected,
        github_actions="github_actions" in selected,
        pypi_publish="pypi_publish" in selected,
        docker="docker" in selected,
    )


def prompt_docs() -> tuple[bool, DocsTheme]:
    """Prompt for documentation options.

    Returns:
        Tuple of (include_docs, theme)
    """
    result = questionary.select(
        "Include documentation site (MkDocs)?",
        choices=[
            Choice("Yes - Material theme (recommended, enterprise-ready)", value="material"),
            Choice("Yes - shadcn theme (modern UI aesthetic)", value="shadcn"),
            Choice("No", value="none"),
        ],
    ).ask()

    if result is None:
        raise KeyboardInterrupt

    if result == "none":
        return False, DocsTheme.MATERIAL

    return True, DocsTheme(result)


def prompt_samples() -> bool:
    """Prompt for sample packages.

    Returns:
        Whether to include sample packages
    """
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


def prompt_license() -> LicenseType:
    """Prompt for license type.

    Returns:
        Selected license type
    """
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


def prompt_init_git() -> bool:
    """Prompt for git initialization.

    Returns:
        Whether to initialize git
    """
    result = questionary.confirm(
        "Initialize git repository?",
        default=True,
    ).ask()

    if result is None:
        raise KeyboardInterrupt

    return result


def prompt_project_config(
    name: str | None = None,
    use_defaults: bool = False,
) -> ProjectConfig:
    """Run interactive prompts for project configuration.

    Args:
        name: Optional project name (skips prompt if provided)
        use_defaults: If True, use default values for all options

    Returns:
        Complete project configuration
    """
    # Project name
    project_name = name or prompt_project_name()

    if use_defaults:
        # Use defaults for everything
        return ProjectConfig(
            project_name=project_name,
            structure=ProjectStructure.MONOREPO,
            python_version=PythonVersion.PY313,
            features=FeatureSet(),
            with_samples=True,
            docs_theme=DocsTheme.MATERIAL,
            license_type=LicenseType.MIT,
            init_git=True,
        )

    # Interactive prompts
    structure = prompt_project_structure()
    python_version = prompt_python_version()
    features = prompt_features()
    include_docs, docs_theme = prompt_docs()
    features.docs = include_docs

    with_samples = prompt_samples() if structure == ProjectStructure.MONOREPO else False
    license_type = prompt_license()
    init_git = prompt_init_git()

    return ProjectConfig(
        project_name=project_name,
        structure=structure,
        python_version=python_version,
        features=features,
        with_samples=with_samples,
        docs_theme=docs_theme,
        license_type=license_type,
        init_git=init_git,
    )


def prompt_package_type() -> PackageType:
    """Prompt for package type.

    Returns:
        Selected package type
    """
    result = questionary.select(
        "Package type:",
        choices=[
            Choice("Library (libs/)", PackageType.LIB),
            Choice("Application (apps/)", PackageType.APP),
        ],
    ).ask()

    if result is None:
        raise KeyboardInterrupt

    return result


def prompt_package_name() -> str:
    """Prompt for package name.

    Returns:
        Package name
    """
    name = questionary.text(
        "Package name:",
        validate=lambda x: len(x) > 0 or "Package name cannot be empty",
    ).ask()

    if name is None:
        raise KeyboardInterrupt

    return name


def prompt_package_description() -> str:
    """Prompt for package description.

    Returns:
        Package description
    """
    result = questionary.text(
        "Description (optional):",
        default="",
    ).ask()

    if result is None:
        raise KeyboardInterrupt

    return result


def prompt_include_docker() -> bool:
    """Prompt for Docker support.

    Returns:
        Whether to include Docker
    """
    result = questionary.confirm(
        "Include Docker support?",
        default=False,
    ).ask()

    if result is None:
        raise KeyboardInterrupt

    return result


def prompt_package_config(
    namespace: str,
    python_requires: str = ">=3.13",
    package_type: PackageType | None = None,
    package_name: str | None = None,
    with_docker: bool | None = None,
) -> PackageConfig:
    """Run interactive prompts for package configuration.

    Args:
        namespace: Project namespace
        python_requires: Python version requirement
        package_type: Optional package type (skips prompt if provided)
        package_name: Optional package name (skips prompt if provided)
        with_docker: Optional Docker flag (skips prompt if provided for apps)

    Returns:
        Complete package configuration
    """
    pkg_type = package_type or prompt_package_type()
    name = package_name or prompt_package_name()
    description = prompt_package_description()

    docker = False
    if pkg_type == PackageType.APP:
        docker = with_docker if with_docker is not None else prompt_include_docker()

    return PackageConfig(
        package_name=name,
        package_type=pkg_type,
        description=description,
        with_docker=docker,
        namespace=namespace,
        python_requires=python_requires,
    )
