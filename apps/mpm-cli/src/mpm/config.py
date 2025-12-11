"""Configuration models for MPM CLI."""

from datetime import UTC, datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    """Return current UTC time as timezone-aware datetime."""
    return datetime.now(UTC)


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
    with_agents_md: bool = Field(default=True, description="Generate AGENTS.md for AI assistants")

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


class MpmConfig(BaseModel):
    """Configuration stored in mpm.toml at project root.

    This file stores scaffolding choices to enable `mpm add` commands
    to understand the existing configuration.
    """

    # MPM metadata
    version: str = Field(default="0.1.0", description="CLI version that created project")
    created_at: datetime = Field(default_factory=_utc_now)

    # Project info
    project_name: str = Field(..., description="Python identifier name")
    project_slug: str = Field(..., description="URL-safe slug")
    project_description: str = Field(default="")

    # Generation settings
    structure: ProjectStructure = Field(default=ProjectStructure.MONOREPO)
    python_version: PythonVersion = Field(default=PythonVersion.PY313)
    license_type: LicenseType = Field(default=LicenseType.MIT)

    # Features
    with_samples: bool = Field(default=False)
    with_docker: bool = Field(default=False)
    with_ci: bool = Field(default=False)
    with_pypi: bool = Field(default=False)
    with_docs: bool = Field(default=False)
    docs_theme: DocsTheme = Field(default=DocsTheme.MATERIAL)
    with_precommit: bool = Field(default=True)
    with_agents_md: bool = Field(default=True, description="Generate AGENTS.md for AI assistants")

    # Metadata
    author_name: str = Field(default="")
    author_email: str = Field(default="")
    github_owner: str = Field(default="")
    github_repo: str = Field(default="")

    @classmethod
    def from_project_config(cls, config: "ProjectConfig", version: str = "0.1.0") -> "MpmConfig":
        """Create MpmConfig from ProjectConfig."""
        return cls(
            version=version,
            created_at=_utc_now(),
            project_name=config.project_name,
            project_slug=config.project_slug,
            project_description=config.project_description,
            structure=config.structure,
            python_version=config.python_version,
            license_type=config.license_type,
            with_samples=config.with_samples,
            with_docker=config.with_docker,
            with_ci=config.with_ci,
            with_pypi=config.with_pypi,
            with_docs=config.with_docs,
            docs_theme=config.docs_theme,
            with_precommit=config.with_precommit,
            with_agents_md=config.with_agents_md,
            author_name=config.author_name,
            author_email=config.author_email,
            github_owner=config.github_owner,
            github_repo=config.github_repo,
        )

    @classmethod
    def from_toml(cls, path: Path) -> "MpmConfig":
        """Load MpmConfig from mpm.toml file."""
        import tomllib

        with open(path, "rb") as f:
            data = tomllib.load(f)

        # Flatten nested structure
        return cls(
            version=data.get("mpm", {}).get("version", "0.1.0"),
            created_at=datetime.fromisoformat(data.get("mpm", {}).get("created_at", _utc_now().isoformat())),
            project_name=data.get("project", {}).get("name", ""),
            project_slug=data.get("project", {}).get("slug", ""),
            project_description=data.get("project", {}).get("description", ""),
            structure=ProjectStructure(data.get("generation", {}).get("structure", "monorepo")),
            python_version=PythonVersion(data.get("generation", {}).get("python_version", "3.13")),
            license_type=LicenseType(data.get("generation", {}).get("license", "MIT")),
            with_samples=data.get("features", {}).get("samples", False),
            with_docker=data.get("features", {}).get("docker", False),
            with_ci=data.get("features", {}).get("ci", False),
            with_pypi=data.get("features", {}).get("pypi", False),
            with_docs=data.get("features", {}).get("docs", False),
            docs_theme=DocsTheme(data.get("features", {}).get("docs_theme", "material")),
            with_precommit=data.get("features", {}).get("precommit", True),
            with_agents_md=data.get("features", {}).get("agents_md", True),
            author_name=data.get("metadata", {}).get("author_name", ""),
            author_email=data.get("metadata", {}).get("author_email", ""),
            github_owner=data.get("metadata", {}).get("github_owner", ""),
            github_repo=data.get("metadata", {}).get("github_repo", ""),
        )

    def to_toml_dict(self) -> dict:
        """Convert to TOML-friendly nested dict structure."""
        return {
            "mpm": {
                "version": self.version,
                "created_at": self.created_at.isoformat(),
            },
            "project": {
                "name": self.project_name,
                "slug": self.project_slug,
                "description": self.project_description,
            },
            "generation": {
                "structure": self.structure.value,
                "python_version": self.python_version.value,
                "license": self.license_type.value,
            },
            "features": {
                "samples": self.with_samples,
                "docker": self.with_docker,
                "ci": self.with_ci,
                "pypi": self.with_pypi,
                "docs": self.with_docs,
                "docs_theme": self.docs_theme.value,
                "precommit": self.with_precommit,
                "agents_md": self.with_agents_md,
            },
            "metadata": {
                "author_name": self.author_name,
                "author_email": self.author_email,
                "github_owner": self.github_owner,
                "github_repo": self.github_repo,
            },
        }
