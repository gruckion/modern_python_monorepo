"""Tests for configuration models."""

import pytest

from modern_python_monorepo.mpm.config import (
    FeatureSet,
    PackageConfig,
    PackageType,
    ProjectConfig,
    ProjectStructure,
    PythonVersion,
    TemplateContext,
)


class TestProjectConfig:
    """Tests for ProjectConfig."""

    def test_valid_project_name(self) -> None:
        """Test valid project name."""
        config = ProjectConfig(project_name="my_project")
        assert config.project_name == "my_project"

    def test_project_name_with_hyphens(self) -> None:
        """Test project name with hyphens is normalized."""
        config = ProjectConfig(project_name="my-project")
        assert config.project_name == "my_project"

    def test_invalid_project_name(self) -> None:
        """Test invalid project name raises error."""
        with pytest.raises(ValueError):
            ProjectConfig(project_name="123invalid")

    def test_project_slug(self) -> None:
        """Test project slug property."""
        config = ProjectConfig(project_name="my_project")
        assert config.project_slug == "my-project"

    def test_namespace(self) -> None:
        """Test namespace property."""
        config = ProjectConfig(project_name="my_project")
        assert config.namespace == "my_project"

    def test_python_requires(self) -> None:
        """Test python_requires property."""
        config = ProjectConfig(
            project_name="test",
            python_version=PythonVersion.PY312,
        )
        assert config.python_requires == ">=3.12"


class TestFeatureSet:
    """Tests for FeatureSet."""

    def test_default_values(self) -> None:
        """Test default feature values."""
        features = FeatureSet()
        assert features.ruff is True
        assert features.ty is True
        assert features.pytest is True
        assert features.poethepoet is True
        assert features.pre_commit is True
        assert features.github_actions is False
        assert features.pypi_publish is False
        assert features.docker is False
        assert features.docs is False


class TestPackageConfig:
    """Tests for PackageConfig."""

    def test_valid_package_name(self) -> None:
        """Test valid package name."""
        config = PackageConfig(
            package_name="auth",
            package_type=PackageType.LIB,
            namespace="my_project",
        )
        assert config.package_name == "auth"

    def test_package_name_with_hyphens(self) -> None:
        """Test package name with hyphens is normalized."""
        config = PackageConfig(
            package_name="my-auth",
            package_type=PackageType.LIB,
            namespace="my_project",
        )
        assert config.package_name == "my_auth"


class TestTemplateContext:
    """Tests for TemplateContext."""

    def test_from_project_config(self) -> None:
        """Test creating context from project config."""
        config = ProjectConfig(
            project_name="test_project",
            structure=ProjectStructure.MONOREPO,
            python_version=PythonVersion.PY313,
        )
        ctx = TemplateContext.from_project_config(config)

        assert ctx.project_name == "test_project"
        assert ctx.project_slug == "test-project"
        assert ctx.namespace == "test_project"
        assert ctx.python_version == "3.13"
        assert ctx.python_requires == ">=3.13"

    def test_from_package_config(self) -> None:
        """Test creating context from package config."""
        project_config = ProjectConfig(project_name="test_project")
        project_ctx = TemplateContext.from_project_config(project_config)

        pkg_config = PackageConfig(
            package_name="auth",
            package_type=PackageType.LIB,
            description="Auth utils",
            namespace="test_project",
        )
        ctx = TemplateContext.from_package_config(pkg_config, project_ctx)

        assert ctx.package_name == "auth"
        assert ctx.package_description == "Auth utils"
        assert ctx.namespace == "test_project"
