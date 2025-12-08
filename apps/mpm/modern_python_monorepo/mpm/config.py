"""Pydantic configuration models for MPM CLI."""

from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class ProjectStructure(str, Enum):
    """Project structure type."""

    MONOREPO = "monorepo"
    SINGLE = "single"


class PythonVersion(str, Enum):
    """Supported Python versions."""

    PY311 = "3.11"
    PY312 = "3.12"
    PY313 = "3.13"


class LicenseType(str, Enum):
    """Supported license types."""

    MIT = "MIT"
    APACHE = "Apache-2.0"
    GPL = "GPL-3.0"
    NONE = "none"


class DocsTheme(str, Enum):
    """MkDocs theme options."""

    MATERIAL = "material"
    SHADCN = "shadcn"


class PackageType(str, Enum):
    """Package type for add command."""

    LIB = "lib"
    APP = "app"


class FeatureSet(BaseModel):
    """Feature flags for project generation."""

    ruff: bool = Field(default=True, description="Include Ruff linting & formatting")
    ty: bool = Field(default=True, description="Include ty type checking")
    pytest: bool = Field(default=True, description="Include pytest testing")
    poethepoet: bool = Field(default=True, description="Include poethepoet task runner")
    pre_commit: bool = Field(default=True, description="Include pre-commit/prek hooks")
    github_actions: bool = Field(default=False, description="Include GitHub Actions CI")
    pypi_publish: bool = Field(default=False, description="Include PyPI publishing workflow")
    docker: bool = Field(default=False, description="Include Docker configuration")
    docs: bool = Field(default=False, description="Include MkDocs documentation")


class ProjectConfig(BaseModel):
    """Configuration for new project generation."""

    # Required fields
    project_name: str = Field(..., description="Project name (used for directory)")

    # Structure
    structure: ProjectStructure = Field(
        default=ProjectStructure.MONOREPO,
        description="Project structure type",
    )

    # Python version
    python_version: PythonVersion = Field(
        default=PythonVersion.PY313,
        description="Minimum Python version",
    )

    # Features
    features: FeatureSet = Field(default_factory=FeatureSet)

    # Samples
    with_samples: bool = Field(default=True, description="Include sample packages")

    # Documentation
    docs_theme: DocsTheme = Field(
        default=DocsTheme.MATERIAL,
        description="MkDocs theme",
    )

    # License
    license_type: LicenseType = Field(default=LicenseType.MIT, description="License type")

    # Git
    init_git: bool = Field(default=True, description="Initialize git repository")

    # Metadata (optional, can be prompted or defaulted)
    author_name: str = Field(default="", description="Author name")
    author_email: str = Field(default="", description="Author email")
    description: str = Field(default="", description="Project description")
    github_owner: str = Field(default="", description="GitHub username/org")

    @field_validator("project_name")
    @classmethod
    def validate_project_name(cls, v: str) -> str:
        """Validate and normalize project name."""
        # Replace hyphens with underscores for Python identifier
        normalized = v.replace("-", "_").lower()
        if not normalized.isidentifier():
            msg = f"Project name '{v}' is not a valid Python identifier"
            raise ValueError(msg)
        return normalized

    @property
    def project_slug(self) -> str:
        """Get URL/PyPI slug (hyphens)."""
        return self.project_name.replace("_", "-")

    @property
    def namespace(self) -> str:
        """Get Python namespace (same as project_name with underscores)."""
        return self.project_name

    @property
    def python_requires(self) -> str:
        """Get requires-python string."""
        return f">={self.python_version.value}"


