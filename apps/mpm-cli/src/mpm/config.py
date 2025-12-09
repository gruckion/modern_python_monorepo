"""Configuration models for MPM CLI."""

from enum import Enum

from pydantic import BaseModel, Field


class ProjectStructure(str, Enum):
    MONOREPO = "monorepo"
    SINGLE = "single"


class PythonVersion(str, Enum):
    PY311 = "3.11"
    PY312 = "3.12"
    PY313 = "3.13"


class LicenseType(str, Enum):
    MIT = "MIT"
    APACHE = "Apache-2.0"
    GPL = "GPL-3.0"
    NONE = "none"


class DocsTheme(str, Enum):
    MATERIAL = "material"
    SHADCN = "shadcn"


class ProjectConfig(BaseModel):
    """Configuration for project generation."""

    project_name: str = Field(..., description="Project name (Python identifier)")
    project_slug: str = Field(..., description="URL-safe project slug")
    project_description: str = Field(default="", description="Project description")
    structure: ProjectStructure = Field(default=ProjectStructure.MONOREPO)
    python_version: PythonVersion = Field(default=PythonVersion.PY313)
    license_type: LicenseType = Field(default=LicenseType.MIT)

    # Optional features
    with_samples: bool = Field(default=False)
    with_docker: bool = Field(default=False)
    with_ci: bool = Field(default=False)
    with_pypi: bool = Field(default=False)
    with_docs: bool = Field(default=False)
    docs_theme: DocsTheme = Field(default=DocsTheme.MATERIAL)
    with_precommit: bool = Field(default=True)

    # Git
    init_git: bool = Field(default=True)

    # Auto-sync
    auto_sync: bool = Field(default=True, description="Run uv sync after project generation")

    # Metadata
    author_name: str = Field(default="")
    author_email: str = Field(default="")
    github_owner: str = Field(default="")
    github_repo: str = Field(default="")

    @property
    def namespace(self) -> str:
        """Python import namespace (underscores)."""
        return self.project_name.replace("-", "_")


class PackageConfig(BaseModel):
    """Configuration for package generation (add lib/app)."""

    package_name: str
    package_type: str  # "lib" or "app"
    description: str = ""
    with_docker: bool = False  # Only for apps