class PackageConfig(BaseModel):
    """Configuration for adding a new package."""

    package_name: str = Field(..., description="Package name")
    package_type: PackageType = Field(..., description="Package type (lib or app)")
    description: str = Field(default="", description="Package description")
    with_docker: bool = Field(default=False, description="Include Dockerfile (apps only)")

    # Context from parent project
    namespace: str = Field(..., description="Project namespace for imports")
    python_requires: str = Field(default=">=3.13", description="Python version requirement")

    @field_validator("package_name")
    @classmethod
    def validate_package_name(cls, v: str) -> str:
        """Validate and normalize package name."""
        normalized = v.replace("-", "_").lower()
        if not normalized.isidentifier():
            msg = f"Package name '{v}' is not a valid Python identifier"
            raise ValueError(msg)
        return normalized


class TemplateContext(BaseModel):
    """Context variables passed to Jinja2 templates."""

    # Project info
    project_name: str
    project_slug: str
    project_description: str = ""
    namespace: str
    python_version: str
    python_requires: str

    # Author info
    author_name: str = ""
    author_email: str = ""

    # GitHub info
    github_owner: str = ""
    github_repo: str = ""

    # License
    license_type: str = "MIT"

    # Package info (for package templates)
    package_name: str = ""
    package_description: str = ""

    # Feature flags
    with_ruff: bool = True
    with_ty: bool = True
    with_pytest: bool = True
    with_poethepoet: bool = True
    with_pre_commit: bool = True
    with_github_actions: bool = False
    with_pypi_publish: bool = False
    with_docker: bool = False
    with_docs: bool = False
    docs_theme: str = "material"
    with_samples: bool = True

    # Runtime info
    year: int = 2024

    @classmethod
    def from_project_config(cls, config: ProjectConfig) -> "TemplateContext":
        """Create template context from project config."""
        from datetime import datetime

        return cls(
            project_name=config.project_name,
            project_slug=config.project_slug,
            project_description=config.description,
            namespace=config.namespace,
            python_version=config.python_version.value,
            python_requires=config.python_requires,
            author_name=config.author_name,
            author_email=config.author_email,
            github_owner=config.github_owner,
            github_repo=config.project_slug,
            license_type=config.license_type.value,
            with_ruff=config.features.ruff,
            with_ty=config.features.ty,
            with_pytest=config.features.pytest,
            with_poethepoet=config.features.poethepoet,
            with_pre_commit=config.features.pre_commit,
            with_github_actions=config.features.github_actions,
            with_pypi_publish=config.features.pypi_publish,
            with_docker=config.features.docker,
            with_docs=config.features.docs,
            docs_theme=config.docs_theme.value,
            with_samples=config.with_samples,
            year=datetime.now().year,
        )

    @classmethod
    def from_package_config(cls, pkg_config: PackageConfig, project_ctx: "TemplateContext") -> "TemplateContext":
        """Create template context for package generation."""
        # Exclude package-specific fields that we'll override
        base_data = project_ctx.model_dump(exclude={"package_name", "package_description", "with_docker"})
        return cls(
            **base_data,
            package_name=pkg_config.package_name,
            package_description=pkg_config.description,
            with_docker=pkg_config.with_docker,
        )


def detect_project_config(path: Path) -> ProjectConfig | None:
    """Detect project configuration from existing pyproject.toml."""
    pyproject_path = path / "pyproject.toml"
    if not pyproject_path.exists():
        return None

    try:
        import tomllib

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        # Check for workspace configuration
        workspace = data.get("tool", {}).get("uv", {}).get("workspace", {})
        una = data.get("tool", {}).get("una", {})

        if not workspace and not una:
            return None

        # Extract project info
        project = data.get("project", {})
        name = project.get("name", path.name)
        requires_python = project.get("requires-python", ">=3.13")

        # Determine Python version from requires-python
        py_version = PythonVersion.PY313
        if "3.11" in requires_python:
            py_version = PythonVersion.PY311
        elif "3.12" in requires_python:
            py_version = PythonVersion.PY312

        # Detect structure
        structure = ProjectStructure.MONOREPO if workspace.get("members") else ProjectStructure.SINGLE

        return ProjectConfig(
            project_name=name,
            structure=structure,
            python_version=py_version,
            description=project.get("description", ""),
        )
    except Exception:
        return None
